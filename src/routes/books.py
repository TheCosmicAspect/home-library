from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.models import Book, Author, Tag, Location, Owner
from forms.forms import BookForm

books_bp = Blueprint('books', __name__)

@books_bp.route('/')
def book_list():
    books = Book.query.all()
    return render_template('book_list.html', books=books)

@books_bp.route('/<int:id>')
def book_detail(id):
    book = Book.query.get_or_404(id)
    return render_template('book_detail.html', book=book)

@books_bp.route('/add', methods=['GET', 'POST'])
def book_add():
    form = BookForm()
    form.authors.choices = [(a.id, a.name) for a in Author.query.all()]
    form.tags.choices = [(t.id, t.label) for t in Tag.query.all()]
    form.location.choices = [(l.id, l.name) for l in Location.query.all()]
    form.owner.choices = [(o.id, o.name) for o in Owner.query.all()]

    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            isbn=form.isbn.data,
            cover_url=form.cover_url.data,
            location_id=form.location.data,
            description=form.description.data,
            owner_id=form.owner.data
        )
        
        # Add authors
        selected_authors = Author.query.filter(Author.id.in_(form.authors.data)).all()
        book.authors.extend(selected_authors)
        
        # Add tags
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        book.tags.extend(selected_tags)
        
        db.session.add(book)
        db.session.commit()
        
        flash('Book added successfully!', 'success')
        return redirect(url_for('books.book_list'))
    
    return render_template('book_form.html', form=form, title='Add Book')

@books_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def book_edit(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    form.authors.choices = [(a.id, a.name) for a in Author.query.all()]
    form.tags.choices = [(t.id, t.label) for t in Tag.query.all()]
    form.location.choices = [(l.id, l.name) for l in Location.query.all()]
    form.owner.choices = [(o.id, o.name) for o in Owner.query.all()]

    if request.method == 'GET':
        form.authors.data = [author.id for author in book.authors]
        form.tags.data = [tag.id for tag in book.tags]
        form.location.data = book.location_id
        form.owner.data = book.owner_id
    
    if form.validate_on_submit():
        book.title = form.title.data
        book.isbn = form.isbn.data
        book.cover_url = form.cover_url.data
        book.location_id = form.location.data
        book.description = form.description.data
        book.owner_id = form.owner.data
        
        # Update authors
        book.authors = Author.query.filter(Author.id.in_(form.authors.data)).all()
        
        # Update tags
        book.tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('books.book_detail', id=book.id))
    
    return render_template('book_form.html', form=form, title='Edit Book')

@books_bp.route('/<int:id>/delete', methods=['POST'])
def book_delete(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('books.book_list'))