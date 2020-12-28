
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import click

db = SQLAlchemy()
migrate = Migrate()

def get_db():
    return db.session

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)