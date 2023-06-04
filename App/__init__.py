from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load configuration from config.py
app.config.from_object('config')

# Initialize database
db = SQLAlchemy(app)

# Import models to create tables
from app.models import User
db.create_all()

# Import views (routes)
from app.views import auth, reports
app.register_blueprint(auth)
app.register_blueprint(reports)

if __name__ == '__main__':
    app.run()
