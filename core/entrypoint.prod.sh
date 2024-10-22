#!/bin/bash
set -e

# Define color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to echo in green
echo_green() {
    echo -e "${GREEN}$1${NC}"
}

# Function to echo in red
echo_red() {
    echo -e "${RED}$1${NC}"
}

# Ensure DATABASE environment variable is set
if [ -z "$PGDB_NAME" ]; then
    echo_red "Error: DATABASE environment variable is not set."
    exit 1
fi


if [ "$PGDB_NAME" = "db_postgres" ]; then
    echo_green "Waiting for postgres..."

    # Wait for PostgreSQL to be available
    while ! nc -z $PGDB_HOST $PGDB_PORT; do
        sleep 0.1
    done

    echo_green "PostgreSQL started"
fi

# Running migrations
echo_green "Making the migrations..."
if python manage.py makemigrations; then
    echo_green "Migrations made successfully."
else
    echo_red "Error making migrations."
    exit 1
fi

# Applying migrations
echo_green "Applying the migrations..."
if python manage.py migrate; then
    echo_green "Migrations applied successfully."
else
    echo_red "Error applying migrations."
    exit 1
fi

# Collecting static files
echo_green "Collecting static files..."
if python manage.py collectstatic --noinput; then
    echo_green "Static files collected successfully."
else
    echo_red "Error collecting static files."
    exit 1
fi

# Starting Gunicorn
echo_green "Starting Gunicorn..."
exec gunicorn core.wsgi --bind 0.0.0.0:8000
