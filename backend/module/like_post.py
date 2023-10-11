from flask import Blueprint, jsonify, request
from bson import ObjectId

like_post_bp = Blueprint('like_post', __name__)

@like_post_bp.route('/api/v1/like/<postId>', methods=['PUT'])
def like_post(posts_collection, postId):
    user_id = request.json.get('userId')
    
    post = posts_collection.find_one({"_id": ObjectId(postId)})
    if not post:
        return jsonify({"message": "게시물을 찾을 수 없습니다."}), 404
    
    # 이미 좋아요를 했는지 확인
    if 'liked_by' not in post:
        post['liked_by'] = []
    if user_id in post['liked_by']:
        # 좋아요 취소
        posts_collection.update_one({"_id": ObjectId(postId)}, {"$pull": {"liked_by": user_id}, "$inc": {"like": -1}})
        return jsonify({"status": "unliked"}), 200
    else:
        # 좋아요 등록
        posts_collection.update_one({"_id": ObjectId(postId)}, {"$push": {"liked_by": user_id}, "$inc": {"like": 1}})
        return jsonify({"status": "liked"}), 200
