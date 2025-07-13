from flask import Blueprint, render_template
from models.models import Copy
from models import db

main_bp = Blueprint('main', __name__)

# Index page
@main_bp.route('/')
def index():
    books = db.session.query(Copy).order_by(Copy.acquired.desc()).limit(10).all()
    for book in books:
        print(f"{book.title}: {book.acquired}")
    return render_template('index.html', books=books)

@main_bp.route('/search')
def search_page():
    return render_template('search.html')