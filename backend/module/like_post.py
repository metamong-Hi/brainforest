from flask import Blueprint, jsonify
from bson import ObjectId

like_post_bp = Blueprint('like_post', __name__)

@like_post_bp.route('/api/v1/like/<postId>', methods=['PUT'])
def like_post(posts_collection, postId):
    post = posts_collection.find_one({"_id": ObjectId(postId)})
    if not post:
        return jsonify({"message": "Post not found"}), 404
    posts_collection.update_one({"_id": ObjectId(postId)}, {"$inc": {"like": 1}})
    return jsonify({"message": "Liked successfully"}), 200
