#### 회원가입, 로그인을 처리하는 뷰 ####

from flask import Blueprint, url_for, render_template, request, session
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash
from ..models import Fcuser
from bookshorts import db


bp = Blueprint('login', __name__, url_prefix='/login')


#회원가입(login/register)
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        #회원정보 생성 (register html -> python 객체)
        username = request.form.get('username')
        userid = request.form.get('userid') 
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        print(password) # 들어오나 확인해볼 수 있다. 

        if not (username and userid and password and re_password) :
            message = "빈칸을 모두 입력해주세요"
            return render_template('register.html', message=message)
        elif password != re_password:
            message = "비밀번호가 일치하지 않습니다."
            return render_template('register.html', message=message)
        else: #모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨) (python 객체 -> Database)
            fcuser = Fcuser()
            fcuser.username = username
            fcuser.password = generate_password_hash(password)  #pw을 hash한 상태로 암호화해야 됨       
            fcuser.userid = userid    
            db.session.add(fcuser)
            db.session.commit()
            message = "회원가입 완료"
            return render_template('login.html', message=message)
        

#로그인(login/)
@bp.route('/', methods=['GET', 'POST'])
def login():
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
                return redirect(url_for('/.bookinfo'))
            else:
                message = "아이디와 비밀번호를 확인해주세요"
                return render_template('login.html', message=message)