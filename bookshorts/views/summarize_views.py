#### 책 입력 뷰 --> 책 요약 화면 html ####


from flask import Blueprint, render_template, request
from ..models import BookInfo, Fcuser
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv  
import os
from bookshorts import db
import re

load_dotenv()
openai_api_key=os.getenv('OPENAI_API_KEY')

bp = Blueprint('/', __name__, url_prefix='/')


#요약하기 버튼을 누르면 동작하는 것

@bp.route('/answer', methods=['GET', 'POST'])
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
            "당신은 세계 최고의 도서 요약 전문가입니다. 
            저자가 작성한 책의 제목과 저자를 알려주면 당신은 책의 핵심 인사이트를 저자에게 요약합니다.
            {book_info}의 책의 핵심 포인트와 인사이트를 5가지로 요약해주세요."
            , "형식: {book_info} 핵심 인사이트 요약: 1. 2. 3. 4. 5."
            '''},
            ]   
        )
        content = response.choices[0].message.content
        # 텍스트를 ':' 기준으로 분리합니다.
        sections = content.split(':')
        # 첫 번째 요소를 제목으로 사용합니다.
        title = sections[0]
        # 나머지 요소들을 순회하며 형식에 맞게 포맷팅합니다.
        summary = '\n'.join(f'{i+1}. {section.strip()}' for i, section in enumerate(sections[1:]))
        # 최종 결과를 출력합니다.
        formatted_text = f'{title}:\n{summary}'
        print(formatted_text)
        bookinfo.answer = formatted_text
        db.session.add(bookinfo)
        db.session.commit()
        # print(response.choices[0].message.content)
        return render_template('summarize.html', 
                               book_info=book_info, 
                               content=formatted_text) #author, title 정보를 summarize.html로 넘겨줌