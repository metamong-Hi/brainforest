from flask import Blueprint, request, jsonify
from bson import ObjectId
from pymongo import MongoClient

# MongoDB 연결 설정
client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
users_collection = db["USERS"]
posts_collection = db["POSTS"]
likes_collection = db["LIKES"]


update_post_bp = Blueprint('update_post', __name__)

@update_post_bp.route('/api/v1/post/<postId>', methods=['PUT'])
def update_post(posts_collection, postId):
    post_data = request.json
    
    result = posts_collection.update_one({"_id": ObjectId(postId)}, {"$set": post_data})
    
    if result.matched_count == 0:
        return jsonify({"status": "failure", "message": "글을 찾을 수 없습니다."}), 404
    
    if result.modified_count == 0:
        return jsonify({"status": "failure", "message": "글 수정에 실패했습니다."}), 500

    return jsonify({"status": "success", "message": "글이 성공적으로 수정되었습니다."}), 200