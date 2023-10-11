from flask import Blueprint, jsonify

view_recent_posts_bp = Blueprint('view_recent', __name__)

@view_recent_posts_bp.route('/api/v1/view/recent/<category>', methods=['GET'])
def view_recent_posts(posts_collection, category):
    posts = list(posts_collection.find({"category": category}).sort("date", -1).limit(10))
    return jsonify(posts), 200
