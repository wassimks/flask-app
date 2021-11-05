# import sqlite3
# import  click
# from flask import g, current_app
# from flask.cli import with_appcontext

# def get_db():
#     if 'db' not in g :
#         g.db = sqlite3.connect(
#             current_app.config['SECRET_KEY']
#             , current_app.config['SQLALCHEMY_DATABASE_URI']
#             , detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row
#     return g.db

# def close_db():
#     db = g.pop('db', None)
#     if db is not None:
#         db.close()

# def init_db():
#     db = get_db()
#     with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))

