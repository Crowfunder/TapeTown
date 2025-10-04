# services/guides_service.py
from __future__ import annotations
from math import radians, sin, cos, asin, sqrt
from typing import Optional, List, Dict, Any
from sqlalchemy.exc import IntegrityError

from sqlalchemy import func, select, desc
from sqlalchemy.orm import Session

from app.database.models import db, GuidesRecord, GuidesRating

#funkcja pomocnicza do uzyskania propozycji
def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in KM."""
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c


def add_guide(payload: Dict[str, Any]) -> GuidesRecord:
    required = ["name", "thumbnail_url", "audio_url", "user_id"]
    missing = [k for k in required if not payload.get(k)]
    if missing:
        raise ValueError(f"Missing fields: {', '.join(missing)}")

    guide = GuidesRecord(
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
    guide = GuidesRecord.query.get(guide_id)
    if not guide:
        return False
    # simple ownership check (skip if not needed):
    if by_user_id is not None and guide.user_id != by_user_id:
        raise PermissionError("You are not allowed to remove this guide.")
    db.session.delete(guide)
    db.session.commit()
    return True


# def report_guide(guide_id: int, reason: str, reporter_user_id: Optional[int] = None) -> int:
#     if not reason or len(reason) < 3:
#         raise ValueError("Reason is required.")
#     # Requires GuideReport model (id, guide_id, reason, reporter_user_id, created_at)
#     from models import GuideReport  # lazy import to avoid circulars
#     rep = GuideReport(guide_id=guide_id, reason=reason, reporter_user_id=reporter_user_id)
#     db.session.add(rep)
#     db.session.commit()
#     return rep.id

def get_recommended_guides(lat: float, lon: float, *, radius_km: float = 10.0, limit: int = 20) -> List[GuidesRecord]:
    if lat is None or lon is None:
        return []

    # Coarse box ~0.12° per 13 km; adjust with radius
    deg = radius_km / 111.0
    q = (
        GuidesRecord.query
        .filter(GuidesRecord.latitude.isnot(None), GuidesRecord.longitude.isnot(None))
        .filter(GuidesRecord.latitude.between(lat - deg, lat + deg))
        .filter(GuidesRecord.longitude.between(lon - deg, lon + deg))
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
    if not (1 <= value <= 5):
        raise ValueError("Rating must be in 1..5")

    try:
        if db.session.bind.dialect.name == "sqlite":
            from sqlalchemy.dialects.sqlite import insert

            stmt = insert(GuidesRating).values(
                guide_id=guide_id,
                user_id=user_id,
                rating=value,
            ).on_conflict_do_update(
                index_elements=[GuidesRating.guide_id, GuidesRating.user_id],
                set_={"rating": value},
            )
            db.session.execute(stmt)
        else:
            existing = GuidesRating.query.filter_by(
                guide_id=guide_id, user_id=user_id
            ).first()
            if existing:
                existing.rating = value
            else:
                db.session.add(GuidesRating(
                    guide_id=guide_id, user_id=user_id, rating=value
                ))

        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        raise ValueError("Unique constraint on (guide_id, user_id) is missing or violated.")

    agg = db.session.execute(
        select(
            func.count(GuidesRating.id),
            func.avg(GuidesRating.rating)
        ).where(GuidesRating.guide_id == guide_id)
    ).one()

    count = int(agg[0])
    avg = float(agg[1]) if agg[1] is not None else 0.0
    return {"guide_id": guide_id, "count": count, "avg": round(avg, 3)}
