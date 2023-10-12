from flask import Blueprint, request, jsonify

create_post_bp = Blueprint('create_post', __name__)

@create_post_bp.route('/api/v1/post', methods=['POST'])
def create_post(posts_collection, users_collection):
    post_data = request.json
    user_id = post_data['userId']
    
    post_data['like'] = 0

    # 게시물을 POSTS 컬렉션에 추가
    result = posts_collection.insert_one(post_data)
    
    if result:
        # 게시물 ID를 USERS 컬렉션의 해당 사용자의 posts 필드에 추가
        # users_collection에서 하나를 수정: 
        # '_id'의 필드값이 'user_id'와 일치하는 요소를 찾음 -> 'posts' 필드에 'result.insterted_id'값 push
        users_collection.update_one(
            {"_id": user_id},
            {"$push": {"posts": result.inserted_id}}
        ) 
        return jsonify({"postId": str(result.inserted_id)}), 201
    else:
        return jsonify({"message": "게시물 생성에 실패하였습니다."}), 500
