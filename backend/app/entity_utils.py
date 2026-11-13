import re

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Activity


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def history_entity_id(
    name: str, entity_type: str, region: str, segment: str
) -> str:
    """ID sintetis stabil untuk entitas yang hanya ada di riwayat."""
    parts = [
        slugify(name),
        slugify(entity_type),
        slugify(region),
        segment.lower(),
    ]
    return "hist:" + "-".join(part for part in parts if part)


def entity_label(name: str, entity_type: str) -> str:
    return f"{name} ({entity_type})"


def find_history_snapshot(
    db: Session, entity_id: str
) -> tuple[str, str, str, str] | None:
    """Cari snapshot riwayat terbaru yang cocok dengan ID sintetis."""
    stmt = (
        select(
            Activity.entity_name,
            Activity.entity_type,
            Activity.entity_region,
            Activity.segment,
        )
        .group_by(
            Activity.entity_name,
            Activity.entity_type,
            Activity.entity_region,
            Activity.segment,
        )
        .order_by(func.max(Activity.created_at).desc())
    )
    for name, entity_type, region, segment in db.execute(stmt).all():
        if history_entity_id(name, entity_type, region, segment) == entity_id:
            return name, entity_type, region, segment
    return None
