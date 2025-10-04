from flask import Blueprint, request, current_app, g, jsonify,session
from sqlalchemy import query
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.models import db, User
from userServices import check_if_data_is_valid
from flask_login import login_required

bp = Blueprint('user', __name__)

@bp.route('/create_user', methods=['POST'])
def create_user():

    data = request.get_json()
    if check_if_data_is_valid(data):
        username = data.get('username')
        password = data.get('password')
        city_of_origin = data.get('city_of_origin')
        social_media_links = data.get('social_media_links', '')

        # Create new user
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password),
            city_of_origin=city_of_origin,
            social_media_links=social_media_links
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    else:
        return jsonify({'message': 'Invalid data or user already exists'}), 400


@bp.route('/login', methods=['POST'])
def login(data):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@login_required
@bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return  jsonify({'message': 'Logged out successfully'}), 200


@bp.route('/get_guides', methods=['GET'])
def get_guides():
    pass 