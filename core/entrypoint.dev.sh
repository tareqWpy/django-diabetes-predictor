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

# Main script execution
main() {

    case "$ROLE" in
        backend)
            echo_green "Creating and applying migrations..."
            python manage.py makemigrations && python manage.py migrate

            echo_green "Starting server..."
            exec python manage.py runserver 0.0.0.0:8000
            ;;
        *)
            echo_red "Error: Unknown ROLE specified: $ROLE"
            exit 1
            ;;
    esac
}

# Run the main function
main "$@"