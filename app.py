from app import app
from app.db import init_db
import click
from flask.cli import with_appcontext

if __name__=='__main__':
	app.run()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')