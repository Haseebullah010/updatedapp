# image-detection-django-backend

Image Detection Backend

# Bulit with

- Django
- DRF
- Yolov5

# How to use

- Clone this repo
- Make python virtual environment and activate it
- Run command **pip -r requirements_macos_win.txt** If you are using MacOs or Windows Otherwise run **pip -r requirements.txt**
- Make .env file in this project root directory with DEBUG=1 and SECRET_KEY=anything_you_want
- Run command python manage.py runserver from this project root directory
- Your app would be served on http://localhost:8000

# Image detection endpoint

- Endpoint is http://localhost:8000/polls/ Request is POST
- POST your image with "file" key on this endpoint
