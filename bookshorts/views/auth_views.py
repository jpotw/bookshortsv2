from flask import Blueprint, url_for, render_template, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from bookshorts import db
from ..models import Fcuser
from ..forms import UserLoginForm

bp = Blueprint('login', __name__, url_prefix='/login')

@bp.route('/', methods=['GET', 'POST'])
def login():
    form=UserLoginForm()
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        error=None
        userid = request.form.get('userid')
        password = request.form.get('password')
        print(userid, password)
        if not (userid and password):
            message = "아이디와 비밀번호를 입력해주세요"
            return render_template('login.html', message=message)
        else:
            fcuser = Fcuser.query.filter_by(userid=userid).first()
            if fcuser is None:
                message = "사용자가 존재하지 않습니다"
                return render_template('login.html', message=message)
            elif check_password_hash(fcuser.password, password):
                session['userid'] = userid
                return redirect(url_for('main.bookinfo'))
            else:
                message = "아이디와 비밀번호를 확인해주세요"
                return render_template('login.html', message=message)