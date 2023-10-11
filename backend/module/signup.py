from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/api/v1/signup', methods=['POST'])
def signup(users_collection, allowed_users):
    user_id = request.json.get('id')
    password = request.json.get('password')
    name = request.json.get('name')

    if users_collection.find_one({"id": user_id}):
        return jsonify({"message": "User ID already exists"}), 400

    if not any(user['이름'] == name for user in allowed_users):
        return jsonify({"message": "You're not allowed to register"}), 403

    hashed_pw = generate_password_hash(password)
    users_collection.insert_one({
        "id": user_id,
        "password": hashed_pw,
        "name": name
    })

    return jsonify({"message": "Signup successful"}), 201
