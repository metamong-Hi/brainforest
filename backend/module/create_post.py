from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from functools import wraps
import jwt

client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
users_collection = db["USERS"]
posts_collection = db["POSTS"]
likes_collection = db["LIKES"]

create_post_bp = Blueprint('create_post', __name__)
SECRET_KEY = 'your_secret_key_for_jwt'

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer ", "")

        if not token:
            return jsonify({"message": "토큰이 없습니다."}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = data['id']
        except:
            return jsonify({"message": "토큰이 유효하지 않습니다."}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@create_post_bp.route('/api/v1/post', methods=['POST'])
@jwt_required
def create_post(current_user):
    post_data = request.json
    post_data['like'] = 0
    post_data['user_id'] = current_user

    # 카테고리를 요청 데이터에서 가져와서 게시물 데이터에 추가
    category = post_data.get('category')
    if category:
        post_data['category'] = category

    result = posts_collection.insert_one(post_data)
    if result:
        return jsonify({"postId": str(result.inserted_id)}), 201
    else:
        return jsonify({"message": "게시물 생성에 실패하였습니다."}), 500
