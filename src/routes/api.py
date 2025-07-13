from flask import Blueprint, request, jsonify
from models import db
from models.models import Work, Copy, Author, Tag, Location
from sqlalchemy import or_, cast, String
import requests

api_bp = Blueprint('api', __name__)

@api_bp.route('/books')
def api_books():
    books = Book.query.all()
    book_list = []
    
    for book in books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'isbn': book.isbn,
            'location': book.location.name if book.location else None,
            'description': book.description,
            'authors': [{'id': a.id, 'name': a.name} for a in book.authors],
            'tags': [{'id': t.id, 'label': t.label} for t in book.tags]
        }
        book_list.append(book_data)
    
    return {'books': book_list}

@api_bp.route('/search')
def api_search():
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'books': []})
    
    try:
        print(f"Search query: '{query}'")
        
        search_conditions = []
        
        # Direct field searches with proper casting
        search_conditions.extend([
            Book.title.ilike(f'%{query}%'),
            cast(Book.isbn, String).ilike(f'%{query}%'),
            Book.description.ilike(f'%{query}%')
        ])
        
        # Relationship searches
        search_conditions.extend([
            Book.authors.any(Author.name.ilike(f'%{query}%')),
            Book.tags.any(Tag.label.ilike(f'%{query}%')),
            Book.location.has(Location.name.ilike(f'%{query}%'))
        ])
        
        # Combine with OR
        search_filter = or_(*search_conditions)
        
        books = Book.query.filter(search_filter).all()
        print(f"Found {len(books)} books")
        
        book_list = []
        for book in books:
            try:
                book_data = {
                    'id': book.id,
                    'title': book.title or '',
                    'isbn': book.isbn or '',
                    'description': book.description or '',
                    'cover_url': book.cover_url or '',
                    'authors': [{'id': a.id, 'name': a.name} for a in (book.authors or [])],
                    'tags': [{'id': t.id, 'label': t.label} for t in (book.tags or [])],
                    'location': {'id': book.location.id, 'name': book.location.name} if book.location else None
                }
                book_list.append(book_data)
            except Exception as e:
                print(f"Error processing book {book.id}: {e}")
                continue
        
        print(f"Returning {len(book_list)} processed books")
        return jsonify({'books': book_list})
        
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({'error': str(e), 'books': []}), 500

@api_bp.route('/isbn-lookup/<isbn>')
def isbn_lookup(isbn):
    """Look up book information by ISBN"""
    try:
        # Try Google Books API first
        google_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
        response = requests.get(google_url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('items'):
                book = data['items'][0]['volumeInfo']
                return jsonify({
                    'success': True,
                    'title': book.get('title', ''),
                    'authors': book.get('authors', []),
                    'description': book.get('description', ''),
                    'cover_url': book.get('imageLinks', {}).get('thumbnail', '').replace('http:', 'https:'),
                    'categories': book.get('categories', [])
                })
        
        # Fallback to Open Library
        openlibrary_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        response = requests.get(openlibrary_url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            book_key = f"ISBN:{isbn}"
            if data.get(book_key):
                book = data[book_key]
                return jsonify({
                    'success': True,
                    'title': book.get('title', ''),
                    'authors': [a['name'] for a in book.get('authors', [])],
                    'description': book.get('notes', '') or book.get('subtitle', ''),
                    'cover_url': book.get('cover', {}).get('medium', ''),
                    'categories': [s['name'] for s in book.get('subjects', [])]
                })
        
        return jsonify({'success': False, 'error': 'Book not found'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
@api_bp.route('/authors', methods=['POST'])
def create_author():
    """Create a single author"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        bio = data.get('bio', '').strip()
        
        if not name:
            return jsonify({'success': False, 'message': 'Author name is required'}), 400
        
        # Check if author already exists
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author:
            return jsonify({'success': False, 'message': 'Author already exists'}), 400
        
        # Create new author
        author = Author(name=name, bio=bio if bio else None)
        db.session.add(author)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'author': {
                'id': author.id,
                'name': author.name,
                'bio': author.bio
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/authors/batch', methods=['POST'])
def create_authors_batch():
    """Create multiple authors at once"""
    try:
        data = request.get_json()
        authors_data = data.get('authors', [])
        
        if not authors_data:
            return jsonify({'success': False, 'message': 'No authors provided'}), 400
        
        created_authors = []
        
        for author_data in authors_data:
            name = author_data.get('name', '').strip()
            bio = author_data.get('bio', '').strip()
            
            if not name:
                continue  # Skip empty names
            
            # Check if author already exists
            existing_author = Author.query.filter_by(name=name).first()
            if existing_author:
                # Add existing author to results
                created_authors.append({
                    'id': existing_author.id,
                    'name': existing_author.name,
                    'bio': existing_author.bio
                })
                continue
            
            # Create new author
            author = Author(name=name, bio=bio if bio else None)
            db.session.add(author)
            db.session.flush()  # Flush to get the ID
            
            created_authors.append({
                'id': author.id,
                'name': author.name,
                'bio': author.bio
            })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'authors': created_authors
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/tags', methods=['POST'])
def create_tag():
    """Create a single tag"""
    try:
        data = request.get_json()
        label = data.get('label', '').strip()
        description = data.get('description', '').strip()
        
        if not label:
            return jsonify({'success': False, 'message': 'Tag label is required'}), 400
        
        # Check if tag already exists
        existing_tag = Tag.query.filter_by(label=label).first()
        if existing_tag:
            return jsonify({'success': False, 'message': 'Tag already exists'}), 400
        
        # Create new tag
        tag = Tag(label=label, description=description if description else None)
        db.session.add(tag)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'tag': {
                'id': tag.id,
                'label': tag.label,
                'description': tag.description
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/tags/batch', methods=['POST'])
def create_tags_batch():
    """Create multiple tags at once"""
    try:
        data = request.get_json()
        tags_data = data.get('tags', [])
        
        if not tags_data:
            return jsonify({'success': False, 'message': 'No tags provided'}), 400
        
        created_tags = []
        
        for tag_data in tags_data:
            label = tag_data.get('label', '').strip()
            description = tag_data.get('description', '').strip()
            
            if not label:
                continue  # Skip empty labels
            
            # Check if tag already exists
            existing_tag = Tag.query.filter_by(label=label).first()
            if existing_tag:
                # Add existing tag to results
                created_tags.append({
                    'id': existing_tag.id,
                    'label': existing_tag.label,
                    'description': existing_tag.description
                })
                continue
            
            # Create new tag
            tag = Tag(label=label, description=description if description else None)
            db.session.add(tag)
            db.session.flush()  # Flush to get the ID
            
            created_tags.append({
                'id': tag.id,
                'label': tag.label,
                'description': tag.description
            })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'tags': created_tags
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500