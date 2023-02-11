#!/bin/bash
cd ..
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata test.json
python test_data/add_image.py