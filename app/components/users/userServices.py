from app.database.models import  User
from sqlalchemy import query
from app.components.users.userConfig import DEFAULT_PROFILE_URL

def check_if_data_is_valid(data):
    #checking if all requaired fields are here
    required_fields = ['username', 'password', 'city_of_origin']
    for field in required_fields:
        if field not in data or not data[field]:
            return False        

    #setting default profile url in absence of custom one
    if data.get('profile_url') is None:
        data['profile_url'] = DEFAULT_PROFILE_URL

        # Check if user already exists
    existing_user = User.query.filter_by(username=data.get('username')).first()
    if existing_user:
        return False
    
    return True