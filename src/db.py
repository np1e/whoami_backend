from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from alembic import op

db = SQLAlchemy()
migrate = Migrate()

def get_db():
    return db.session

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

def create_tables():
    db.create_all()