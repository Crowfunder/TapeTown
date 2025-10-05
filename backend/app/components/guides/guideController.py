# controllers/guides_controller.py
from __future__ import annotations
from backend.app.app import db
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, Forbidden, NotFound
from backend.app.database.schema.schemas import guide_out_many
from backend.app.components.file_storage.fsService import fs_get, fs_post

from backend.app.components.file_storage.fsService import *
from backend.app.database.models import GuidesRating, GuidesRecord
from backend.app.database.schema.schemas import guide_out_one
from backend.app.components.guides.guideService import (
    add_guide, remove_guide,
    get_recommended_guides, add_rating
)

bp = Blueprint("guides", __name__, url_prefix="/api/guides")


@bp.delete("/<int:guide_id>")
def api_remove_guide(guide_id: int):
    by_user_id = request.args.get("by_user_id", type=int)
    try:
        ok = remove_guide(guide_id, by_user_id=by_user_id)
    except PermissionError as e:
        raise Forbidden(str(e))
    if not ok:
        raise NotFound("Guide not found.")
    return "", 204

# POST /api/guides/<id>/report -> report guide, return report id
# @bp.post("/<int:guide_id>/report")
# def api_report_guide(guide_id: int):
#     data = request.get_json(silent=True) or {}
#     reason = data.get("reason")
#     reporter = data.get("user_id")
#     if not reason:
#         raise BadRequest("Field 'reason' is required.")
#     report_id = report_guide(guide_id, reason=reason, reporter_user_id=reporter)
#     return jsonify({"report_id": report_id}), 201

@bp.get("/<int:guide_id>")
def get_guide(guide_id: int):
    guide = GuidesRecord.query.get(guide_id)
    if guide is None:
        return jsonify({"error": "Guide nie istnieje"}), 404

    data = guide_out_one.dump(guide)
    return jsonify(data), 200

# GET /api/guides/recommended?lat=&lon=&radius_km=&limit=
# return only list of ids
@bp.get("/recommended")
def api_get_recommended():
    lat = request.args.get("latitude", type=float)
    lon = request.args.get("longitude", type=float)
    radius = request.args.get("radius_km", default=10.0, type=float)
    limit = request.args.get("limit", default=20, type=int)
    if lat is None or lon is None:
        raise BadRequest("Query params 'latitude' and 'longitude' are required.")

    guides = get_recommended_guides(lat, lon, radius_km=radius, limit=limit)  # lista ORM
    return jsonify(guide_out_many.dump(guides)), 200

@bp.post("/<int:guide_id>/rating")
def api_add_rating(guide_id: int):
    rating = int(request.form.get("rating"))
    user_id = request.form.get("user_id")

    if user_id is None or rating is None:
        raise BadRequest("Fields 'user_id' (int) and 'rating' (1..5) are required.")

    try:
        result = add_rating(guide_id=guide_id, user_id=user_id, value=rating)
    except ValueError as e:
        raise BadRequest(str(e))

    return jsonify(result), 201

@bp.get("/<int:guide_id>/rating")
def api_get_rating(guide_id: int):
    guide = GuidesRecord.query.get(guide_id)
    if guide is None:
        raise NotFound("Guide not found.")
    # average rating and count
    avg_rating = db.session.query(db.func.avg(GuidesRating.rating)).filter_by(guide_id=guide_id).scalar()
    count = db.session.query(db.func.count(GuidesRating.id)).filter_by(guide_id=guide_id).scalar()
    return jsonify({
        "avg": float(avg_rating) if avg_rating is not None else None,
        "count": count
    }), 200

@bp.post("/upload")
def api_add_guide():
    audio = request.files.get("file")
    if audio is None or audio.filename == "":
        return {"error": "No audio file provided"}, 400

    image = request.files.get("image") or request.files.get("thumbnail")
    if image is None or image.filename == "":
        return {"error": "No image file provided"}, 400

    name = request.form.get("name")
    user_id = request.form.get("user_id", type=int)
    lat = request.form.get("latitude", type=float)
    lon = request.form.get("longitude", type=float)

    missing = [k for k, v in {
        "name": name, "user_id": user_id, "latitude": lat, "longitude": lon
    }.items() if v in (None, "")]
    if missing:
        return {"error": f"Missing fields: {', '.join(missing)}"}, 400

    audio_hash = fs_post(audio)
    image_hash = fs_post(image)

    guide = GuidesRecord(
        name=name,
        user_id=user_id,
        latitude=lat,
        longitude=lon,
        audio_hash=audio_hash,
        image_hash=image_hash,
    )

    db.session.add(guide)
    db.session.commit()
    return jsonify({"id": guide.id}), 200

