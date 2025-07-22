from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.models import Author, AuthorName
from forms.forms import AuthorForm

authors_bp = Blueprint('authors', __name__)

# Author main page - lists all authors
@authors_bp.route('/')
def author_list():
    authors = db.session.query(Author).all()
    return render_template('author_list.html', authors=authors)

# Author detail page
@authors_bp.route('/<int:id>')
def author_detail(id):
    author = db.session.query(Author).get(id)
    return render_template('author_detail.html', author=author)

# Add author
@authors_bp.route('/add', methods=['GET', 'POST'])
def author_add():
    form = AuthorForm()
    
    if form.validate_on_submit():
        author = Author(
            primary_name=form.name.data,
            bio=form.bio.data
        )
        db.session.add(author)
        db.session.flush()

        # Add alternative names
        for alt_name in form.alt_names.data:
            if alt_name:
                alt_name_entry = AuthorName(
                    author_id=author.id,
                    alt_name=alt_name
                )
                db.session.add(alt_name_entry)

        db.session.commit()
        flash('Author added successfully!', 'success')
        return redirect(url_for('authors.author_list'))
    
    return render_template('author_form.html', form=form, title='Add Author')

# Edit author
@authors_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def author_edit(id):
    author = db.session.query(Author).get(id)
    form = AuthorForm()
    
    if request.method == 'GET':
        form.name.data = author.primary_name
        form.bio.data = author.bio
        # Pre-fill alt_names
        for alt_name in author.alt_names:
            print(f'Adding alt {alt_name.alt_name}')
            form.alt_names.append_entry(alt_name.alt_name)

    if form.validate_on_submit():
        author.primary_name = form.name.data
        author.bio = form.bio.data
        db.session.commit()

        # TODO: Handle alternative names

        flash('Author updated successfully!', 'success')
        return redirect(url_for('authors.author_detail', id=author.id))
    
    return render_template('author_form.html', form=form, title='Edit Author')

@authors_bp.route('/<int:id>/delete', methods=['POST'])
def author_delete(id):
    author = db.session.query(Author).get(id)
    db.session.delete(author)
    db.session.commit()
    flash('Author deleted successfully!', 'success')
    return redirect(url_for('authors.author_list'))