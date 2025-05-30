# Home library application
# Copyright (C) 2025  TheCosmicAspect

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from flask import Flask
from models import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from routes.main import main_bp
    from routes.books import books_bp
    from routes.authors import authors_bp
    from routes.tags import tags_bp
    from routes.locations import locations_bp
    from routes.places import places_bp
    from routes.owners import owners_bp
    from routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(authors_bp, url_prefix='/authors')
    app.register_blueprint(tags_bp, url_prefix='/tags')
    app.register_blueprint(locations_bp, url_prefix='/locations')
    app.register_blueprint(places_bp, url_prefix='/places')
    app.register_blueprint(owners_bp, url_prefix='/owners')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)