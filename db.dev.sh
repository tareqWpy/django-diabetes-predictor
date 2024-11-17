#!/bin/bash

# Execute commands in the Docker container
docker compose exec backend bash -c "
    python manage.py makemigrations accounts &&
    python manage.py makemigrations predictor &&
    python manage.py makemigrations referral &&
    python manage.py migrate &&
    python manage.py insert_data -s True 
"

