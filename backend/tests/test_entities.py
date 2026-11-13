from datetime import date

from tests.conftest import (
    ENT_DUP_B2B,
    ENT_DUP_B2G,
    ENT_B2G_1,
    SALES1_ID,
)


def test_master_options_have_type_labels_and_no_duplicates(
    client, auth, reset_data
):
    response = client.get(
        "/api/entities", params={"search": "cempaka"}, headers=auth()
    )

    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) == 2
    assert {item["id"] for item in items} == {ENT_DUP_B2G, ENT_DUP_B2B}
    assert {item["label"] for item in items} == {
        "Cempaka (Instansi)",
        "Cempaka (Perusahaan)",
    }


def test_entity_segment_filter(client, auth, reset_data):
    response = client.get(
        "/api/entities", params={"segment": "B2G"}, headers=auth()
    )

    assert response.status_code == 200
    items = response.json()["items"]
    assert items
    assert {item["segment"] for item in items} == {"B2G"}


def test_history_fallback_only_when_master_is_empty(
    client, auth, make_activity
):
    make_activity(
        "hist-activity-1",
        date(2026, 1, 10),
        entity_id=None,
        entity_name="Kantor Seruni",
        entity_type="Instansi",
        region="Bandung",
        segment="B2G",
        sales_id=SALES1_ID,
    )
    make_activity(
        "hist-activity-2",
        date(2026, 1, 11),
        entity_id=None,
        entity_name="Kantor Seruni",
        entity_type="Instansi",
        region="Bandung",
        segment="B2G",
        sales_id=SALES1_ID,
    )

    fallback = client.get(
        "/api/entities", params={"search": "seruni"}, headers=auth()
    )
    assert fallback.status_code == 200
    items = fallback.json()["items"]
    assert len(items) == 1
    assert items[0]["id"].startswith("hist:")
    assert items[0]["label"] == "Kantor Seruni (Instansi)"
    assert items[0]["name"] == "Kantor Seruni"

    # Master tidak kosong tanpa pencarian, jadi fallback tidak dicampurkan.
    master_only = client.get("/api/entities", headers=auth())
    assert master_only.status_code == 200
    assert all(
        not item["id"].startswith("hist:")
        for item in master_only.json()["items"]
    )

    no_match = client.get(
        "/api/entities",
        params={"search": "seruni", "segment": "B2B"},
        headers=auth(),
    )
    assert no_match.status_code == 200
    assert no_match.json()["items"] == []


def test_post_with_history_entity_id_uses_latest_snapshot(
    client, auth, make_activity
):
    make_activity(
        "hist-source",
        date(2026, 1, 10),
        entity_id=None,
        entity_name="Kantor Seruni",
        entity_type="Instansi",
        region="Bandung",
        segment="B2G",
    )

    options = client.get(
        "/api/entities", params={"search": "seruni"}, headers=auth()
    ).json()["items"]
    history_id = options[0]["id"]

    created = client.post(
        "/api/activities",
        json={
            "entityId": history_id,
            "segment": "B2G",
            "visitDate": "2026-05-10",
        },
        headers=auth(),
    )

    assert created.status_code == 201
    item = created.json()
    assert item["entityId"] is None
    assert item["entityName"] == "Kantor Seruni"
    assert item["entityType"] == "Instansi"
    assert item["region"] == "Bandung"


def test_post_with_unknown_history_id_returns_400(client, auth, reset_data):
    response = client.post(
        "/api/activities",
        json={
            "entityId": "hist:tidak-ada",
            "segment": "B2G",
            "visitDate": "2026-05-10",
        },
        headers=auth(),
    )

    assert response.status_code == 400
    assert response.json()["message"] == "Entitas riwayat tidak ditemukan."


def test_history_fallback_respects_segment_filter(
    client, auth, make_activity
):
    make_activity(
        "hist-b2b",
        date(2026, 1, 10),
        entity_id=None,
        entity_name="PT Puspa",
        entity_type="Perusahaan",
        region="Jakarta",
        segment="B2B",
    )

    response = client.get(
        "/api/entities",
        params={"search": "puspa", "segment": "B2B"},
        headers=auth(),
    )

    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) == 1
    assert items[0]["segment"] == "B2B"
