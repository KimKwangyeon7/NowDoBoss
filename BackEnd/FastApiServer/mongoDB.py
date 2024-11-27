from pymongo import MongoClient
import pandas as pd
from pyspark.sql import Row
from motor.motor_asyncio import AsyncIOMotorClient

# 연결에 필요한 정보
authenticationDatabase = "admin"
username = "ssafy"
password = "ssafy!2341234"
host = "k10c208.p.ssafy.io"
port = 27017

url = f"mongodb://{username}:{password}@{host}:{port}/{authenticationDatabase}"
client = AsyncIOMotorClient(url)
db = client.nowdoboss


async def find_weights(userId):
    collection = db['weights']
    document = await collection.find_one({"userId": userId})
    
    if not document:
        # 새 문서 생성 (userId 제외 모든 필드를 0으로 설정)
        document = {
            "userId": userId,
            "totalTrafficFootValue": 0.0,
            "totalSalesValue": 0.0,
            "openedRateValue": 0.0,
            "closedRateValue": 0.0,
            "totalConsumptionValue": 0.0,
            "finalRating": 0.0
        }
        await collection.insert_one(document)
        print(f"New document created for userId {userId} with default values.")
    else:
        document.pop('_id', None)
        print(f"Document found for userId {userId}.")
    
    return document

async def update_weights(new_record):
    collection = db['weights']
    if isinstance(new_record, Row):
        new_record = new_record.asDict()
    
    # userId를 기반으로 문서 업데이트
    result = await collection.update_one(
        {"userId": new_record['userId']}, 
        {"$set": new_record}
    )
    
    if result.matched_count == 0:
        print(f"No document found with userId {new_record['userId']} to update.")
    else:
        print(f"Document with userId {new_record['userId']} updated successfully.")
