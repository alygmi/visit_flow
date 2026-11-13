from datetime import date
from uuid import uuid4

from fastapi import APIRouter, Query
from sqlalchemy import select

from app.deps import CurrentUser, DbSession
from app.entity_utils import find_history_snapshot
from app.errors import api_error
from app.models import Activity, Entity, User
from app.schemas import (
    ActivityCreate,
    ActivityItem,
    ActivityListResponse,
    ActivityStatusUpdate,
    ActivitySummary,
    ActivityStatus,
    Segment,
)

router = APIRouter(tags=["activities"])


def _to_item(activity: Activity, sales_name: str, current_user_id: int) -> ActivityItem:
    return ActivityItem(
        id=activity.id,
        entity_id=activity.entity_id,
        entity_name=activity.entity_name,
        entity_type=activity.entity_type,
        segment=activity.segment,
        region=activity.entity_region,
        visit_date=activity.visit_date,
        status=activity.status,
        sales_id=activity.sales_id,
        sales_name=sales_name,
        can_edit=activity.sales_id == current_user_id,
    )


def _resolve_entity(
    db: DbSession, entity_id: str, segment: str
) -> tuple[str | None, str, str, str]:
    """Kembalikan (entity_id, nama, tipe, wilayah) dari master atau riwayat."""
    if entity_id.startswith("hist:"):
        snapshot = find_history_snapshot(db, entity_id)
        if snapshot is None:
            api_error(
                400,
                "Entitas riwayat tidak ditemukan.",
                {"entityId": "Entitas riwayat tidak ditemukan."},
            )
        name, entity_type, region, snapshot_segment = snapshot
        if snapshot_segment != segment:
            api_error(
                400,
                "Segmen tidak sesuai dengan segmen entitas.",
                {"segment": "Segmen tidak sesuai dengan segmen entitas."},
            )
        return None, name, entity_type, region

    entity = db.get(Entity, entity_id)
    if entity is None:
        api_error(
            400,
            "Entitas tidak ditemukan.",
            {"entityId": "Entitas tidak ditemukan."},
        )
    if entity.segment != segment:
        api_error(
            400,
            "Segmen tidak sesuai dengan segmen entitas.",
            {"segment": "Segmen tidak sesuai dengan segmen entitas."},
        )
    return entity.id, entity.name, entity.type, entity.region

@router.get("/api/activities", response_model=ActivityListResponse)
def list_activities(
    db:DbSession,
    current_user:CurrentUser,
    segment:Segment | None = Query(default=None),
    status:ActivityStatus | None = Query(default=None),
    date_from:date | None = Query(default=None, alias="start"),
    date_to:date | None = Query(default=None, alias="end"),
    search:str | None = Query(default=None)
    ) -> ActivityListResponse:
    if date_from and date_to and date_from > date_to:
        api_error(
            400,
            "Tanggal mulai tidak valid.",
            {"start": "Tanggal mulai tidak valid."},
        )

    filters = []
    if segment:
        filters.append(Activity.segment == segment)
    if status:
        filters.append(Activity.status == status)
    if date_from:
        filters.append(Activity.visit_date >= date_from)
    if date_to:
        filters.append(Activity.visit_date <= date_to)
    term = (search or "").strip()
    if term:
        filters.append(Activity.entity_name.ilike(f"%{term}%"))

    rows = db.execute(
        select(Activity, User.name)
        .join(User, Activity.sales_id == User.id)
        .where(*filters)
        .order_by(
            Activity.visit_date.desc(),
            Activity.created_at.desc(),
            Activity.id.desc()
        )
    ).all()

    items = [
        _to_item(activity, sales_name, current_user.id)
        for activity, sales_name in rows
    ]
    visited = sum(1 for item in items if item.status == "VISITED")
    summary = ActivitySummary(
        total=len(items),
        visited=visited,
        not_visited=len(items) - visited,
    )
    return ActivityListResponse(items=items, summary=summary)


@router.post(
    "/api/activities", response_model=ActivityItem, status_code=201
)
def create_activity(
    payload: ActivityCreate,
    db: DbSession,
    current_user: CurrentUser,
) -> ActivityItem:
    entity_id, name, entity_type, region = _resolve_entity(
        db, payload.entity_id, payload.segment
    )

    activity = Activity(
        id=f"act-{uuid4().hex}",
        entity_id=entity_id,
        entity_name=name,
        entity_type=entity_type,
        entity_region=region,
        segment=payload.segment,
        visit_date=payload.visit_date,
        status="NOT_VISITED",
        sales_id=current_user.id,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)

    return _to_item(activity, current_user.name, current_user.id)


@router.patch("/api/activities/{activity_id}", response_model=ActivityItem)
def update_activity_status(
    activity_id: str,
    payload: ActivityStatusUpdate,
    db: DbSession,
    current_user: CurrentUser,
) -> ActivityItem:
    activity = db.get(Activity, activity_id)
    if activity is None:
        api_error(404, "Kunjungan tidak ditemukan.")

    if activity.sales_id != current_user.id:
        api_error(403, "Anda hanya dapat mengubah kunjungan milik Anda.")

    activity.status = payload.status
    db.commit()
    db.refresh(activity)

    return _to_item(activity, activity.sales.name, current_user.id)
