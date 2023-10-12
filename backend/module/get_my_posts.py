from flask import Blueprint, jsonify, request
from bson import ObjectId

get_my_posts_bp = Blueprint('get_my_posts', __name__)

@get_my_posts_bp.route('/api/v1/mypost', methods=['GET'])
def get_my_posts(posts_collection):
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({"message": "사용자 ID가 필요합니다."}), 400

    user_id_obj = ObjectId(user_id)
    posts = list(posts_collection.find({"userId": user_id_obj}))
    
    if not posts:
        return jsonify({"message": "게시물이 없습니다."}), 404

    # 게시물 데이터를 JSON 직렬화 가능한 형태로 변환
    serialized_posts = []
    for post in posts:
        post['_id'] = str(post['_id'])
        post['userId'] = str(post['userId'])
        serialized_posts.append(post)

    return jsonify(serialized_posts), 200

    
    # return jsonify(posts), 200 # 원본