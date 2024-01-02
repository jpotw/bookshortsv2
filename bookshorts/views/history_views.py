from flask import Flask, Blueprint, render_template, url_for
from ..models import BookInfo



bp = Blueprint('history', __name__, url_prefix='/history')


@bp.route('/')
def history():
    book_list = BookInfo.query.order_by(BookInfo.create_date.desc())
    return render_template('book_list/book_list.html', book_list=book_list)


@bp.route('/summarized/<int:id>')
def title(id):
    book=BookInfo.query.get(id)
    return render_template('book_list/summarized.html', book=book)