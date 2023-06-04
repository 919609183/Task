from flask import Blueprint, request, jsonify
from app.models import db, User
from app.schemas import UserSchema

auth = Blueprint('auth', __name__)
cars = Blueprint('cars', __name__)

@auth.route('/signup', methods=['POST'])
def signup():
    schema = UserSchema()

    try:
        user_data = schema.load(request.json)
    except Exception as e:
        return jsonify({'message': 'Invalid input', 'errors': str(e)}), 400

    # Check if username already exists
    if User.query.filter_by(username=user_data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400

    # Create new user
    user = User(username=user_data['username'], password=user_data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth.route('/login', methods=['POST'])
def login():
    schema = UserSchema()

    try:
        user_data = schema.load(request.json)
    except Exception as e:
        return jsonify({'message': 'Invalid input', 'errors': str(e)}), 400

    user = User.query.filter_by(username=user_data['username']).first()

    if not user or user.password != user_data['password']:
        return jsonify({'message': 'Invalid username or password'}), 401


@cars.route('/api/cars', methods=['GET'])
def get_reports():
    make = request.args.get('make', None)
    model = request.args.get('model', None)
    make_year = request.args.get('make_year', None)

    # Create the base query
    query = db.session.query(Car)

    # Apply filters based on query parameters
    if make:
        query = query.filter(Car.make == make)
    if model:
        query = query.filter(Car.model == model)
    if make_year:
        query = query.filter(Car.make_year == make_year)

    # Perform pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated_query = query.paginate(page, per_page, error_out=False)

    # Serialize the cars
    cars_schema = CarSchema(many=True)
    cars_data = cars_schema.dump(paginated_query.items)

    # Prepare the response data
    response = {
        'cars': cars_data,
        'total_pages': paginated_query.pages,
        'current_page': paginated_query.page,
        'total_records': paginated_query.total,
        'per_page': per_page
    }

    return jsonify(response), 200

    return jsonify(cars), 200
