# home-library
## IMPORTANT
This project is a work in progress. Many features are incomplete.
Full transparency: most everything is written by me with *some* LLM assistance in places to speed up development. Any JS is entirely AI-generated though. I'm not good with JS.
## Summary
This project gives the user an easy way to manage their books through its many features, such as storing book locations, custom tags for genres and types, and owners for families or other applications. It is intended to be hosted on a small computer that can be left running without intervention. As of right now, its scope extends only to home uses, but may be expanded for home libraries in the future.
## Installation
As this is still under development, detailed installation instructions are not given. For those who wish to brave the installation, see below:
- Install postgresql on the host
- Set up a database with the schema provided by [db.sql](db.sql)
- Download the files in [src/](src/) to the desired directory
- Install the required libraries with `pip install flask flask-sqlalchemy dotenv psycop2 config flask-wtf requests`
- Run `python app.py` and connect locally
**Congrats! If you know how to do that, you're all set!**
## Anything else?
If I missed something important, let me know over discord (@thecosmicaspect). Else, hold on. This will be finished soon.
