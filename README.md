# Social media API
API service for social media platform written in DRF

## Description
This project is a social media API built using Django Rest Framework (DRF). It provides a backend service for a social media platform where users can create profiles, follow other users, create posts, like and comment on posts, and manage their interactions. The API supports JWT authentication for secure access and includes comprehensive documentation generated with drf-spectacular.

The project is structured to support scalability and maintainability, with separate apps for user management and social media functionalities. It also includes an admin panel for managing the data and a debug toolbar for development purposes.

## Installing using GitHub
- git clone https://github.com/Serhii-Chubur/social-media-api
- cd social-media-api
- python -m venv venv
- venv/bin/activate
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py loaddata data.json
- python manage.py runserver

## Getting access
- Create user: user/register
- Get access token: user/token
- Get info about user: user/me

## Key features include:
- User registration and JWT authentication
- Profile management
- Creating, updating, and deleting posts
- Liking and commenting on posts
- Following and unfollowing users
- Filtering and searching for posts and profiles
- Admin panel for data management
- API documentation with Swagger and Redoc

## DB structure
![DB structure][def]

[def]: ./db_diagram.jpg
