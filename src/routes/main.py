from flask import Blueprint, render_template
from models.models import Copy
from models import db

main_bp = Blueprint('main', __name__)

# Index page
@main_bp.route('/')
def index():
    books = db.session.query(Copy).order_by(Copy.acquired.desc()).limit(10).all()
    return render_template('index.html', books=books)

# Search page
@main_bp.route('/search')
def search_page():
    return render_template('search.html')

# Error pages
@main_bp.app_errorhandler(404)
def error_page_404(error):
    return render_template('404.html'), 404