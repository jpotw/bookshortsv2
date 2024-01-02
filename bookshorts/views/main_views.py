from flask import Blueprint, render_template, request, redirect, url_for
from bookshorts import db
from ..models import Fcuser
from werkzeug.security import generate_password_hash

#p45 main, __name__, url_prefix를 설정해 줘야 한다고 함. 처음 두 개 뭔지 나중에 확인할 것
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def login_first():
    return render_template('login.html')



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
            message = "모두 입력해주세요"
            return render_template('register.html', message=message)
        elif password != re_password:
            message = "비밀번호를 확인해주세요"
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


