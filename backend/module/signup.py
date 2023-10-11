from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/api/v1/signup', methods=['POST'])
def signup(users_collection, allowed_users):
    user_id = request.json.get('id')  # 'email'을 'id'로 변경
    password = request.json.get('password')
    name = request.json.get('name')

    if users_collection.find_one({"id": user_id}):  # 'email'을 'id'로 변경
        return jsonify({"status": "failure", "message": "아이디가 이미 존재합니다"}), 400  # 메시지 수정

    if not any(user['아이디'] == user_id for user in allowed_users):  # '이메일'을 '아이디'로 변경
        return jsonify({"status": "failure", "message": "등록할 수 없는 아이디입니다"}), 403  # 메시지 수정

    hashed_pw = generate_password_hash(password)
    users_collection.insert_one({
        "id": user_id,  # 'email'을 'id'로 변경
        "password": hashed_pw,
        "name": name
    })

    return jsonify({"status": "success", "message": "회원가입 성공"}), 201
