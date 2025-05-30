from flask import Blueprint, render_template, redirect, url_for, flash
from models import db
from models.models import Owner
from forms.forms import OwnerForm

owners_bp = Blueprint('owners', __name__)

@owners_bp.route('/')
def owner_list():
    owners = Owner.query.all()
    return render_template('owner_list.html', owners=owners)

@owners_bp.route('/add', methods=['GET', 'POST'])
def owner_add():
    form = OwnerForm()
    
    if form.validate_on_submit():
        owner = Owner(name=form.name.data)
        db.session.add(owner)
        db.session.commit()
        flash('Owner added successfully!', 'success')
        return redirect(url_for('owners.owner_list'))
    
    return render_template('owner_form.html', form=form, title='Add Owner')

@owners_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def owner_delete(id):
    pass