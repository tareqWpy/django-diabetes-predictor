#!/bin/bash

# Execute commands in the Docker container
docker compose exec core bash -c "
    python manage.py makemigrations predictor &&
    python manage.py migrate
"

