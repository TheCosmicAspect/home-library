from . import db
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, Text, String, BigInteger, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

# Association tables for many-to-many relationships
works_authors = Table(
    'works_authors',
    Base.metadata,
    Column('works_id', Integer, ForeignKey('works.id'), primary_key=True),
    Column('authors_id', Integer, ForeignKey('authors.id'), primary_key=True)
)

works_tags = Table(
    'works_tags',
    Base.metadata,
    Column('works_id', Integer, ForeignKey('works.id'), primary_key=True),
    Column('tags_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    primary_name = Column(Text, nullable=False)
    bio = Column(Text)
    
    # Relationships
    alt_names = relationship("AuthorName", back_populates="author")
    works = relationship("Work", secondary=works_authors, back_populates="authors")

class AuthorName(Base):
    __tablename__ = 'author_names'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    alt_name = Column(Text)
    
    # Relationships
    author = relationship("Author", back_populates="alt_names")

class Work(Base):
    __tablename__ = 'works'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    publisher = Column(Text)
    isbn = Column(BigInteger, unique=True)
    description = Column(Text)
    cover_url = Column(Text)
    
    # Relationships
    authors = relationship("Author", secondary=works_authors, back_populates="works")
    tags = relationship("Tag", secondary=works_tags, back_populates="works")
    copies = relationship("Copy", back_populates="work")

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True, nullable=False)
    info = Column(Text)
    join_date = Column(DateTime, nullable=False)
    
    # Relationships
    owned_copies = relationship("Copy", foreign_keys="Copy.owner_id", back_populates="owner")
    borrowed_copies = relationship("Copy", foreign_keys="Copy.lended_to", back_populates="borrower")

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey('tags.id'))
    type = Column(String(50), nullable=False)
    label = Column(Text, nullable=False)
    description = Column(Text)
    
    # Relationships
    parent = relationship("Tag", remote_side=[id], back_populates="children")
    children = relationship("Tag", back_populates="parent")
    works = relationship("Work", secondary=works_tags, back_populates="tags")

class Location(Base):
    __tablename__ = 'locations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey('locations.id'))
    name = Column(Text, nullable=False)
    description = Column(Text)
    type = Column(String(50), nullable=False)
    
    # Relationships
    parent = relationship("Location", remote_side=[id], back_populates="children")
    children = relationship("Location", back_populates="parent")
    copies = relationship("Copy", back_populates="location")

class Copy(Base):
    __tablename__ = 'copies'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    work_id = Column(Integer, ForeignKey('works.id'), nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    condition = Column(String(50))
    acquired = Column(DateTime(timezone=True), default=func.now)
    lended_to = Column(Integer, ForeignKey('users.id'))
    
    # Relationships
    work = relationship("Work", back_populates="copies")
    location = relationship("Location", back_populates="copies")
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_copies")
    borrower = relationship("User", foreign_keys=[lended_to], back_populates="borrowed_copies")


# Helper functions
def create_tables(engine):
    """Create all tables in the database"""
    Base.metadata.create_all(engine)

def get_works_by_author(session, author_name):
    """Get all works by an author (searching primary name and alt names)"""
    return session.query(Work).join(works_authors).join(Author).outerjoin(AuthorName).filter(
        (Author.primary_name.ilike(f'%{author_name}%')) | 
        (AuthorName.alt_name.ilike(f'%{author_name}%'))
    ).all()