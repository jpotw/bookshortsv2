from . import db #__init__.py 에 있는 db를 갖고온다, circular import 방지
from flask_login import UserMixin

# UserMixin 상속하여 flask_login에서 제공하는 기본 함수들 사용
class User(UserMixin):
    
    # User 객체에 저장할 사용자 정보
    # 그 외의 정보가 필요할 경우 추가한다. (ex. email 등)
    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password
    
    def get_id(self):
        return str(self.user_id)
    
    def get_password(self):
        return str(self.password)
    
    # User객체를 생성하지 않아도 사용할 수 있도록 staticmethod로 설정
    # 사용자가 작성한 계정 정보가 맞는지 확인하거나
    # flask_login의 user_loader에서 사용자 정보를 조회할 때 사용한다.
    @staticmethod
    def get_user_info(user_id, user_pw):
        result = dict()

        try:
            sql = ""
            sql += f"SELECT USER_ID, USER_NAME, `PASSWORD`, COMPANY_CODE, DEPARTMENT_CODE, POSITION_CODE, AUTH_CODE, "
            sql += f"REGISTER_DATETIME, LOGIN_DATETIME, LASTWEEK_REPORT_ID, THISWEEK_REPORT_ID, "
            sql += f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME "
            sql += f"FROM tn_user_info "
            if user_pw:
                sql += f"WHERE USER_ID = '{user_id}' AND `PASSWORD` = '{user_pw}'; "
            else:
                sql += f"WHERE USER_ID = '{user_id}'; "

            result = select(sql)
            
        except ex:
            result['result'] = 'fail'
            result['data'] = ex
        finally:
            return result
#책 정보 저장
class BookInfo(db.Model): #db.Model = 모든 모델의 기본 class
    id = db.Column(db.Integer, primary_key=True) #primary_key를 통해 배타성을 확보
    title = db.Column(db.String(32), nullable=False) #빈값을 허용하고 싶지 않다면 nullable = False로 설정함.
    author = db.Column(db.String(32), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False) #생성 시간
    answer = db.Column(db.String(400), nullable=True)

# GPT 답변 저장
# class Answer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     bookinfo_id = db.Column(db.Integer, db.ForeignKey('bookinfo.id', ondelete))
#     answer = db.Column(db.String(400), nullable=False)

#회원가입
class Fcuser(db.Model): 
    __tablename__ = 'fcuser'   #테이블 이름 : fcuser : 주로 사용자 정보를 나타내는 클래스
    id = db.Column(db.Integer, primary_key = True)   #id를 프라이머리키로 설정
    password = db.Column(db.String(64))     #패스워드를 받아올 문자열길이 
    userid = db.Column(db.String(32))       #이하 위와 동일
    username = db.Column(db.String(8))


# class User(UserMixin):
#     def __init__(self, userid, password):
#         self.userid = userid
#         self.password = password
#     def get_id(self):
#         return str(self.user_id)
#     def get_password(self):
#         return str(self.password)
    

#     # User객체를 생성하지 않아도 사용할 수 있도록 staticmethod로 설정
#     # 사용자가 작성한 계정 정보가 맞는지 확인하거나
#     # flask_login의 user_loader에서 사용자 정보를 조회할 때 사용한다.
#     @staticmethod
#     def get_user_info(userid, password):
#         result = dict()

#         try:
#             sql = ""
#             sql += f"SELECT USER_ID, USER_NAME, `PASSWORD`, COMPANY_CODE, DEPARTMENT_CODE, POSITION_CODE, AUTH_CODE, "
#             sql += f"REGISTER_DATETIME, LOGIN_DATETIME, LASTWEEK_REPORT_ID, THISWEEK_REPORT_ID, "
#             sql += f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME "
#             sql += f"FROM tn_user_info "
#             if user_pw:
#                 sql += f"WHERE USER_ID = '{user_id}' AND `PASSWORD` = '{user_pw}'; "
#             else:
#                 sql += f"WHERE USER_ID = '{user_id}'; "

#             result = select(sql)
            
#         except ex:
#             result['result'] = 'fail'
#             result['data'] = ex
#         finally:
#             return result
