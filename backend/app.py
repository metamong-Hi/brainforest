from flask import Flask
from pymongo import MongoClient
import pandas as pd
from module import (login, logout, create_post, get_my_posts, delete_post, 
                    like_post, update_post, view_most_liked_posts, view_recent_posts)
from init_db import initialize_db
from module.signup import signup as signup_func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# MongoDB 설정
client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
users_collection = db["jungle_users"]
posts_collection = db["jungle_posts"]

# 엑셀 파일에서 'id', 'name' 정보 가져오기
df = pd.read_excel("Jungle_DB.xlsx")
allowed_users = df[['id', 'name']].to_dict(orient='records')

@app.route('/api/v1/signup', methods=['POST'])
def signup_route():
    return signup_func(users_collection, allowed_users)

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
    app.run(debug=True)
