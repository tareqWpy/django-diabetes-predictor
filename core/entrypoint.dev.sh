set -e

echo "Making the migrations..."
python manage.py makemigrations --noinput

echo "Applying the migrations..."
python manage.py migrate --noinput

echo "Starting the server..."
exec python manage.py runserver 0.0.0.0:8000