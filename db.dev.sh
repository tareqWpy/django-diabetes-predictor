#!/bin/bash

# Execute commands in the Docker container
docker compose exec backend bash -c "
    python manage.py makemigrations predictor &&
    python manage.py migrate
"

