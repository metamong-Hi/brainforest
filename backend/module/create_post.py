from flask import Blueprint, request, jsonify
import jwt 

create_post_bp = Blueprint('create_post', __name__)

@create_post_bp.route('/api/v1/post', methods=['POST'])
def create_post(posts_collection, app):
    post_data = request.json
    user_id = jwt.decode(request.headers['Authorization'], app.config['SECRET_KEY'])['user_id']
    
    post_data['like'] = 0
    post_data['user_id'] = user_id

    result = posts_collection.insert_one(post_data)
    if result:
        return jsonify({"message": "Post created", "post_id": str(result.inserted_id)}), 201
    else:
        return jsonify({"message": "Failed to create post"}), 500
