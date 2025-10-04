# controllers/guides_controller.py
from app.app import db
from __future__ import annotations
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, Forbidden, NotFound

from models import GuidesRecord
from services.guides_service import (
    add_guide, remove_guide, report_guide,
    get_audio_for_guide, get_recommended_guides, add_rating
)

guides_bp = Blueprint("guides", __name__)

# POST /api/guides -> add guide, return only new id
@guides_bp.post("/")
def api_add_guide():
    data = request.get_json(silent=True) or {}
    try:
        g = add_guide(data)
        return jsonify({"id": g.id}), 201
    except ValueError as e:
        raise BadRequest(str(e))

@guides_bp.delete("/<int:guide_id>")
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
@guides_bp.post("/<int:guide_id>/report")
def api_report_guide(guide_id: int):
    data = request.get_json(silent=True) or {}
    reason = data.get("reason")
    reporter = data.get("user_id")
    if not reason:
        raise BadRequest("Field 'reason' is required.")
    report_id = report_guide(guide_id, reason=reason, reporter_user_id=reporter)
    return jsonify({"report_id": report_id}), 201

# GET /api/guides/<id>/audio -> return only audio url
@guides_bp.get("/<int:guide_id>/audio")
def api_get_audio_for_guide(guide_id: int):
    url = get_audio_for_guide(guide_id)
    if not url:
        raise NotFound("Guide not found.")
    return jsonify({"audio_url": url})

# GET /api/guides/recommended?lat=&lon=&radius_km=&limit=
# return only list of ids
@guides_bp.get("/recommended")
def api_get_recommended():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    radius = request.args.get("radius_km", default=10.0, type=float)
    limit = request.args.get("limit", default=20, type=int)

    if lat is None or lon is None:
        raise BadRequest("Query params 'lat' and 'lon' are required.")

    guides = get_recommended_guides(lat, lon, radius_km=radius, limit=limit)
    return jsonify({
        "ids": [g.id for g in guides],
        "count": len(guides),
    })

# POST /api/guides/<id>/rating -> add/update rating, return aggregate numbers
@guides_bp.post("/<int:guide_id>/rating")
def api_add_rating(guide_id: int):
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    value = data.get("value")
    if not isinstance(user_id, int) or not isinstance(value, int):
        raise BadRequest("Fields 'user_id' (int) and 'value' (1..5) are required.")
    try:
        agg = add_rating(guide_id, user_id, value)  # {"guide_id", "count", "avg"}
        return jsonify(agg), 201
    except ValueError as e:
        raise BadRequest(str(e))

@guides_bp.post("/upload")
def api_add_guide():
    if 'file' not in request.files:
        return {'error': 'No file part in the request'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    
    name = request.form.get("name")
    user_id = request.form.get("user_id", type=int)
    lat = request.form.get("latitude", type=float)
    lon = request.form.get("longitude", type=float)

    file_hash = fs_upload(file)

    guide = GuidesRecord(
        name = name,
        user_id = user_id,
        latitude = lat,
        longitude = lon,
        audio_hash = file_hash,
        )

    db.session.add(guide)
    db.session.commit()

