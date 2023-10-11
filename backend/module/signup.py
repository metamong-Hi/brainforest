from flask import request, jsonify
from werkzeug.security import generate_password_hash

def signup(users_collection, allowed_users):
    user_id = request.json.get('id')
    password = request.json.get('password')
    name = request.json.get('name')
    
    if users_collection.find_one({"id": user_id}):
        return jsonify({"status": "failure", "message": "아이디가 이미 존재합니다"}), 400

    if not any(user['id'] == user_id for user in allowed_users):
        return jsonify({"status": "failure", "message": "등록할 수 없는 아이디입니다"}), 403

    hashed_pw = generate_password_hash(password)
    users_collection.insert_one({
        "id": user_id,
        "password": hashed_pw,
        "name": name
    })

    return jsonify({"status": "success", "message": "회원가입 성공"}), 201
