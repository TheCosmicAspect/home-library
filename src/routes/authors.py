from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.models import Author
from forms.forms import AuthorForm

authors_bp = Blueprint('authors', __name__)

@authors_bp.route('/')
def author_list():
    authors = Author.query.all()
    return render_template('author_list.html', authors=authors)

@authors_bp.route('/<int:id>')
def author_detail(id):
    author = Author.query.get_or_404(id)
    return render_template('author_detail.html', author=author)

@authors_bp.route('/add', methods=['GET', 'POST'])
def author_add():
    form = AuthorForm()
    
    if form.validate_on_submit():
        author = Author(name=form.name.data)
        db.session.add(author)
        db.session.commit()
        flash('Author added successfully!', 'success')
        return redirect(url_for('authors.author_list'))
    
    return render_template('author_form.html', form=form, title='Add Author')

@authors_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def author_edit(id):
    author = Author.query.get_or_404(id)
    form = AuthorForm(obj=author)
    
    if request.method == 'GET':
        form.name.data = author.name
        form.bio.data = author.bio

    if form.validate_on_submit():
        author.name = form.name.data
        author.bio = form.bio.data
        db.session.commit()
        flash('Author updated successfully!', 'success')
        return redirect(url_for('authors.author_detail', id=author.id))
    
    return render_template('author_form.html', form=form, title='Edit Author')

@authors_bp.route('/<int:id>/delete', methods=['POST'])
def author_delete(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    flash('Author deleted successfully!', 'success')
    return redirect(url_for('authors.author_list'))