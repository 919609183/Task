import requests
from flask import Flask
from celery import Celery
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json'
)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    year = db.Column(db.Integer)
    category = db.Column(db.Text)

    def __init__(self, make, model, year, category):
        self.make = make
        self.model = model
        self.year = year
        self.category = category

@celery.task
def sync_dataset():
    headers = {
        'X-Parse-Application-Id': 'gP38fEGPgSSBvvO4Kz9McQD2UpUrcpIlrXDyHLWc',
        'X-Parse-REST-API-Key': '72gJMaTFClPr90oA7bkRYdUy0PJIcKQ8tj8bQvtP'
    }

    url = 'https://parseapi.back4app.com/classes/Car_Model_List'  # Replace with the actual URL

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Assuming the response JSON is a list of car objects
        for car_data in data:
            make = car_data['Make']
            model = car_data['Model']
            year = car_data['Year']
            category = car_data['Category']

            # Check if the car data already exists in the database
            existing_car = Car.query.filter_by(make=make, model=model, year=year).first()
            if existing_car:
                # Update the existing car data
                existing_car.category = category
            else:
                # Create a new car entry
                car = Car(make=make, model=model, year=year, category=category)
                db.session.add(car)
        
        db.session.commit()
    else:
        print(f'Error retrieving data: {response.status_code}')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    celery.start()
    app.run()
