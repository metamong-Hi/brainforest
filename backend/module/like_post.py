from flask import Blueprint, jsonify, request
from bson import ObjectId
from pymongo import MongoClient

# MongoDB 연결 설정
client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
users_collection = db["USERS"]
posts_collection = db["POSTS"]
likes_collection = db["LIKES"]

like_post_bp = Blueprint('like_post', __name__)

@like_post_bp.route('/api/v1/like/<postId>', methods=['PUT'])
def like_post(postId):
    userId = str(request.json.get('userId'))  # ObjectId를 문자열로 변환
    
    post = posts_collection.find_one({"_id": ObjectId(postId)})
    if not post:
        return jsonify({"message": "게시물을 찾을 수 없습니다."}), 404

    # 좋아요 정보를 찾는다
    like_data = likes_collection.find_one({"post_id": ObjectId(postId), "user_id": userId})

    # 좋아요 취소
    if like_data:
        likes_collection.delete_one({"post_id": ObjectId(postId), "user_id": userId})
        posts_collection.update_one({"_id": ObjectId(postId)}, {"$inc": {"like": -1}}) # 좋아요 수 감소
        return jsonify({"status": "unliked"}), 200

    # 좋아요 등록
    else:
        likes_collection.insert_one({"post_id": ObjectId(postId), "user_id": userId})
        posts_collection.update_one({"_id": ObjectId(postId)}, {"$inc": {"like": 1}}) # 좋아요 수 증가
        return jsonify({"status": "liked"}), 200
