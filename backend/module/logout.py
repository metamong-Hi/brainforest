from flask import Blueprint, jsonify

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/api/v1/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logged out successfully"}), 200
