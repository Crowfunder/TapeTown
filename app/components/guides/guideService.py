# services/guides_service.py
from __future__ import annotations
from math import radians, sin, cos, asin, sqrt
from typing import Optional, List, Dict, Any

from sqlalchemy import func, select, desc
from sqlalchemy.orm import Session

from models import db, GuideRecord  # "guide" == AudioRecord
# optional (create these models in models.py):
# from models import GuideReport, GuideRating

#funkcja pomocnicza do uzyskania propozycji
def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in KM."""
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c


def add_guide(payload: Dict[str, Any]) -> GuideRecord:
    required = ["name", "thumbnail_url", "audio_url", "user_id"]
    missing = [k for k in required if not payload.get(k)]
    if missing:
        raise ValueError(f"Missing fields: {', '.join(missing)}")

    guide = GuideRecord(
        name=payload["name"],
        thumbnail_url=payload["thumbnail_url"],
        audio_url=payload["audio_url"],
        location=payload.get("location"),
        user_id=int(payload["user_id"]),
        likes=int(payload.get("likes", 0)),
        latitude=payload.get("latitude"),
        longitude=payload.get("longitude"),
    )
    db.session.add(guide)
    db.session.commit()
    return guide


def remove_guide(guide_id: int, *, by_user_id: Optional[int] = None) -> bool:
    guide = GuideRecord.query.get(guide_id)
    if not guide:
        return False
    # simple ownership check (skip if not needed):
    if by_user_id is not None and guide.user_id != by_user_id:
        raise PermissionError("You are not allowed to remove this guide.")
    db.session.delete(guide)
    db.session.commit()
    return True


def report_guide(guide_id: int, reason: str, reporter_user_id: Optional[int] = None) -> int:
    if not reason or len(reason) < 3:
        raise ValueError("Reason is required.")
    # Requires GuideReport model (id, guide_id, reason, reporter_user_id, created_at)
    from models import GuideReport  # lazy import to avoid circulars
    rep = GuideReport(guide_id=guide_id, reason=reason, reporter_user_id=reporter_user_id)
    db.session.add(rep)
    db.session.commit()
    return rep.id


def get_audio_for_guide(guide_id: int) -> Optional[str]:
    guide = GuideRecord.query.get(guide_id)
    return guide.audio_url if guide else None


def get_recommended_guides(lat: float, lon: float, *, radius_km: float = 10.0, limit: int = 20) -> List[GuideRecord]:
    if lat is None or lon is None:
        return []

    # Coarse box ~0.12° per 13 km; adjust with radius
    deg = radius_km / 111.0
    q = (
        GuideRecord.query
        .filter(GuideRecord.latitude.isnot(None), GuideRecord.longitude.isnot(None))
        .filter(GuideRecord.latitude.between(lat - deg, lat + deg))
        .filter(GuideRecord.longitude.between(lon - deg, lon + deg))
        .limit(limit * 5)  # wider prefetch
    ).all()

    scored = []
    for g in q:
        d = _haversine_km(lat, lon, g.latitude, g.longitude)
        if d <= radius_km:
            # score: nearer is better; likes as tie-breaker
            score = (d, -g.likes)
            scored.append((score, g))

    scored.sort(key=lambda x: x[0])
    return [g for _, g in scored[:limit]]


def add_rating(guide_id: int, user_id: int, value: int) -> Dict[str, Any]:
    if value not in (1, 2, 3, 4, 5):
        raise ValueError("Rating must be in 1..5")
    from models import GuideRating  # lazy import
    # upsert-like logic: replace user's rating if exists
    existing = GuideRating.query.filter_by(guide_id=guide_id, user_id=user_id).first()
    if existing:
        existing.value = value
    else:
        db.session.add(GuideRating(guide_id=guide_id, user_id=user_id, value=value))
    db.session.commit()

    # aggregate
    agg = db.session.execute(
        select(func.count(GuideRating.id), func.avg(GuideRating.value)).where(GuideRating.guide_id == guide_id)
    ).one()
    count, avg = int(agg[0]), float(agg[1]) if agg[1] is not None else 0.0
    return {"guide_id": guide_id, "count": count, "avg": round(avg, 3)}
