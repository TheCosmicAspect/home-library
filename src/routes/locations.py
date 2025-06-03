from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db
from models.models import Location, Place
from forms.forms import LocationForm

locations_bp = Blueprint('locations', __name__)

@locations_bp.route('/')
def location_list():
    locations = Location.query.all()
    return render_template('location_list.html', locations=locations)

@locations_bp.route('/<int:id>')
def location_detail(id):
    location = Location.query.get_or_404(id)
    return render_template('location_detail.html', location=location)

@locations_bp.route('/add', methods=['GET', 'POST'])
def location_add():
    form = LocationForm()
    form.place.choices = [(p.id, p.name) for p in Place.query.all()]
    
    if form.validate_on_submit():
        location = Location(name=form.name.data)
        db.session.add(location)
        db.session.commit()
        flash('Location added successfully!', 'success')
        return redirect(url_for('locations.location_list'))
    
    return render_template('location_form.html', form=form, title='Add Location')

@locations_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def location_edit(id):
    location = Location.query.get_or_404(id)
    form = LocationForm(obj=location)
    
    if request.method == 'GET':
        form.name.data = location.name
        form.notes.data = location.notes

    if form.validate_on_submit():
        location.name = form.name.data
        location.notes = form.notes.data

        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('locations.location_detail', id=location.id))
    
    return render_template('location_form.html', form=form, title='Edit Location')

@locations_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def location_delete(id):
    location = Location.query.get_or_404(id)
    db.session.delete(location)
    db.session.commit()
    flash('Location deleted successfully!', 'success')
    return redirect(url_for('locations.location_list'))