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
class temp(db.Model):
    __tablename__ = ''

    Id = db.Column(db.Integer, primary_key=True)

## db for Guides 
@dataclass
class GuideRecord(db.Model):
    __tablename__ = "GuidesRecord"

    # primary key
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name: str = db.Column(db.String(200), nullable=False)
    thumbnail_url: str = db.Column(db.String(500), nullable=False)
    audio_url: str = db.Column(db.String(500), nullable=False)
    location: str | None = db.Column(db.String(200), nullable=True)

    user_id: int = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    user = db.relationship("User", back_populates="GuidesRecord")

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