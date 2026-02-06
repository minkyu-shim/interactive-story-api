from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # [추가]

db = SQLAlchemy()
migrate = Migrate() # [추가] 객체 생성

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db' # 본인의 DB 설정
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db) # [추가] 앱과 DB를 연결하여 초기화

    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app