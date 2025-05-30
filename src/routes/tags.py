from flask import Blueprint, render_template, redirect, url_for, flash
from models import db
from models.models import Tag
from forms.forms import TagForm

tags_bp = Blueprint('tags', __name__)

@tags_bp.route('/')
def tag_list():
    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags)

@tags_bp.route('/<int:id>')
def tag_detail(id):
    tag = Tag.query.get_or_404(id)
    return render_template('tag_detail.html', tag=tag)

@tags_bp.route('/add', methods=['GET', 'POST'])
def tag_add():
    form = TagForm()
    
    if form.validate_on_submit():
        tag = Tag(label=form.label.data)
        db.session.add(tag)
        db.session.commit()
        flash('Tag added successfully!', 'success')
        return redirect(url_for('tags.tag_list'))
    
    return render_template('tag_form.html', form=form, title='Add Tag')

@tags_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def tag_edit(id):
    form = TagForm()
    return render_template('tag_form.html', form=form, title='Edit Tag')

@tags_bp.route('/<int:id>/delete', methods=['POST'])
def tag_delete(id):
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag deleted successfully!', 'success')
    return redirect(url_for('tags.tag_list'))
