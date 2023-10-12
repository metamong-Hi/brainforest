from pymongo import MongoClient
import logging

# 로그 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB 설정 및 데이터베이스 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
users_collection = db["jungle_users"]

# 모든 'id' 값 가져오기
all_ids = [user['id'] for user in users_collection.find({}, {"id": 1})]

# 콘솔에 출력
for user_id in all_ids:
    logger.info(user_id)
