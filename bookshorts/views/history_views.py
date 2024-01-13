#### 요약한 책을 볼 수 있는 뷰 ####


from flask import Flask, Blueprint, render_template, url_for
from ..models import BookInfo
import json



bp = Blueprint('history', __name__, url_prefix='/history')

# 요약 리스트 보여주기
@bp.route('/', methods=['GET'])
def history():
    book_list = BookInfo.query.order_by(BookInfo.create_date.desc())
    return render_template('book_list/book_list.html', book_list=book_list)

# 요약 리스트 클릭시 답변 상세 보기
@bp.route('/summarized/<int:id>', methods=['GET'])
def title(id):
    book = BookInfo.query.get_or_404(id)
    # answer 필드가 JSON 문자열인지 확인하고 리스트로 변환합니다.
    try:
        answer_list = json.loads(book.answer) if book.answer else []
    except json.JSONDecodeError:
        answer_list = []
    return render_template('book_list/summarized.html', book=book, answer_list=answer_list)