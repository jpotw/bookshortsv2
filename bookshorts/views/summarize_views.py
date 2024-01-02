from flask import Blueprint, render_template, request
from ..models import BookInfo
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv  
import os
from bookshorts import db


load_dotenv()
openai_api_key=os.getenv('OPENAI_API_KEY')

bp = Blueprint('/', __name__, url_prefix='/')


@bp.route('/bookinfo', methods=['POST', 'GET'])
def bookinfo():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        #회원정보 생성 (register html -> python 객체)
        title = request.form.get('title') 
        author = request.form.get('author')
        print(title, author) # 들어오나 확인해볼 수 있다. 

        if (title and author):
         #모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨) (python 객체 -> Database)
            bookinfo = BookInfo()         
            bookinfo.title = title          
            bookinfo.author = author
            bookinfo.create_date = datetime.now()      
            db.session.add(bookinfo)
            db.session.commit()
        
        book_info = f"{author}의 {title}"
        print(book_info)

        openai = OpenAI(api_key=openai_api_key)
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": 
            f'''Don't say; just do
            "당신은 지금부터 책 요약 전문가입니다. 
            저자가 작성한 책의 제목과 저자를 알려주면 당신은 책의 핵심인사이트를 요약합니다.
            {book_info}의 책의 핵심 포인트와 인사이트를 5가지로 요약해주세요."
            '''},
            ]   
        )
        content = response.choices[0].message.content
        for i in range(1, 6):  # Assuming there are up to 5 points
            if f"{i}." in content:
                content = content.replace(f"{i}. ", f"\n{i}. ")
            else: pass
        bookinfo.answer = content
        db.session.add(bookinfo)
        db.session.commit()
        # print(response.choices[0].message.content)
        return render_template('summarize.html', book_info=book_info, content=content) #author, title 정보를 summarize.html로 넘겨줌