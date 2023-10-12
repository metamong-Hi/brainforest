from flask import Blueprint, jsonify, request
from bson import ObjectId

like_post_bp = Blueprint('like_post', __name__)

@like_post_bp.route('/api/v1/like/<postId>', methods=['PUT'])
def like_post(posts_collection, postId):
    userId = str(request.json.get('userId'))  # ObjectId를 문자열로 변환
    
    post = posts_collection.find_one({"_id": ObjectId(postId)})
    if not post:
        return jsonify({"message": "게시물을 찾을 수 없습니다."}), 404
    
    # 좋아요 취소
    if userId in post['liked_by']:
        posts_collection.update_one({"_id": ObjectId(postId)}, {"$pull": {"liked_by": userId}, "$inc": {"like": -1}}) # '$inc' 는 특정 값 증감
        return jsonify({"status": "unliked"}), 200
    # 좋아요 등록
    else:
        posts_collection.update_one({"_id": ObjectId(postId)}, {"$push": {"liked_by": userId}, "$inc": {"like": 1}})
        return jsonify({"status": "liked"}), 200
