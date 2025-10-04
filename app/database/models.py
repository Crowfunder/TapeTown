import datetime as dt
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
class FileBlob(db.Model):
    __tablename__ = 'files'

    file_hash: str = db.Column(db.String, primary_key=True)
    file_path: str = db.Column(db.String)


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

## db for Guides 
@dataclass
class GuidesRecord(db.Model):
    __tablename__ = "guides_record"

    # primary key
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name: str = db.Column(db.String(200), nullable=False)
    thumbnail_url: str = db.Column(db.String(500), nullable=False)
    # audio_url: str = db.Column(db.String(500), nullable=False)
    audio_hash: str = db.Column(db.String(500), nullable=False)
    image_hash: str = db.Column(db.String(500), nullable=False)

    user_id: int = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    user = db.relationship("User", back_populates="guides_record")

    likes: int = db.Column(db.Integer, nullable=False, default=0)

    latitude: float | None = db.Column(db.Float, nullable=True)
    longitude: float | None = db.Column(db.Float, nullable=True)

    created_at: dt.datetime = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    __table_args__ = (
        #likes >= 0
        sa.CheckConstraint("likes >= 0", name="ck_likes_nonneg"),
        #dozwolone zakresy geolokalizacji lub oba NULL
        sa.CheckConstraint(
            "(latitude IS NULL AND longitude IS NULL) OR "
            "(latitude BETWEEN -90 AND 90 AND longitude BETWEEN -180 AND 180)",
            name="ck_geo_ranges"
        ),
        #jeden użytkownik nie może mieć dwóch rekordów o tej samej nazwie
        sa.UniqueConstraint("user_id", "name", name="uq_user_name"),
        #pomocniczy indeks
        sa.Index("ix_audio_likes", "likes"),
    )

@dataclass
class GuidesRating(db.Model):
    __tablename__ = "guides_rating"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guide_id: int = db.Column(
        db.Integer, db.ForeignKey("guides_record.id"), nullable=False, index=True
    )
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, index=True
    )
    rating: int = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        sa.CheckConstraint("rating BETWEEN 0 AND 5", name="ck_rating_range"),
        sa.UniqueConstraint("guide_id", "user_id", name="uq_rating_user_guide"),
    )
