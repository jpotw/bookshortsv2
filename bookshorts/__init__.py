from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from models import db
# from models import Fcuser
import config
from flask_login import LoginManager
# from .models import Fcuser

db = SQLAlchemy()
migrate = Migrate()
# login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config) #뭐임 이거? -> config.py를 app.config로 불러오는 거 **get 아니고 from_object**
    app.debug = True


    #login_manager
    # login_manager.init_app(app)

    #ORM
    db.init_app(app)
    migrate.init_app(app,db) #migrate은 뭐하는거
    from . import models
    from .views import main_views, history_views, auth_views, summarize_views
    app.register_blueprint(main_views.bp) #main_views 파일에 bp(blueprint로 만든 객체) 불러오기
    app.register_blueprint(history_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(summarize_views.bp)  
    return app



# @login_manager.user_loader
# def load_user(user_id):
#     return Fcuser.query.get(int(user_id)) 