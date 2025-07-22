from flask import Blueprint, render_template, redirect, url_for, flash
from models import db
from models.models import User
from forms.forms import UserForm

users_bp = Blueprint('users', __name__)

# Users main route - shows all users
@users_bp.route('/')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

# User detail
@users_bp.route('/add', methods=['GET', 'POST'])
def user_add():
    form = UserForm()

    if form.validate_on_submit():
        user = User(name=form.name.data)
        db.session.add(user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('users.user_list'))

    return render_template('user_form.html', form=form, title='Add User')

# Edit user
@users_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def user_edit(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        user.name = form.name.data
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('users.user_list'))

    return render_template('user_form.html', form=form, title='Edit User')

# Delete user
@users_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def user_delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('users.user_list'))