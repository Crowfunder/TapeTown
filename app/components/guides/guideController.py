# controllers/guides_controller.py
from __future__ import annotations
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, Forbidden, NotFound

from models import GuideRecord
from services.guides_service import (
    add_guide, remove_guide, report_guide,
    get_audio_for_guide, get_recommended_guides, add_rating
)

guides_bp = Blueprint("guides", __name__)

def _serialize(g: GuideRecord) -> dict:
    return {
        "id": g.id,
        "name": g.name,
        "thumbnail_url": g.thumbnail_url,
        "audio_url": g.audio_url,
        "location": g.location,
        "user_id": g.user_id,
        "likes": g.likes,
        "latitude": g.latitude,
        "longitude": g.longitude,
        "created_at": g.created_at.isoformat() if g.created_at else None,
    }

# POST /api/guides -> add guide
@guides_bp.post("/")
def api_add_guide():
    data = request.get_json(silent=True) or {}
    try:
        g = add_guide(data)
        return jsonify(_serialize(g)), 201
    except ValueError as e:
        raise BadRequest(str(e))

# DELETE /api/guides/<id> -> remove guide (optional ?by_user_id=...)
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

# POST /api/guides/<id>/report -> report guide
@guides_bp.post("/<int:guide_id>/report")
def api_report_guide(guide_id: int):
    data = request.get_json(silent=True) or {}
    reason = data.get("reason")
    reporter = data.get("user_id")
    if not reason:
        raise BadRequest("Field 'reason' is required.")
    rep_id = report_guide(guide_id, reason=reason, reporter_user_id=reporter)
    return jsonify({"report_id": rep_id}), 201

# GET /api/guides/<id>/audio -> get audio url for guide
@guides_bp.get("/<int:guide_id>/audio")
def api_get_audio_for_guide(guide_id: int):
    url = get_audio_for_guide(guide_id)
    if not url:
        raise NotFound("Guide not found.")
    return jsonify({"guide_id": guide_id, "audio_url": url})

# GET /api/guides/recommended?lat=..&lon=..&radius_km=&limit=
@guides_bp.get("/recommended")
def api_get_recommended():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    radius = request.args.get("radius_km", default=10.0, type=float)
    limit = request.args.get("limit", default=20, type=int)

    if lat is None or lon is None:
        raise BadRequest("Query params 'lat' and 'lon' are required.")

    guides = get_recommended_guides(lat, lon, radius_km=radius, limit=limit)
    return jsonify([_serialize(g) for g in guides])

# POST /api/guides/<id>/rating -> add/update rating
@guides_bp.post("/<int:guide_id>/rating")
def api_add_rating(guide_id: int):
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id", type(int)) if hasattr(data, "get") else None
    value = data.get("value")
    if not isinstance(user_id, int) or not isinstance(value, int):
        raise BadRequest("Fields 'user_id' (int) and 'value' (1..5) are required.")
    try:
        agg = add_rating(guide_id, user_id, value)
        return jsonify(agg), 201
    except ValueError as e:
        raise BadRequest(str(e))
