import os
from dotenv import load_dotenv
load_dotenv(verbose=True)
basedir = os.path.abspath(os.path.dirname(__file__))

BCRYPT_LOG_ROUNDS = 12 # Configuration for the Flask-Bcrypt extension
MAIL_FROM_EMAIL = "admin@nhafkemeyer.com" # For use in application emails
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
FLASK_ADMIN_SWATCH='cosmo'
