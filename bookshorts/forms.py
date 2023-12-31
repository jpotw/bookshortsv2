from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired

class UserLoginForm(FlaskForm):
    username=StringField('id', validators=[DataRequired()])
    passworkd= PasswordField('비밀번호', validators=[DataRequired()])