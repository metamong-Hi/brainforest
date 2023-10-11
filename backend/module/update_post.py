from flask import Blueprint, request, jsonify
from bson import ObjectId

update_post_bp = Blueprint('update_post', __name__)

@update_post_bp.route('/api/v1/post/<postId>', methods=['PUT'])
def update_post(posts_collection, postId):
    post_data = request.json
    posts_collection.update_one({"_id": ObjectId(postId)}, {"$set": post_data})
    return jsonify({"message": "Post updated successfully"}), 200
