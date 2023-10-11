from pymongo import MongoClient
import pandas as pd

# 엑셀 파일 읽기
df = pd.read_excel("주소록_modified.xlsx")

# MongoDB 클라이언트 생성
client = MongoClient("mongodb://localhost:27017/")

# 데이터베이스와 컬렉션 선택
db = client["jungle_db"]
users_collection = db["jungle_users"]
posts_collection = db["jungle_posts"]
# 데이터프레임의 각 행을 몽고DB에 저장
records = df.to_dict(orient='records')
users_collection.insert_many(records)
