from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import jwt
import datetime

login_bp = Blueprint('login', __name__)

@login_bp.route('/api/v1/login', methods=['POST'])
def login(users_collection, app):
    email = request.json.get('email')
    password = request.json.get('password')

    user = users_collection.find_one({"email": email})

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"message": "이메일 또는 비밀번호가 잘못되었습니다"}), 401

    token = jwt.encode({
        'user_id': user["id"],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'])

    return jsonify({"token": token, "name": user["name"]}), 200
