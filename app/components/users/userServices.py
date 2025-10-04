from app.components.file_storage.fsController import file_get
from app.database.models import  User
from sqlalchemy import select
from app.components.file_storage.fsService import fs_get, fs_post

def check_if_data_is_valid(data):
    #checking if all requaired fields are here
    required_fields = ['username', 'password', 'city_of_origin']
    for field in required_fields:
        if field not in data or not data[field]:
            return False        

        # Check if user already exists
    existing_user = User.query.filter_by(username=data.get('username')).first()
    if existing_user:
        return False
    
    return True

def manage_picture_upload(profile_picture):
    picture_hash = fs_post(profile_picture)
    return fs_get(picture_hash)