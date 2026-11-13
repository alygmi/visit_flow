from fastapi import APIRouter, Query
from sqlalchemy import select

from app.deps import CurrentUser, DbSession
from app.entity_utils import entity_label, history_entity_id
from app.models import Activity, Entity
from app.schemas import EntityListResponse, EntityOption, Segment

router = APIRouter(tags=["entities"])


@router.get("/api/entities", response_model=EntityListResponse)
def list_entities(
    db: DbSession,
    current_user: CurrentUser,
    segment: Segment | None = Query(default=None),
    search: str | None = Query(default=None),
) -> EntityListResponse:
    term = (search or "").strip() or None

    stmt = select(Entity)
    if segment:
        stmt = stmt.where(Entity.segment == segment)
    if term:
        stmt = stmt.where(Entity.name.ilike(f"%{term}%"))
    entities = db.scalars(stmt.order_by(Entity.name, Entity.type)).all()

    if entities:
        return EntityListResponse(
            items=[
                EntityOption(
                    id=entity.id,
                    name=entity.name,
                    type=entity.type,
                    segment=entity.segment,
                    region=entity.region,
                    label=entity_label(entity.name, entity.type)
                )
                for entity in entities
            ]
        )

    # Master kosong: pakai kombinasi unik snapshot riwayat yang cocok filter.
    history_stmt = select(
        Activity.entity_name,
        Activity.entity_type,
        Activity.segment,
        Activity.entity_region
    ).group_by(
        Activity.entity_name,
        Activity.entity_type,
        Activity.segment,
        Activity.entity_region
    )
    if segment:
        history_stmt = history_stmt.where(Activity.segment == segment)
    if term:
        history_stmt = history_stmt.where(Activity.entity_name.ilike(f"%{term}%"))

    rows = db.execute(
        history_stmt.order_by(Activity.entity_name, Activity.entity_type)
    ).all()

    seen: set[str] = set()
    items: list[EntityOption] = []
    for name, entity_type, row_segment, region in rows:
        synthetic_id = history_entity_id(
            name, entity_type, region, row_segment
        )
        if synthetic_id in seen:
            continue
        seen.add(synthetic_id)
        items.append(
            EntityOption(
                id=synthetic_id,
                name=name,
                type=entity_type,
                segment=row_segment,
                region=region,
                label=entity_label(name, entity_type)
            )
        )

    return EntityListResponse(items=items)
