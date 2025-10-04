from flask import Blueprint, request, current_app, g, jsonify,session
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.models import db, User, GuidesRecord
from .userServices import check_if_data_is_valid, manage_picture_upload
from flask_login import login_required
from app.database.schema.schemas import guide_out_many

bp = Blueprint('user', __name__, url_prefix="/api/users")

@bp.route('/create_user', methods=['POST'])
def create_user():
    if check_if_data_is_valid():
        username = request.form.get('username')
        password = request.form.get('password')
        profile_picture = request.form.get('profile_picture')
        city_of_origin = request.form.get('city_of_origin')
        social_media_links = request.form.get('social_media_links')

        profile_url = manage_picture_upload(profile_picture)

        # Create new user
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password),
            city_of_origin=city_of_origin,
            social_media_links=social_media_links,
            profile_picture=profile_url
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 200
    else:
        return jsonify({'message': 'Invalid data or user already exists'}), 400


@bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return jsonify({'message': 'No input data provided'}), 400

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.user_id
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
    user_id = session.get('user_id')
    guidesRecord = GuidesRecord.query.filter_by(user_id=user_id).all()
    return jsonify(guide_out_many.dump(guidesRecord)), 200