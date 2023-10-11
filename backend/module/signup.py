from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/api/v1/signup', methods=['POST'])
def signup(users_collection, allowed_users):
    email = request.json.get('email')
    password = request.json.get('password')
    name = request.json.get('name')

    if users_collection.find_one({"email": email}):
        return jsonify({"status": "failure", "message": "이메일이 이미 존재합니다"}), 400

    if not any(user['이메일'] == email for user in allowed_users):
        return jsonify({"status": "failure", "message": "등록할 수 없는 이메일입니다"}), 403

    hashed_pw = generate_password_hash(password)
    users_collection.insert_one({
        "email": email,
        "password": hashed_pw,
        "name": name
    })

    return jsonify({"status": "success", "message": "회원가입 성공"}), 201
