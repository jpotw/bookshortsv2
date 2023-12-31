from flask import Blueprint, url_for, render_template, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from bookshorts import db
from ..models import Fcuser

bp = Blueprint()

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        userid = request.form.get('userid')
        password = request.form.get('password')
        print(userid, password)
        if not (userid and password):
            return "아이디와 비밀번호를 입력해주세요"
        else:
            fcuser = Fcuser.query.filter_by(userid=userid).first()
            if check_password_hash(fcuser.password, password):
                session['userid'] = userid
                return redirect(url_for('main.bookinfo'))
            else:
                return "아이디와 비밀번호를 확인해주세요"