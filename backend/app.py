from flask import Flask, current_app
from pymongo import MongoClient
import pandas as pd
import logging
from module import (login, logout, create_post, get_my_posts, delete_post, 
                    like_post, update_post, view_most_liked_posts, view_recent_posts)
from module.signup import signup as signup_func

app = Flask(__name__)
# 로거 생성 및 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # 로그 레벨 설정

# 콘솔 출력 핸들러 설정
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# 로그 포맷 설정
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# 핸들러를 로거에 추가
logger.addHandler(ch)

app.config['SECRET_KEY'] = 'your_secret_key'
logger = logging.getLogger(__name__)  # 로거 생성

# MongoDB 설정 및 데이터베이스 연결을 앱의 컨텍스트에 저장
client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
app.config['USERS_COLLECTION'] = db["jungle_users"]
app.config['POSTS_COLLECTION'] = db["jungle_posts"]

@app.before_request
def check_mongodb_connection():
    """MongoDB 연결 상태 확인"""
    try:
        app.config['USERS_COLLECTION'].database.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB!")
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")

# 엑셀 파일에서 'id', 'name' 정보 가져오기
df = pd.read_excel(r"C:\Users\으훈\KraftonJungle\brainforest\backend\Jungle_DB.xlsx")
allowed_users = df[['id', 'name']].to_dict(orient='records')

@app.route('/api/v1/signup', methods=['POST'])
def signup_route():
    """회원 가입 라우트"""
    return signup_func(app.config['USERS_COLLECTION'], allowed_users)

@app.route('/')
def index():
    """홈 페이지 라우트"""
    return "Welcome to the homepage"

@app.errorhandler(404)
def page_not_found(e):
    """404 에러 핸들러"""
    return "페이지를 찾을 수 없습니다. 요청한 URL이 잘못되었을 수 있습니다.", 404

# 블루프린트 등록
app.register_blueprint(login.login_bp)
app.register_blueprint(logout.logout_bp)
app.register_blueprint(create_post.create_post_bp)
app.register_blueprint(get_my_posts.get_my_posts_bp)
app.register_blueprint(delete_post.delete_post_bp)
app.register_blueprint(like_post.like_post_bp)
app.register_blueprint(update_post.update_post_bp)
app.register_blueprint(view_most_liked_posts.view_most_liked_posts_bp)
app.register_blueprint(view_recent_posts.view_recent_posts_bp)

if __name__ == '__main__':
    check_mongodb_connection()
    app.run(debug=True, threaded=False, use_reloader=False)
