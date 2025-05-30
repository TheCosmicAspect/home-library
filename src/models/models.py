from . import db
from sqlalchemy.sql import func

# Association tables
books_authors = db.Table('books_authors',
    db.Column('books_id', db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), primary_key=True),
    db.Column('authors_id', db.Integer, db.ForeignKey('authors.id', ondelete='CASCADE'), primary_key=True)
)

books_tags = db.Table('books_tags',
    db.Column('books_id', db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tags_id', db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

# Tables
class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    bio = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Author {self.name}>'

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Tag {self.label}>'

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    isbn = db.Column(db.String(20))
    description = db.Column(db.Text)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    cover_url = db.Column(db.Text)
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    authors = db.relationship('Author', secondary=books_authors, backref=db.backref('books', lazy='dynamic'))
    tags = db.relationship('Tag', secondary=books_tags, backref=db.backref('books', lazy='dynamic'))
    location = db.relationship('Location', backref=db.backref('books', lazy='dynamic'))
    owner = db.relationship('Owner', backref=db.backref('books', lazy='dynamic'))

    def __repr__(self):
        return f'<Book {self.title}>'

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    notes = db.Column(db.Text)
    place_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<Location {self.name}>'

class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<Place {self.name}>'

class Owner(db.Model):
    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __repr__(self):
        return f'<Owner {self.name}>'