from flask import Blueprint, jsonify, request
import jwt

get_my_posts_bp = Blueprint('get_my_posts', __name__)

@get_my_posts_bp.route('/api/v1/mypost', methods=['GET'])
def get_my_posts(posts_collection, app):
    user_id = jwt.decode(request.headers['Authorization'], app.config['SECRET_KEY'])['user_id']
    posts = list(posts_collection.find({"user_id": user_id}))
    return jsonify(posts), 200
