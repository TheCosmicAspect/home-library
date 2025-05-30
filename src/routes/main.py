from flask import Blueprint, render_template
from models.models import Book

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    books = Book.query.order_by(Book.created_date.desc()).limit(10).all()
    return render_template('index.html', books=books)

@main_bp.route('/search')
def search_page():
    return render_template('search.html')