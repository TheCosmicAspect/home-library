from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class BookForm(FlaskForm):
    title = StringField('Title')
    isbn = StringField('ISBN', validators=[Length(min=10, max=20)])
    submit = SubmitField('Submit')

class WorkForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired(), Length(min=10, max=20)])
    authors = SelectMultipleField('Authors', coerce=int)
    publisher = StringField('Publisher')
    description = TextAreaField('Description')
    tags = SelectMultipleField('Tags', coerce=int)
    cover_url = StringField('Cover URL')
    submit = SubmitField('Submit')

class CopyForm(FlaskForm):
    work = SelectField('Work', coerce=int, validators=[DataRequired()])
    location = SelectField('Location', coerce=int, validators=[DataRequired()])
    owner = SelectField('Owner', coerce=int)
    condition = StringField('Condition', validators=[Length(max=50)])
    lended_to = SelectField('Lended To', coerce=int)
    submit = SubmitField('Submit')

class AuthorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    bio = TextAreaField('Bio')
    submit = SubmitField('Submit')

class AuthorNameForm(FlaskForm):
    author = SelectField('Author', coerce=int, validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TagForm(FlaskForm):
    label = StringField('Label', validators=[DataRequired()])
    description = TextAreaField('Description')
    parent = SelectField('Parent', coerce=int, validators=[DataRequired()])
    type = StringField('Type', validators=[Length(max=50)])
    submit = SubmitField('Submit')

class LocationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    parent = SelectField('Parent', coerce=int, validators=[DataRequired()])
    type = StringField('Type', validators=[Length(max=50)])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Submit')