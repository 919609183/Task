**Setup**

To set up the Flask Car Reports App, follow these steps:
Clone the repository from the provided public GitHub link.
Install the required dependencies using the command pip install -r requirements.txt.
Set up the necessary environment variables, such as FLASK_APP=app.py and FLASK_ENV=development.
Run the Flask development server using the command flask run. The server will start running locally on http://localhost:5000.

**Code Structure**

The code for the Flask Car Reports App is organized into the following files:
app/models.py: This file defines the application's database models using SQLAlchemy. It includes the User and Car models, representing users and car reports, respectively.

app/schemas.py: This file contains the Marshmallow schemas for validating input and output data. It includes the UserSchema for user data validation and the CarSchema for car report data validation.

app/tasks.py: This file defines the background task for periodically syncing the dataset from a remote source. It uses Celery to handle the background processing. The sync_dataset task retrieves data from the provided dataset URL and updates the local database with new or updated car reports.

app/views.py: This file contains the Flask routes and API endpoints for user authentication, car report search, and retrieval. It includes the auth and cars blueprints for organizing the routes.

**Functionality**

The Flask Car Reports App provides the following functionalities:
Sign-Up/Login Functionality: Users can register and log in to the application. The signup route allows users to register by providing a username and password. The login route validates the user's credentials and returns an authentication token.

Periodic Sync of Dataset: The application automatically syncs the dataset from a remote source once a day. This syncing process runs as a background task using Celery. The sync_dataset task retrieves the data from the provided dataset URL and updates the local database with new or updated car reports.

Search Functionality: The application provides an API endpoint (/api/cars) to search for car reports. Users can query the dataset based on the make, model, and make year of the car. The API returns paginated results based on the search criteria.

Schema Validation: The application properly validates input and output schemas using Marshmallow. The UserSchema validates the user registration and login data, while the CarSchema validates the car report data.
