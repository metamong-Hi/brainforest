from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
import jwt
import datetime
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# MongoDB 설정
client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
users_collection = db["jungle_users"]
posts_collection = db["jungle_posts"]

# 엑셀 파일에서 '이름', '연락처', '이메일' 정보 가져오기
df = pd.read_excel("주소록_modified.xlsx")
allowed_users = df[['이름', '연락처', '이메일']].to_dict(orient='records')

@app.route('/api/v1/login', methods=['POST'])
def login():
    user_id = request.json.get('id')
    password = request.json.get('password')

    user = users_collection.find_one({"id": user_id})

    # 사용자가 없거나 비밀번호가 일치하지 않는 경우
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid credentials"}), 401

    # JWT 토큰 생성
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'])

    return jsonify({"token": token}), 200

@app.route('/api/v1/signup', methods=['POST'])
def signup():
    user_id = request.json.get('id')
    password = request.json.get('password')
    name = request.json.get('name')
    contact = request.json.get('contact')
    email = request.json.get('email')

    # 사용자 ID 중복 검사
    if users_collection.find_one({"id": user_id}):
        return jsonify({"message": "User ID already exists"}), 400

    # 엑셀 파일의 정보와 일치하는지 검사
    if not any(user['이름'] == name and user['연락처'] == contact and user['이메일'] == email for user in allowed_users):
        return jsonify({"message": "You're not allowed to register"}), 403

    # 비밀번호를 해싱하여 저장
    hashed_pw = generate_password_hash(password)
    users_collection.insert_one({
        "id": user_id,
        "password": hashed_pw,
        "name": name,
        "contact": contact,
        "email": email
    })

    return jsonify({"message": "Signup successful"}), 201

@app.route('/api/v1/post', methods=['POST'])
def create_post():
    post_data = request.json
    user_id = jwt.decode(request.headers['Authorization'], app.config['SECRET_KEY'])['user_id']
    
    post_data['like'] = 0
    post_data['user_id'] = user_id

    result = posts_collection.insert_one(post_data)
    if result:
        return jsonify({"message": "Post created", "post_id": str(result.inserted_id)}), 201
    else:
        return jsonify({"message": "Failed to create post"}), 500

@app.route('/api/v1/mypost', methods=['GET'])
def get_my_posts():
    user_id = jwt.decode(request.headers['Authorization'], app.config['SECRET_KEY'])['user_id']
    posts = list(posts_collection.find({"user_id": user_id}))
    return jsonify(posts), 200

@app.route('/api/v1/view/recent/<category>', methods=['GET'])
def view_recent_posts(category):
    posts = list(posts_collection.find({"category": category}).sort("date", -1).limit(10))
    return jsonify(posts), 200

@app.route('/api/v1/view/like/<category>', methods=['GET'])
def view_most_liked_posts(category):
    posts = list(posts_collection.find({"category": category}).sort("like", -1).limit(10))
    return jsonify(posts), 200

@app.route('/api/v1/like/<postId>', methods=['PUT'])
def like_post(postId):
    post = posts_collection.find_one({"_id": ObjectId(postId)})
    if not post:
        return jsonify({"message": "Post not found"}), 404
    posts_collection.update_one({"_id": ObjectId(postId)}, {"$inc": {"like": 1}})
    return jsonify({"message": "Liked successfully"}), 200

@app.route('/api/v1/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/api/v1/post/<postId>', methods=['PUT'])
def update_post(postId):
    post_data = request.json
    posts_collection.update_one({"_id": ObjectId(postId)}, {"$set": post_data})
    return jsonify({"message": "Post updated successfully"}), 200

@app.route('/api/v1/post/<postId>', methods=['DELETE'])
def delete_post(postId):
    posts_collection.delete_one({"_id": ObjectId(postId)})
    return jsonify({"message": "Post deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)