from pyspark.sql import SparkSession, Row
from pyspark import SparkConf
from pyspark.sql.functions import col, udf, to_timestamp
from pyspark.sql.types import IntegerType
from pyspark.ml.recommendation import ALS, ALSModel
from pyspark.sql.functions import corr
import json
import datetime
from pyspark.sql.functions import explode
import os
from pyspark.sql.functions import when, desc
from pyspark.sql import functions as F
from pyspark.sql.functions import lit
from pyspark.sql.utils import AnalysisException
import concurrent.futures
import mongoDB
import pandas as pd
from fastapi import BackgroundTasks
from pydoop.hdfs import rm

model_path = "hdfs://master1:9000/model/model"
commercial_data_path = "hdfs://master1:9000/data/commercial_data.csv"
log_path = "hdfs://master1:9000/data/log_data.csv"

# HDFS에서 데이터를 읽는 함수
def read_new_data_from_hdfs(hdfs_path):
    print(f"Reading new data from {hdfs_path}")
    new_data = spark.read.csv(hdfs_path, header=True, inferSchema=True)
    return new_data

def delete_data_from_hdfs(hdfs_path):
    print(f"Deleting processed data from {hdfs_path}")
    try:
        rm(hdfs_path, recursive=True)
        print(f"Deleted {hdfs_path}")
    except Exception as e:
        print(f"Failed to delete {hdfs_path}: {e}")

# 사용자 행동별 가중치 부여 함수
def action_weight(action):
    weights = {"click": 2, "search":4, "analysis": 7, "save": 10}
    return weights.get(action, 0)

async def update_weights_in_background(weights_dict):
    mongoDB.update_weights(weights_dict)

async def train_or_continue_model(df_actions, hdfs_path):
    try:
        # 기존 모델 로드
        if os.path.exists(model_path):
            print(f"Loading existing model from {model_path}...")
            model = ALSModel.load(model_path)
            print("Model loaded successfully.")
            
            # 기존 userFactors와 itemFactors를 이어 학습 초기값으로 설정
            als = ALS(
                maxIter=5,
                regParam=0.01,
                userCol="userId",
                itemCol="commercialCode",
                ratingCol="weight",
                coldStartStrategy="drop",
                checkpointInterval=2
            ).setUserFactors(model.userFactors).setItemFactors(model.itemFactors)
        else:
            print("모델 존재 X")
            als = ALS(
                maxIter=5,
                regParam=0.01,
                userCol="userId",
                itemCol="commercialCode",
                ratingCol="weight",
                coldStartStrategy="drop"
            )

        model = als.fit(df_actions)
        model.write().overwrite().save(model_path)
        print(f"Model saved at: {model_path}")

        delete_data_from_hdfs(hdfs_path)
        return model

    except Exception as e:
        print(f"Error during model training or continuation: {e}")
        raise


async def recommend_commercials(spark, userId, background_tasks: BackgroundTasks):
    new_data = read_new_data_from_hdfs(log_path)
    df = pd.DataFrame(new_data)

    if df.empty:
        print("유저 데이터 없음")
        return
    df_actions = df[['userId', 'commercialCode', 'action']]
    sdf = spark.createDataFrame(df_actions)
    sdf = sdf.withColumn("weight", udf(action_weight, IntegerType())(col("action")))
    model = await load_or_train_model(sdf)

    commercial_data = spark.read.csv(commercial_data_path, header=True, inferSchema=True)
    commercial_columns = ["commercialCode", "totalTrafficFoot", "totalSales", "openedRate", "closedRate", "totalConsumption"]
    df_commercials = commercial_data.select(*commercial_columns)

    # 사용자별 상권 추천 - 추천 상권 개수는 추후 조정
    user_recommendations = model.recommendForAllUsers(20)

    recommendations_df = user_recommendations.withColumn("recommendation", explode("recommendations")).select(
        col("userId"),
        col("recommendation.commercialCode").alias("commercialCode"),
        col("recommendation.rating").alias("rating")
    )

    df_integrated_with_recommendations = recommendations_df.join(df_commercials, recommendations_df.commercialCode == df_commercials.commercialCode, "inner")
    df_integrated_with_recommendations = df_integrated_with_recommendations[df_integrated_with_recommendations['userId'] == userId]
    
    if df_integrated_with_recommendations.count() == 0:
        print("해당 유저의 정보 없음")
        empty_res = {}
        return empty_res
    
    # mongoDB에서 userId에 맞는 레코드 가져오기
    user_weights = await mongoDB.find_weights(userId)
    user_weights_df = pd.DataFrame([user_weights])  
    user_weights = spark.createDataFrame(user_weights_df)

    joined_df = df_integrated_with_recommendations.join(user_weights, on='userId', how='inner')
    joined_df = joined_df.fillna(0)
    weighted_df = joined_df.withColumn('weighted_totalTrafficFoot', col('totalTrafficFoot') * col('totalTrafficFootValue')) \
                        .withColumn('weighted_totalSales', col('totalSales') * col('totalSalesValue')) \
                        .withColumn('weighted_openedRate', col('openedRate') * col('openedRateValue')) \
                        .withColumn('weighted_closedRate', col('closedRate') * col('closedRateValue')) \
                        .withColumn('weighted_totalConsumption', col('totalConsumption') * col('totalConsumptionValue'))

    df_updated = weighted_df.withColumn(
        "final_rating",
        F.col("rating") + 
        F.col("weighted_totalTrafficFoot") +
        F.col("weighted_totalSales") +
        F.col("weighted_openedRate") +
        F.col("weighted_closedRate") +
        F.col("weighted_totalConsumption")
    )

    columns_to_drop = ["totalTrafficFootValue", "totalSalesValue",
                    "openedRateValue", "closedRateValue", "totalConsumptionValue", "weighted_totalTrafficFoot", "weighted_totalSales", "weighted_openedRate", "weighted_closedRate",
                    "weighted_totalConsumption", "rating"] 

    df_cleaned = df_updated.drop(*columns_to_drop)
    final_recommendations_sorted = df_cleaned.orderBy(desc('final_rating'))
    res = final_recommendations_sorted.toPandas().to_dict(orient="records")

    # 백그라운드에서 가중치 조정하고 바뀐 값 저장하기.
    background_tasks.add_task(update_weights_background, final_recommendations_sorted, spark, userId, user_weights, background_tasks)

    return res  

async def update_weights_background(final_recommendations_sorted, spark, userId, user_weights, background_tasks: BackgroundTasks):
    # 추천 점수와 각 특성 간의 상관관계 계산
    correlations = final_recommendations_sorted.select(
        corr("final_rating", "totalTrafficFoot").alias("corr_population"),
        corr("final_rating", "totalSales").alias("corr_sales"),
        corr("final_rating", "openedRate").alias("corr_openedRate"),
        corr("final_rating", "closedRate").alias("corr_closedRate"),
        corr("final_rating", "totalConsumption").alias("corr_consumption")
    )

    # correlations DataFrame의 각 열의 값을 수집하여 딕셔너리에 저장
    new_weights = {
        "userId": userId,
        "totalTrafficFootValue": correlations.select("corr_population").collect()[0][0],
        "totalSalesValue": correlations.select("corr_sales").collect()[0][0],
        "openedRateValue": correlations.select("corr_openedRate").collect()[0][0],
        "closedRateValue": correlations.select("corr_closedRate").collect()[0][0],
        "totalConsumptionValue": correlations.select("corr_consumption").collect()[0][0]
    }

    # 새로운 가중치와 이전 가중치 점진적 업데이트 (50%만 반영)
    update_ratio = 0.5
    updated_weights = user_weights.withColumn(
        "totalTrafficFootValue", 
        (col("totalTrafficFootValue") * (1 - update_ratio)) + (lit(new_weights["totalTrafficFootValue"]) * update_ratio)
    ).withColumn(
        "totalSalesValue", 
        (col("totalSalesValue") * (1 - update_ratio)) + (lit(new_weights["totalSalesValue"]) * update_ratio)
    ).withColumn(
        "openedRateValue", 
        (col("openedRateValue") * (1 - update_ratio)) + (lit(new_weights["openedRateValue"]) * update_ratio)
    ).withColumn(
        "closedRateValue", 
        (col("closedRateValue") * (1 - update_ratio)) + (lit(new_weights["closedRateValue"]) * update_ratio)
    ).withColumn(
        "totalConsumptionValue", 
        (col("totalConsumptionValue") * (1 - update_ratio)) + (lit(new_weights["totalConsumptionValue"]) * update_ratio)
    )
    weights_row = updated_weights.first().asDict()
    weights_dict = {key: float(value) for key, value in weights_row.items()}
    await mongoDB.update_weights(weights_dict)