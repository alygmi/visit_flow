"""Seed data fiktif dan idempotent untuk demo Visit Flow.

Jalankan dari direktori backend:
    python -m app.seed
"""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Activity, Entity, User
from app.security import hash_password

DEMO_PASSWORD = "password123"

USERS = [
    {"username": "sales1", "name": "Adit Pratama"},
    {"username": "sales2", "name": "Rina Kurnia"},
    {"username": "sales3", "name": "Bayu Santoso"},
]

ENTITIES = [
    {
        "id": "ent-001",
        "name": "Kantor Layanan Melati",
        "type": "Instansi",
        "segment": "B2G",
        "region": "Bandung",
    },
    {
        "id": "ent-002",
        "name": "Dinas Pendidikan Cendana",
        "type": "Instansi",
        "segment": "B2G",
        "region": "Bandung",
    },
    {
        "id": "ent-003",
        "name": "Kantor Wilayah Kenanga",
        "type": "Instansi",
        "segment": "B2G",
        "region": "Jakarta",
    },
    {
        "id": "ent-004",
        "name": "Balai Pelatihan Anggrek",
        "type": "Instansi",
        "segment": "B2G",
        "region": "Surabaya",
    },
    {
        "id": "ent-005",
        "name": "Dinas Kesehatan Flamboyan",
        "type": "Instansi",
        "segment": "B2G",
        "region": "Yogyakarta",
    },
    {
        "id": "ent-006",
        "name": "Kantor Kelurahan Dahlia",
        "type": "Instansi",
        "segment": "B2G",
        "region": "Semarang",
    },
    {
        "id": "ent-007",
        "name": "Badan Arsip Merpati",
        "type": "Instansi",
        "segment": "B2G",
        "region": "Jakarta",
    },
    {
        "id": "ent-008",
        "name": "Toko Sinar Jaya",
        "type": "Perusahaan",
        "segment": "B2B",
        "region": "Jakarta",
    },
    {
        "id": "ent-009",
        "name": "PT Melati Digital",
        "type": "Perusahaan",
        "segment": "B2B",
        "region": "Bandung",
    },
    {
        "id": "ent-010",
        "name": "CV Sinar Jaya Express",
        "type": "Perusahaan",
        "segment": "B2B",
        "region": "Surabaya",
    },
    {
        "id": "ent-011",
        "name": "Koperasi Cendana Sejahtera",
        "type": "Koperasi",
        "segment": "B2B",
        "region": "Bandung",
    },
    {
        "id": "ent-012",
        "name": "PT Anggrek Niaga",
        "type": "Perusahaan",
        "segment": "B2B",
        "region": "Medan",
    },
    {
        "id": "ent-013",
        "name": "CV Flamboyan Teknologi",
        "type": "Perusahaan",
        "segment": "B2B",
        "region": "Yogyakarta",
    },
    {
        "id": "ent-014",
        "name": "Toko Merpati Jaya",
        "type": "Perusahaan",
        "segment": "B2B",
        "region": "Semarang",
    },
]

# Kunjungan dengan entitas master. Snapshot diambil dari ENTITIES.
ACTIVITIES = [
    ("act-001", "ent-001", date(2026, 3, 1), "NOT_VISITED", "sales1"),
    ("act-002", "ent-008", date(2026, 3, 1), "VISITED", "sales2"),
    ("act-003", "ent-002", date(2026, 3, 3), "VISITED", "sales1"),
    ("act-004", "ent-009", date(2026, 3, 5), "NOT_VISITED", "sales3"),
    ("act-005", "ent-003", date(2026, 3, 8), "VISITED", "sales2"),
    ("act-006", "ent-010", date(2026, 3, 10), "NOT_VISITED", "sales1"),
    ("act-007", "ent-004", date(2026, 3, 12), "VISITED", "sales3"),
    ("act-008", "ent-011", date(2026, 3, 14), "NOT_VISITED", "sales2"),
    ("act-009", "ent-005", date(2026, 3, 17), "VISITED", "sales1"),
    ("act-010", "ent-012", date(2026, 3, 19), "NOT_VISITED", "sales3"),
    ("act-011", "ent-006", date(2026, 3, 21), "VISITED", "sales2"),
    ("act-012", "ent-013", date(2026, 3, 23), "NOT_VISITED", "sales1"),
    ("act-013", "ent-007", date(2026, 3, 25), "VISITED", "sales3"),
    ("act-014", "ent-014", date(2026, 3, 27), "NOT_VISITED", "sales2"),
    ("act-015", "ent-001", date(2026, 3, 29), "VISITED", "sales1"),
    ("act-016", "ent-008", date(2026, 3, 31), "VISITED", "sales3"),
    ("act-017", "ent-002", date(2026, 3, 31), "NOT_VISITED", "sales2"),
    ("act-018", "ent-003", date(2026, 2, 25), "VISITED", "sales1"),
    ("act-019", "ent-010", date(2026, 4, 2), "VISITED", "sales3"),
    ("act-020", "ent-004", date(2026, 4, 5), "NOT_VISITED", "sales2"),
]

# Kunjungan lama tanpa entitas master, untuk mendemokan fallback riwayat.
HISTORICAL_ACTIVITIES = [
    {
        "id": "hist-001",
        "entity_name": "Kantor Layanan Seruni",
        "entity_type": "Instansi",
        "entity_region": "Bandung",
        "segment": "B2G",
        "visit_date": date(2025, 12, 10),
        "status": "VISITED",
        "sales_username": "sales1",
    },
    {
        "id": "hist-002",
        "entity_name": "PT Puspa Mandiri",
        "entity_type": "Perusahaan",
        "entity_region": "Jakarta",
        "segment": "B2B",
        "visit_date": date(2026, 1, 15),
        "status": "NOT_VISITED",
        "sales_username": "sales2",
    },
    {
        "id": "hist-003",
        "entity_name": "Koperasi Tunas Baru",
        "entity_type": "Koperasi",
        "entity_region": "Surabaya",
        "segment": "B2B",
        "visit_date": date(2026, 2, 5),
        "status": "VISITED",
        "sales_username": "sales3",
    },
    {
        "id": "hist-004",
        "entity_name": "Balai Desa Cempaka",
        "entity_type": "Instansi",
        "entity_region": "Yogyakarta",
        "segment": "B2G",
        "visit_date": date(2026, 2, 18),
        "status": "VISITED",
        "sales_username": "sales1",
    },
]


def _seed_users(db: Session) -> dict[str, User]:
    by_username: dict[str, User] = {}
    for item in USERS:
        user = db.scalar(select(User).where(User.username == item["username"]))
        if user is None:
            user = User(
                name=item["name"],
                username=item["username"],
                password_hash=hash_password(DEMO_PASSWORD),
            )
            db.add(user)
            print(f"  + user {item['username']}")
        else:
            user.name = item["name"]
        by_username[item["username"]] = user
    db.flush()
    return by_username


def _seed_entities(db: Session) -> dict[str, Entity]:
    by_id: dict[str, Entity] = {}
    for item in ENTITIES:
        entity = db.get(Entity, item["id"])
        if entity is None:
            entity = Entity(**item)
            db.add(entity)
            print(f"  + entitas {item['id']}")
        else:
            entity.name = item["name"]
            entity.type = item["type"]
            entity.segment = item["segment"]
            entity.region = item["region"]
        by_id[item["id"]] = entity
    db.flush()
    return by_id


def _snapshot(entity: Entity) -> dict[str, str]:
    return {
        "entity_id": entity.id,
        "entity_name": entity.name,
        "entity_type": entity.type,
        "entity_region": entity.region,
        "segment": entity.segment,
    }


def run_seed(db: Session) -> None:
    print("Menjalankan seed Visit Flow...")
    users = _seed_users(db)
    entities = _seed_entities(db)

    for activity_id, entity_id, visit_date, status, username in ACTIVITIES:
        if db.get(Activity, activity_id) is not None:
            continue
        entity = entities[entity_id]
        db.add(
            Activity(
                id=activity_id,
                **_snapshot(entity),
                visit_date=visit_date,
                status=status,
                sales_id=users[username].id,
            )
        )
        print(f"  + kunjungan {activity_id}")

    for item in HISTORICAL_ACTIVITIES:
        if db.get(Activity, item["id"]) is not None:
            continue
        user = users[item["sales_username"]]
        db.add(
            Activity(
                id=item["id"],
                entity_id=None,
                entity_name=item["entity_name"],
                entity_type=item["entity_type"],
                entity_region=item["entity_region"],
                segment=item["segment"],
                visit_date=item["visit_date"],
                status=item["status"],
                sales_id=user.id,
            )
        )
        print(f"  + kunjungan {item['id']}")

    db.commit()
    print("Seed selesai. Data yang sudah ada tidak diduplikasi.")


def main() -> None:
    with SessionLocal() as db:
        run_seed(db)


if __name__ == "__main__":
    main()
