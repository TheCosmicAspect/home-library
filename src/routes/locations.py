from flask import Blueprint, render_template, redirect, url_for, flash
from models import db
from models.models import Location
from forms.forms import LocationForm

locations_bp = Blueprint('locations', __name__)

# Locations main route - shows all locations
@locations_bp.route('/')
def location_list():
    locations = Location.query.all()
    return render_template('location_list.html', locations=locations)

# Location detail
@locations_bp.route('/<int:id>')
def location_detail(id):
    location = Location.query.get_or_404(id)
    return render_template('location_detail.html', location=location)

# Add a new location
@locations_bp.route('/add', methods=['GET', 'POST'])
def location_add():
    form = LocationForm()
    form.parent.choices = [(l.id, l.name) for l in Location.query.all()]

    if form.validate_on_submit():
        location = Location(
            name=form.name.data,
            description=form.description.data,
            parent_id=form.parent.data,
            type=form.type.data
        )
        db.session.add(location)
        db.session.commit()
        flash('Location added successfully!', 'success')
        return redirect(url_for('locations.location_list'))

    return render_template('location_form.html', form=form, title='Add Location')

# Edit location
@locations_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def location_edit(id):
    location = Location.query.get_or_404(id)
    form = LocationForm(obj=location)
    form.parent.choices = [(l.id, l.name) for l in Location.query.all()]

    if form.validate_on_submit():
        location.name = form.name.data
        location.description = form.description.data
        location.parent_id = form.parent.data
        location.type = form.type.data
        
        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('locations.location_detail', id=location.id))

    return render_template('location_form.html', form=form, title='Edit Location')

# Delete location
@locations_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def location_delete(id):
    location = Location.query.get_or_404(id)
    db.session.delete(location)
    db.session.commit()
    flash('Location deleted successfully!', 'success')
    return redirect(url_for('locations.location_list'))