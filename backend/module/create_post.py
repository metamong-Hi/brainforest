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
        return jsonify({"postId": str(result.inserted_id)}), 201
    else:
        return jsonify({"message": "게시물 생성에 실패하였습니다."}), 500
