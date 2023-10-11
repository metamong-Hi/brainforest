from flask import Blueprint, jsonify
from bson import ObjectId

delete_post_bp = Blueprint('delete_post', __name__)

@delete_post_bp.route('/api/v1/post/<postId>', methods=['DELETE'])
def delete_post(posts_collection, postId):
    result = posts_collection.delete_one({"_id": ObjectId(postId)})
    
    if result.deleted_count == 0:
        return jsonify({"status": "failure", "message": "글을 찾을 수 없습니다."}), 404
    
    return jsonify({"status": "success", "message": "글이 성공적으로 삭제되었습니다."}), 200
