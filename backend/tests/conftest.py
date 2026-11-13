import os
from datetime import date
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Muat .env root bila ada, lalu paksa tes memakai database terpisah.
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://visitflow:visitflow@localhost:5433/visitflow_test",
)
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ["JWT_SECRET"] = "test-only-secret"

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import text  # noqa: E402

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Activity, Entity, User  # noqa: E402
from app.security import hash_password  # noqa: E402

SALES1_ID = 1
SALES2_ID = 2
SALES3_ID = 3

ENT_B2G_1 = "ent-b2g-1"
ENT_B2G_2 = "ent-b2g-2"
ENT_B2B_1 = "ent-b2b-1"
ENT_B2B_2 = "ent-b2b-2"
ENT_DUP_B2G = "ent-dup-b2g"
ENT_DUP_B2B = "ent-dup-b2b"

TEST_PASSWORD_HASH = hash_password("password123")


def _base_users() -> list[User]:
    return [
        User(
            id=SALES1_ID,
            name="Sales Satu",
            username="sales1",
            password_hash=TEST_PASSWORD_HASH,
        ),
        User(
            id=SALES2_ID,
            name="Sales Dua",
            username="sales2",
            password_hash=TEST_PASSWORD_HASH,
        ),
        User(
            id=SALES3_ID,
            name="Sales Tiga",
            username="sales3",
            password_hash=TEST_PASSWORD_HASH,
        ),
    ]


def _base_entities() -> list[Entity]:
    return [
        Entity(
            id=ENT_B2G_1,
            name="Kantor Melati",
            type="Instansi",
            segment="B2G",
            region="Bandung",
        ),
        Entity(
            id=ENT_B2G_2,
            name="Dinas Cendana",
            type="Instansi",
            segment="B2G",
            region="Surabaya",
        ),
        Entity(
            id=ENT_B2B_1,
            name="Toko Melati",
            type="Perusahaan",
            segment="B2B",
            region="Jakarta",
        ),
        Entity(
            id=ENT_B2B_2,
            name="CV Sinar Jaya",
            type="Perusahaan",
            segment="B2B",
            region="Medan",
        ),
        # Nama sama, tipe berbeda untuk menguji label pembeda.
        Entity(
            id=ENT_DUP_B2G,
            name="Cempaka",
            type="Instansi",
            segment="B2G",
            region="Bandung",
        ),
        Entity(
            id=ENT_DUP_B2B,
            name="Cempaka",
            type="Perusahaan",
            segment="B2B",
            region="Bandung",
        ),
    ]


@pytest.fixture(scope="session", autouse=True)
def prepare_schema():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
def reset_data():
    with engine.begin() as connection:
        connection.execute(
            text(
                "TRUNCATE TABLE activities, entities, users "
                "RESTART IDENTITY CASCADE"
            )
        )

    with SessionLocal() as db:
        db.add_all(_base_users())
        db.add_all(_base_entities())
        db.commit()

    yield


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth(client, reset_data):
    def _login(username: str = "sales1") -> dict[str, str]:
        response = client.post(
            "/api/auth/login",
            json={"username": username, "password": "password123"},
        )
        assert response.status_code == 200
        return {"Authorization": f"Bearer {response.json()['token']}"}

    return _login


@pytest.fixture
def make_activity(reset_data):
    def _make(
        activity_id: str,
        visit_date: date,
        status: str = "NOT_VISITED",
        sales_id: int = SALES1_ID,
        entity_id: str | None = ENT_B2G_1,
        entity_name: str | None = None,
        entity_type: str | None = None,
        region: str | None = None,
        segment: str | None = None,
    ) -> str:
        with SessionLocal() as db:
            if entity_id is not None:
                entity = db.get(Entity, entity_id)
                assert entity is not None
                snapshot = {
                    "entity_id": entity.id,
                    "entity_name": entity.name,
                    "entity_type": entity.type,
                    "entity_region": entity.region,
                    "segment": entity.segment,
                }
            else:
                snapshot = {
                    "entity_id": None,
                    "entity_name": entity_name,
                    "entity_type": entity_type,
                    "entity_region": region,
                    "segment": segment,
                }

            db.add(
                Activity(
                    id=activity_id,
                    **snapshot,
                    visit_date=visit_date,
                    status=status,
                    sales_id=sales_id,
                )
            )
            db.commit()
        return activity_id

    return _make
