from flask import Blueprint, jsonify

view_most_liked_posts_bp = Blueprint('view_most_liked', __name__)

@view_most_liked_posts_bp.route('/api/v1/view/like/<category>', methods=['GET'])
def view_most_liked_posts(posts_collection, category):
    posts = list(posts_collection.find({"category": category}).sort("like", -1).limit(10))
    return jsonify(posts), 200
