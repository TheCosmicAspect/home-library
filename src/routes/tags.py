from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db
from models.models import Tag
from forms.forms import TagForm

tags_bp = Blueprint('tags', __name__)

@tags_bp.route('/')
def tag_list():
    tags = db.session.query(Tag).all()
    return render_template('tag_list.html', tags=tags)

# Tag detail view
@tags_bp.route('/<int:id>')
def tag_detail(id):
    tag = db.session.query(Tag).get(id)
    return render_template('tag_detail.html', tag=tag)

# Add Tag
@tags_bp.route('/add', methods=['GET', 'POST'])
def tag_add():
    form = TagForm()
    form.parent.choices = [(0, '-none-')] + [(tag.id, tag.label) for tag in db.session.query(Tag).all()]
    
    if form.validate_on_submit():
        if form.parent.data == 0:
            form.parent.data = None
        tag = Tag(
            label=form.label.data,
            description=form.description.data,
            parent_id=form.parent.data,
            type=form.type.data
        )
        db.session.add(tag)
        db.session.commit()
        flash('Tag added successfully!', 'success')
        return redirect(url_for('tags.tag_list'))
    
    return render_template('tag_form.html', form=form, title='Add Tag')

# Edit Tag
@tags_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def tag_edit(id):
    tag = db.session.query(Tag).get(id)
    form = TagForm(obj=tag)

    if request.method == 'GET':
        form.label.data = tag.label
        form.description.data = tag.description
        form.parent.data = tag.parent.id if tag.parent else None
        form.type.data = tag.type
        
    if form.validate_on_submit():
        tag.label = form.label.data
        tag.description = form.description.data
        tag.parent = form.parent.data
        tag.type = form.type.data

        db.session.commit()
        flash('Tag updated successfully!', 'success')
        return redirect(url_for('tags.tag_detail', id=tag.id))

    return render_template('tag_form.html', form=form, title='Edit Tag')

# Delete Tag
@tags_bp.route('/<int:id>/delete', methods=['POST'])
def tag_delete(id):
    tag = db.session.query(Tag).get(id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag deleted successfully!', 'success')
    return redirect(url_for('tags.tag_list'))
