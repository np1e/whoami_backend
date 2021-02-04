export FLASK_APP="src"
export FLASK_ENV="development"

gunicorn --worker-class eventlet -w 1 "src:create_app()"
