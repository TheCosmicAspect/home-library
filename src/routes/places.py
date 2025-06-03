from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db
from models.models import Place
from forms.forms import PlaceForm

places_bp = Blueprint('places', __name__)

@places_bp.route('/')
def place_list():
    places = Place.query.all()
    return render_template('place_list.html', places=places)

@places_bp.route('/<int:id>')
def place_detail(id):
    place = Place.query.get_or_404(id)
    return render_template('place_detail.html', place=place)

@places_bp.route('/add', methods=['GET', 'POST'])
def place_add():
    form = PlaceForm()
    
    if form.validate_on_submit():
        place = Place(name=form.name.data)
        db.session.add(place)
        db.session.commit()
        flash('Place added successfully!', 'success')
        return redirect(url_for('places.place_list'))
    
    return render_template('place_form.html', form=form, title='Add Place')

@places_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def place_edit(id):
    place = Place.query.get_or_404(id)
    form = PlaceForm(obj=place)
    
    if request.method == 'GET':
        form.name.data = place.name
        form.notes.data = place.notes

    if form.validate_on_submit():
        place.name = form.name.data
        place.notes = form.notes.data

        db.session.commit()
        flash('Place updated successfully!', 'success')
        return redirect(url_for('places.place_detail', id=place.id))
    
    return render_template('place_form.html', form=form, title='Edit Place')

@places_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def place_delete(id):
    place = Place.query.get_or_404(id)
    db.session.delete(place)
    db.session.commit()
    flash('Place deleted successfully!', 'success')
    return redirect(url_for('places.place_list'))