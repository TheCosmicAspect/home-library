from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db
from models.models import Location
from forms.forms import LocationForm

locations_bp = Blueprint('locations', __name__)

# Locations main route - shows all locations
@locations_bp.route('/')
def location_list():
    locations = db.session.query(Location).all()
    return render_template('location_list.html', locations=locations)

# Location detail
@locations_bp.route('/<int:id>')
def location_detail(id):
    location = db.session.query(Location).get(id)
    return render_template('location_detail.html', location=location)

# Add Location
@locations_bp.route('/add', methods=['GET', 'POST'])
def location_add():
    form = LocationForm()
    form.parent.choices = [(0, '-none-')] + [(loc.id, loc.name) for loc in db.session.query(Location).all()]

    if form.validate_on_submit():
        if form.parent.data == 0:
            form.parent.data = None
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
    location = db.session.query(Location).get(id)
    form = LocationForm(obj=location)
    form.parent.choices = [(0, '-none-')] + [(loc.id, loc.name) for loc in db.session.query(Location).filter(Location.id != id).all()]

    if request.method == 'GET':
        form.name.data = location.name
        form.description.data = location.description
        form.parent.data = location.parent.id if location.parent else 0
        form.type.data = location.type

    if form.validate_on_submit():
        if form.parent.data == 0:
            form.parent.data = None
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
    location = db.session.query(Location).get(id)
    db.session.delete(location)
    db.session.commit()
    flash('Location deleted successfully!', 'success')
    return redirect(url_for('locations.location_list'))