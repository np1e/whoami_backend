export FLASK_APP="src"
export FLASK_ENV="development"

if [ "$1" == "--g" ]; then
  echo "Starting gunicorn..."
  gunicorn --worker-class eventlet -w 1 "src:create_app()"
else
  echo "Starting Flask development server..."
  flask run --host=0.0.0.0
fi
