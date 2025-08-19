from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.models import Work, Copy, Author, AuthorName, Tag, Location, User
from forms.forms import WorkForm, CopyForm, BookForm

books_bp = Blueprint('books', __name__)

# Main books page
@books_bp.route('/')
def books():
    works = db.session.query(Work).all()
    return render_template('books.html', works=works)

# Works
@books_bp.route('/works')
def work_list():
    works = db.session.query(Work).all()
    return render_template('work_list.html', works=works)

# Work detail
@books_bp.route('/<int:id>')
def work_detail(id):
    work = db.session.query(Work).get(id)
    return render_template('work_detail.html', work=work)

# Copies list
@books_bp.route('/copies')
def copies_list():
    copies = db.session.query(Copy).all()
    return render_template('copies.html', copies=copies)

# Copies
@books_bp.route('/<int:work_id>/copies')
def work_copies(work_id):
    work = db.session.query(Work).get(work_id)
    copies = db.session.query(Copy).filter_by(work_id=work_id).all()
    return render_template('copies_list.html', work=work, copies=copies)

# Copy detail
@books_bp.route('/<int:work_id>/copies/<int:copy_id>')
def copy_detail(work_id, copy_id):
    work = db.session.query(Work).get(work_id)
    copy = db.session.query(Copy).get(copy_id)
    return render_template('copy_detail.html', work=work, copy=copy)

# Add a new book
@books_bp.route('/add', methods=['GET', 'POST'])
def book_add():
    form = BookForm()
        
    if form.validate_on_submit():
        if not form.isbn.data:
            return redirect(url_for('books.work_add'))
        
        existing_work = db.session.query(Work).filter_by(isbn=form.isbn.data).first()
        if existing_work:
            flash('A book with this ISBN already exists. Add Copy?', 'warning')
            return redirect(url_for('books.add_copy', work_id=existing_work.id))

        return redirect(url_for('books.work_add', isbn=form.isbn.data))

    return render_template('add_book.html', form=form, title='Add Book')

# Add a work
@books_bp.route('/works/add', methods=['GET', 'POST'])
def work_add(isbn=None):
    form = WorkForm()
    form.authors.choices = [(a.id, a.primary_name) for a in db.session.query(Author).all()]
    form.tags.choices = [(t.id, t.label) for t in db.session.query(Tag).all()]

    # If coming from book_add with ISBN, prefill
    if isbn:
        form.isbn.data = isbn

    if form.validate_on_submit():
        work = Work(
            title=form.title.data,
            isbn=form.isbn.data,
            cover_url=form.cover_url.data,
            description=form.description.data
        )

        # Add authors
        work.authors = db.session.query(Author).filter(Author.id.in_(form.authors.data)).all()

        # Add tags
        work.tags = db.session.query(Tag).filter(Tag.id.in_(form.tags.data)).all()

        db.session.add(work)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('books.work_detail', id=work.id))

    return render_template('work_form.html', form=form, title='Add Work')

# Add a copy
@books_bp.route('/<int:work_id>/copies/add', methods=['GET', 'POST'])
def copy_add(work_id):
    work = Work.query.get_or_404(work_id)
    form = CopyForm()
    form.work.choices = [(work.id, work.title)]
    form.location.choices = [(l.id, l.name) for l in Location.query.all()]
    form.owner.choices = [(o.id, o.name) for o in User.query.all()]

    if form.validate_on_submit():
        copy = Copy(
            work_id=form.work.data,
            location_id=form.location.data,
            owner_id=form.owner.data,
            condition=form.condition.data,
            lended_to=form.lended_to.data
        )
        db.session.add(copy)
        db.session.commit()
        flash('Copy added successfully!', 'success')
        return redirect(url_for('books.copies_list', work_id=work.id))
    
    return render_template('copy_form.html', form=form, title='Add Copy')

# Edit work
@books_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def work_edit(id):
    work = Work.query.get_or_404(id)
    form = WorkForm(obj=work)
    form.authors.choices = [(a.id, a.name) for a in Author.query.all()]
    form.tags.choices = [(t.id, t.label) for t in Tag.query.all()]

    if request.method == 'GET':
        form.authors.data = [author.id for author in work.authors]
        form.tags.data = [tag.id for tag in work.tags]

    if form.validate_on_submit():
        work.title = form.title.data
        work.isbn = form.isbn.data
        work.cover_url = form.cover_url.data
        work.description = form.description.data    

        # Update authors
        work.authors = Author.query.filter(Author.id.in_(form.authors.data)).all()

        # Update tags
        work.tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('books.work_detail', id=work.id))

    return render_template('work_form.html', form=form, title='Edit Work')

# Edit copy
@books_bp.route('/<int:work_id>/copies/<int:copy_id>/edit', methods=['GET', 'POST'])
def copy_edit(work_id, copy_id):
    work = Work.query.get_or_404(work_id)
    copy = Copy.query.get_or_404(copy_id)
    form = CopyForm(obj=copy)
    form.work.choices = [(w.id, w.title) for w in Work.query.all()]
    form.location.choices = [(l.id, l.name) for l in Location.query.all()]
    form.owner.choices = [(o.id, o.name) for o in User.query.all()]

    if form.validate_on_submit():
        copy.work_id = form.work.data
        copy.location_id = form.location.data
        copy.owner_id = form.owner.data
        copy.condition = form.condition.data
        copy.lended_to = form.lended_to.data
        
        db.session.commit()
        flash('Copy updated successfully!', 'success')
        return redirect(url_for('books.copy_detail', work_id=work.id, copy_id=copy.id))

    return render_template('copy_form.html', form=form, title='Edit Copy')

# Delete work
@books_bp.route('/<int:id>/delete', methods=['POST'])
def work_delete(id):
    work = Work.query.get_or_404(id)
    db.session.delete(work)
    db.session.commit()
    flash('Work deleted successfully!', 'success')
    return redirect(url_for('books.work_list'))