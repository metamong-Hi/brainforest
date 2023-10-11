from flask import Blueprint, jsonify, request
from bson import ObjectId

get_my_posts_bp = Blueprint('get_my_posts', __name__)

@get_my_posts_bp.route('/api/v1/mypost', methods=['GET'])
def get_my_posts(posts_collection):
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({"message": "사용자 ID가 필요합니다."}), 400

    user_id_obj = ObjectId(user_id)
    posts = list(posts_collection.find({"user_id": user_id_obj}))
    
    if not posts:
        return jsonify({"message": "게시물이 없습니다."}), 404

    return jsonify(posts), 200
