from bookshorts import db


#책 정보 저장
class BookInfo(db.Model): #db.Model = 모든 모델의 기본 class
    id = db.Column(db.Integer, primary_key=True) #primary_key를 통해 배타성을 확보
    title = db.Column(db.String(32), nullable=False) #빈값을 허용하고 싶지 않다면 nullable = False로 설정함.
    author = db.Column(db.String(32), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False) #생성 시간
    answer = db.Column(db.String(400), nullable=True) #나중에 저장


#회원가입
class Fcuser(db.Model): 
    __tablename__ = 'fcuser'   #테이블 이름 : fcuser : 주로 사용자 정보를 나타내는 클래스
    id = db.Column(db.Integer, primary_key = True)   #id를 프라이머리키로 설정
    password = db.Column(db.String(64))     #패스워드를 받아올 문자열길이 
    userid = db.Column(db.String(32))       #이하 위와 동일
    username = db.Column(db.String(8))
