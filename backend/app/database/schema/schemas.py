from marshmallow import Schema, fields, EXCLUDE, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from backend.app.database.models import GuidesRecord

class GuideOutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GuidesRecord
        load_instance = False
        include_fk = True
        fields = ("name", "user_id", "likes", "created_at", "audio_hash", "image_hash")
    # Możesz jawnie wskazać tylko potrzebne pola:
    # fields = ("id","name","latitude","longitude","audio_url","thumbnail_url")

guide_out_many = GuideOutSchema(many=True)
guide_out_one = GuideOutSchema()
