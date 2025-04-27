#!/bin/sh

# Execute migrations and run the Django application
# Uses `0.0.0.0` to allow access from outside the container
python api/manage.py migrate & 
python api/manage.py runserver 0.0.0.0:8000
