# home-library
## IMPORTANT
This project is a work in progress. Many features are incomplete.
## Summary
This project gives the user an easy way to manage their books through its many features, such as storing book locations, custom tags for genres and types, and owners for families or other applications. It is intended to be hosted on a small computer that can be left running without intervention. As of right now, its scope extends only to home uses, but may be expanded for home libraries in the future.
## Installation
As this is still under development, detailed installation instructions are not given. For those who wish to brave the installation, see below:
- Install postgresql on the host
- Set up a database with the schema provided by [db.sql](db.sql)
- Download the files in [src/](src/) to the desired directory
- Install the required libraries with `pip install flask flask-sqlalchemy dotenv psycopg2 config flask-wtf requests`
- Create a `.env` file in `src/` with the following information:
```
FLASK_APP=app.py
FLASK_ENV=production
DATABASE_URL=postgresql://{username}:{password}@localhost:{port}/{database name}
SECRET_KEY={type a whole bunch of random characters here}
```
- Run `python app.py` and connect locally
**Congrats! If you know how to do that, you're all set!**