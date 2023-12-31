from flask import Flask, render_template, request, redirect, url_for #render_template으로 html파일 렌더링
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from models import db
# from models import Fcuser
import config


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config) #뭐임 이거? -> config.py를 app.config로 불러오는 거 **get 아니고 from_object**
    app.debug = True

    #ORM
    db.init_app(app)
    migrate.init_app(app,db) #migrate은 뭐하는거
    from . import models
    from .views import main_views, history_views, auth_views
    app.register_blueprint(main_views.bp) #main_views 파일에 bp(blueprint로 만든 객체) 불러오기
    app.register_blueprint(history_views.bp)
    app.register_blueprint(auth_views.bp)    
    return app

#     @app.route('/')
#     def index():
#         return render_template('/index.html')

	
# with app.app_context():
# 	db.init_app(app) #초기화 후 db.app에 app으로 명시적으로 넣어줌
# 	db.app = app    
# 	db.create_all()


# app.run(host='127.0.0.1', port=5000, debug=True) 