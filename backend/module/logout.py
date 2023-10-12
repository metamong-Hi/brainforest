from flask import Blueprint, jsonify

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/api/v1/logout', methods=['POST'])
def logout():
    # 이 API 엔드포인트는 실제로는 아무런 작업을 수행하지 않습니다. 
    # 클라이언트 측에서 JWT 토큰을 삭제하는 것만으로 로그아웃을 처리합니다.
    # 이 엔드포인트는 사용자에게 로그아웃 되었다는 메시지를 전달하기 위한 것입니다.
    return jsonify({"status": "success", "message": "로그아웃 성공"}), 200
