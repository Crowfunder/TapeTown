import datetime
import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy

# Here you can read about useful column types (Integer, String, DateTime, etc...):
# https://docs.sqlalchemy.org/en/20/core/type_basics.html#generic-camelcase-types

# Here you can read about relationships between models:
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
# https://stackoverflow.com/questions/3113885/difference-between-one-to-many-many-to-one-and-many-to-many

# Here you can read about using models defined below to work
# with the database (creating rows, selecting rows, deleting rows, etc...):
# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/queries/



db = SQLAlchemy()
from dataclasses import dataclass

@dataclass
class temp(db.Model):
    __tablename__ = ''

    Id = db.Column(db.Integer, primary_key=True)

@dataclass
class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    city_of_origin = db.Column(db.String(120), nullable=False)
    # is_local_guide = db.Column(db.Boolean, default=False)
    social_media_links = db.Column(db.String(400), nullable=True)

    user = relationship("User", back_populates="Guides",lazy=True)