from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import jwt
import datetime

login_bp = Blueprint('login', __name__)

@login_bp.route('/api/v1/login', methods=['POST'])
def login(users_collection, app):
    user_id = request.json.get('id')
    password = request.json.get('password')

    user = users_collection.find_one({"id": user_id})

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'])

    return jsonify({"token": token}), 200
