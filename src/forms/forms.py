from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired(), Length(min=10, max=20)])
    authors = SelectMultipleField('Authors', coerce=int)
    description = TextAreaField('Description')
    location = SelectField('Location', coerce=int, validators=[DataRequired()])
    owner = SelectField('Owner', coerce=int, validators=[DataRequired()])
    tags = SelectMultipleField('Tags', coerce=int)
    cover_url = StringField('Cover URL')
    submit = SubmitField('Submit')

class AuthorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    bio = TextAreaField('Bio')
    submit = SubmitField('Submit')

class TagForm(FlaskForm):
    label = StringField('Label', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

class LocationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    place = SelectMultipleField('Places', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

class PlaceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Submit')

class OwnerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')