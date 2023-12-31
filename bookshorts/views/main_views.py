from flask import Blueprint, render_template, request, redirect, url_for
from bookshorts import db
from ..models import Fcuser
from ..models import BookInfo
from datetime import datetime


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
        userid = request.form.get('userid') 
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        print(password) # 들어오나 확인해볼 수 있다. 

        if not (userid and username and password and re_password) :
            return "모두 입력해주세요"
        elif password != re_password:
            return "비밀번호를 확인해주세요"
        else: #모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨) (python 객체 -> Database)
            fcuser = Fcuser()         
            fcuser.password = password           #models의 FCuser 클래스를 이용해 db에 입력한다.
            fcuser.userid = userid
            fcuser.username = username      
            db.session.add(fcuser)
            db.session.commit()
            return "회원가입 완료"


@bp.route('/bookinfo', methods=['POST', 'GET'])
def bookinfo():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        #회원정보 생성 (register html -> python 객체)
        title = request.form.get('title') 
        author = request.form.get('author')
        print(title, author) # 들어오나 확인해볼 수 있다. 

        if not (title and author) :
            return "모두 입력해주세요"
        else: #모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨) (python 객체 -> Database)
            bookinfo = BookInfo()         
            bookinfo.title = title          
            bookinfo.author = author      
            db.session.add(bookinfo)
            db.session.commit()
            return redirect(url_for('summarize'))
        

@bp.route('/summarize', methods=['POST'])
def summarize():
    return render_template('summarize.html')

