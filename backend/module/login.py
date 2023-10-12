from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
import logging

# Blueprint 초기화 및 로그 설정
login_bp = Blueprint('login', __name__)
logger = logging.getLogger(__name__)  # 로거 생성

SECRET_KEY = 'your_secret_key_for_jwt'

@login_bp.route('/api/v1/login', methods=['POST'])
def login():
    users_collection = current_app.config['USERS_COLLECTION']
    
    user_id = request.form.get('id')
    password = request.form.get('password')
    
    # POST로 받은 'id'와 'password'를 먼저 출력
    logger.warning(f"Received id: {user_id}, password: {password}")
    
    if user_id is None or password is None or user_id.strip() == '' or password.strip() == '':
        logger.warning("받은 값이 없습니다.")
        return jsonify({"message": "받은 값이 없습니다."}), 400
    
    # 모든 'id' 값 가져오기
    all_ids = [user['id'] for user in users_collection.find({}, {"id": 1})]
    
    # 입력받은 'id' 값이 DB에 있는 'id' 리스트에 있는지 확인
    if user_id not in all_ids:
        logger.warning("입력된 id가 DB에 존재하지 않습니다.")
        return jsonify({"message": "아이디가 틀렸습니다."}), 401
    else:
        logger.warning("id가 있습니다.")  # 'id'가 존재할 경우 로그에 기록
    
    # 해당 'id' 값을 가진 사용자 검색
    user = users_collection.find_one({"id": user_id})

    # 사용자의 비밀번호와 제공된 비밀번호가 일치하는지 확인
    stored_password_hash = user.get('password', '')
    if not check_password_hash(stored_password_hash, password):
        logger.warning("Incorrect password provided.")
        return jsonify({"message": "비밀번호가 틀렸습니다."}), 401

    # 로그인 성공 시 JWT 토큰 생성
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)  # 1일 뒤에 만료
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    logger.info("로그인 성공")
    return jsonify({"message": "로그인 성공", "token": token, "id_message": "id가 있습니다."}), 200
