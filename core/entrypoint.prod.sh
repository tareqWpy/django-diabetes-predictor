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
    # Only check for environment variables and PostgreSQL if the role is backend or celery-worker
    if [ "$ROLE" == "backend" ]; then
        wait_for_postgres
    fi

    case "$ROLE" in
        backend)
            echo_green "Creating and applying migrations..."
            python manage.py makemigrations && python manage.py migrate

            echo_green "Collecting static files..."
            python manage.py collectstatic --noinput

            echo_green "Starting Gunicorn server..."
            exec gunicorn core.wsgi --bind 0.0.0.0:8000
            ;;
        *)
            echo_red "Error: Unknown ROLE specified: $ROLE"
            exit 1
            ;;
    esac
}

# Run the main function
main "$@"
