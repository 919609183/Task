import os

# Set the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration options
SECRET_KEY = 'your_secret_key'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
