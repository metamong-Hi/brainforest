from flask import Blueprint, jsonify

view_most_liked_posts_bp = Blueprint('view_most_liked', __name__)

@view_most_liked_posts_bp.route('/api/v1/view/like/<category>', methods=['GET'])
def view_most_liked_posts(posts_collection, category):
    posts = list(posts_collection.find({"category": category}).sort("like", -1).limit(10))
    
    if not posts:
        return jsonify({"message": "해당 카테고리의 게시물이 없습니다."}), 404

    # 결과 포맷을 API 명세서와 일치시킵니다.
    formatted_posts = [{"postId": post["_id"], "userId": post["user_id"]} for post in posts]
    return jsonify(formatted_posts), 200
