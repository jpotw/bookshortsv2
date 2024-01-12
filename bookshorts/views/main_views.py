#### 첫화면 ####

from flask import Blueprint, render_template, request, redirect, url_for
from bookshorts import db
from ..models import Fcuser
from werkzeug.security import generate_password_hash

#p45 main, __name__, url_prefix를 설정해 줘야 한다고 함. 처음 두 개 뭔지 나중에 확인할 것
bp = Blueprint('main', __name__, url_prefix='/')

# 바로 로그인 뷰로 redirect함
@bp.route('/')
def login_first():
    return render_template('login.html')

