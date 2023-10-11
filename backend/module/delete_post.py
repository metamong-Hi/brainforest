from flask import Blueprint, jsonify
from bson import ObjectId

delete_post_bp = Blueprint('delete_post', __name__)

@delete_post_bp.route('/api/v1/post/<postId>', methods=['DELETE'])
def delete_post(posts_collection, postId):
    posts_collection.delete_one({"_id": ObjectId(postId)})
    return jsonify({"message": "Post deleted successfully"}), 200
