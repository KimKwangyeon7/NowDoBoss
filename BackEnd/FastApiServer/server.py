
from pydantic import BaseModel
import spark_reco
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
import json
import scheduler
from hdfs import InsecureClient
from kafka import KafkaConsumer
import datetime

app = FastAPI()

class Item(BaseModel):
    data: str

class UserRequest(BaseModel):
    userId: int

# Kafka 컨슈머 설정
KAFKA_BROKERS = 'kafka-1:29092,kafka-2:29093,kafka-3:29094'
TOPIC_NAME = 'log-data'
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BROKERS.split(','),
    auto_offset_reset='earliest',
    group_id='log-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

HDFS_UPDATE_PATH = "hdfs://master1:9000/data/update_data.csv"
HDFS_LOG_PATH = "hdfs://master1:9000/logs/"


@app.post("/recommend")
async def recommend_commercial_areas(request: UserRequest, background_tasks: BackgroundTasks):
    print("추천에 도착!")
    try:
        # 요청 로그
        print(f"Received request: {request}")
        # 처리 로직
        spark = start_spark()
        response = await spark_reco.recommend_commercials(spark, request.userId, background_tasks)
        # 응답 로그
        print(f"Sending response: {response}")
        return response
    except Exception as e:
        # 에러 로그
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/data")
async def receive_data(request: Request):
    body = await request.body()
    data_str = body.decode('utf-8')
    data = json.loads(data_str)     
    print("Received data:", data)
    return {"message": "Data received successfully", "receivedData": data}

def start_spark():
    spark = SparkSession.builder \
        .appName("FastAPI-Spark Integration") \
        .getOrCreate()

    return spark

# Kafka 컨슈머로 메시지 수신
def process_kafka_messages():
    print("Starting Kafka consumer...")
    for message in consumer:
        try:
            print(f"Received message: {message.value}")
            save_logs_to_hdfs(message.value)
        except Exception as e:
            print(f"Error processing message: {e}")

# Kafka에서 메시지 저장
def save_logs_to_hdfs(message):
    # 메시지를 DataFrame으로 변환
    spark = start_spark()
    log_data = [{"userId": message["userId"], "action": message["action"]}]
    df = spark.createDataFrame(log_data)

    # 업데이트 용 파일 처리
    if not os.path.exists(HDFS_UPDATE_PATH):
        df.write.csv(HDFS_UPDATE_PATH, mode="overwrite", header=True)
    else:
        df.write.csv(HDFS_UPDATE_PATH, mode="append", header=True)
    print(f"Log saved to update file: {HDFS_UPDATE_PATH}")

    # 날짜별 로그 파일 처리
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    hdfs_file_path = f"{HDFS_LOG_PATH}logs-{current_date}.csv"

    if not os.path.exists(hdfs_file_path):
        df.write.csv(hdfs_file_path, mode="overwrite", header=True)
    else:
        df.write.csv(hdfs_file_path, mode="append", header=True)
    print(f"Log saved to daily log file: {hdfs_file_path}")




if __name__ == "__main__":
    process_kafka_messages()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)