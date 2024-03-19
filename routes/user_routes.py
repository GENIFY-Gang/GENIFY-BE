# user_routes.py
from flask import Blueprint, jsonify, request
from models import db, User
import jwt
import datetime
from flask_jwt_extended import create_access_token
import datetime
import hashlib

users_bp = Blueprint('users', __name__, url_prefix='/user')

@users_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    # Check if the user with the given username or email already exists
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({'error': 'Username or email already exists'}), 400

    # Create a new user
    user = User(username=username, email=email, password=password, role=role)
    db.session.add(user)
    db.session.commit()

    # Generate a JWT token for the registered user
    access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(days=1))

    return jsonify({'message': 'User registered successfully', 'access_token': access_token, 'role': role})

@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Find the user with the given username
    user = User.query.filter_by(username=username).first()

    # Check if the user exists and the password is correct
    if user and user.password == password:
        # Generate a JWT token for the logged-in user
        access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(days=1))
        return jsonify({'message': 'Login successful', 'access_token': access_token, 'role': user.role, 'email':user.email})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'], password=data['password'], role=data['role'], )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])