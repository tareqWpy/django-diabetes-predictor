#!/bin/bash
set -euo pipefail  # Exit on errors, undefined variables, or failed pipelines

# Define color codes for output formatting
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print messages in green
echo_green() {
    echo -e "${GREEN}$1${NC}"
}

# Function to print messages in red
echo_red() {
    echo -e "${RED}$1${NC}"
}

# Function to check if required environment variables are set
check_env_vars() {
    [[ -v PGDB_NAME ]] || { echo_red "Error: DATABASE environment variable (PGDB_NAME) is not set."; exit 1; }
    [[ -v PGDB_HOST ]] || { echo_red "Error: HOST environment variable (PGDB_HOST) is not set."; exit 1; }
    [[ -v PGDB_PORT ]] || { echo_red "Error: PORT environment variable (PGDB_PORT) is not set."; exit 1; }
}

# Function to wait for PostgreSQL to be available
wait_for_postgres() {
    echo_green "Waiting for PostgreSQL..."
    until nc -z "$PGDB_HOST" "$PGDB_PORT"; do
        sleep 0.1
    done
    echo_green "PostgreSQL is up and running!"
}

# Main script execution
main() {
    check_env_vars
    wait_for_postgres

    case "$ROLE" in
        backend)
            echo_green "Creating and applying migrations..."
            python manage.py makemigrations && python manage.py migrate

            echo_green "Collecting static files..."
            python manage.py collectstatic --noinput

            echo_green "Starting Gunicorn server..."
            exec gunicorn core.wsgi --bind 0.0.0.0:8000

            ;;
        celery-worker)
            echo_green "Starting Celery worker..."
            exec celery -A core worker --loglevel=info

            ;;
        celery-beat)
            echo_green "Starting Celery beat..."
            exec celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

            ;;
        *)
            echo_red "Error: Unknown ROLE specified: $ROLE"
            exit 1
            ;;
    esac
}

# Run the main function
main "$@"

