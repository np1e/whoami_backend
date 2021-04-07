import os
from dotenv import load_dotenv
load_dotenv(verbose=True)
basedir = os.path.abspath(os.path.dirname(__file__))

BCRYPT_LOG_ROUNDS = 12 # Configuration for the Flask-Bcrypt extension
MAIL_FROM_EMAIL = "admin@nhafkemeyer.com" # For use in application emails

# sqlalchemy settings
SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# Flask Admin UI settings
FLASK_ADMIN_SWATCH='cosmo'

# cors settings
CORS_HEADERS = 'application/json'


