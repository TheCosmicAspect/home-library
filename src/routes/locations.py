from flask import Blueprint, render_template, redirect, url_for, flash
from models import db
from models.models import Location
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
    pass

@locations_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def location_delete(id):
    pass