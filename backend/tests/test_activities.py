from datetime import date

from tests.conftest import (
    ENT_B2B_1,
    ENT_B2G_1,
    ENT_B2G_2,
    SALES1_ID,
    SALES2_ID,
)


def test_date_filter_is_inclusive(client, auth, make_activity):
    make_activity("act-from", date(2026, 3, 1))
    make_activity("act-to", date(2026, 3, 31))
    make_activity("act-outside", date(2026, 4, 1))

    response = client.get(
        "/api/activities",
        params={"from": "2026-03-01", "to": "2026-03-31"},
        headers=auth(),
    )

    assert response.status_code == 200
    ids = {item["id"] for item in response.json()["items"]}
    assert ids == {"act-from", "act-to"}


def test_combined_filters_are_applied_in_sql(client, auth, make_activity):
    make_activity(
        "act-match",
        date(2026, 3, 15),
        status="VISITED",
        entity_id=ENT_B2G_1,
    )
    make_activity(
        "act-wrong-segment",
        date(2026, 3, 15),
        status="VISITED",
        entity_id=ENT_B2B_1,
    )
    make_activity(
        "act-wrong-status",
        date(2026, 3, 16),
        status="NOT_VISITED",
        entity_id=ENT_B2G_1,
    )
    make_activity(
        "act-outside-date",
        date(2026, 4, 1),
        status="VISITED",
        entity_id=ENT_B2G_1,
    )
    make_activity(
        "act-wrong-name",
        date(2026, 3, 17),
        status="VISITED",
        entity_id=ENT_B2G_2,
    )

    response = client.get(
        "/api/activities",
        params={
            "segment": "B2G",
            "status": "VISITED",
            "from": "2026-03-01",
            "to": "2026-03-31",
            "search": "melati",
        },
        headers=auth(),
    )

    assert response.status_code == 200
    items = response.json()["items"]
    assert [item["id"] for item in items] == ["act-match"]
    assert items[0]["entityName"] == "Kantor Melati"


def test_from_after_to_returns_400(client, auth, reset_data):
    response = client.get(
        "/api/activities",
        params={"from": "2026-03-31", "to": "2026-03-01"},
        headers=auth(),
    )

    assert response.status_code == 400
    body = response.json()
    assert body["message"] == "Tanggal mulai tidak boleh setelah tanggal akhir."
    assert "from" in body["errors"]


def test_post_requires_required_fields(client, auth, reset_data):
    response = client.post("/api/activities", json={}, headers=auth())

    assert response.status_code == 422
    body = response.json()
    assert body["message"] == "Data yang dikirim tidak valid."
    assert {"entityId", "segment", "visitDate"} <= set(body["errors"])


def test_post_rejects_invalid_date_and_segment(client, auth, reset_data):
    bad_date = client.post(
        "/api/activities",
        json={
            "entityId": ENT_B2G_1,
            "segment": "B2G",
            "visitDate": "2026-02-30",
        },
        headers=auth(),
    )
    assert bad_date.status_code == 422
    assert "visitDate" in bad_date.json()["errors"]

    bad_segment = client.post(
        "/api/activities",
        json={
            "entityId": ENT_B2G_1,
            "segment": "B2C",
            "visitDate": "2026-03-10",
        },
        headers=auth(),
    )
    assert bad_segment.status_code == 422
    assert bad_segment.json()["errors"]["segment"] == (
        "Segmen harus B2G atau B2B."
    )


def test_post_rejects_segment_mismatch_with_entity(client, auth, reset_data):
    response = client.post(
        "/api/activities",
        json={
            "entityId": ENT_B2G_1,
            "segment": "B2B",
            "visitDate": "2026-03-10",
        },
        headers=auth(),
    )

    assert response.status_code == 400
    assert response.json()["errors"]["segment"] == (
        "Segmen tidak sesuai dengan segmen entitas."
    )


def test_post_rejects_unknown_entity(client, auth, reset_data):
    response = client.post(
        "/api/activities",
        json={
            "entityId": "ent-tidak-ada",
            "segment": "B2G",
            "visitDate": "2026-03-10",
        },
        headers=auth(),
    )

    assert response.status_code == 400
    assert response.json()["errors"]["entityId"] == "Entitas tidak ditemukan."


def test_post_uses_identity_from_token(client, auth, reset_data):
    response = client.post(
        "/api/activities",
        json={
            "entityId": ENT_B2G_1,
            "segment": "B2G",
            "visitDate": "2026-05-01",
        },
        headers=auth("sales2"),
    )

    assert response.status_code == 201
    item = response.json()
    assert item["salesId"] == SALES2_ID
    assert item["salesName"] == "Sales Dua"
    assert item["status"] == "NOT_VISITED"
    assert item["canEdit"] is True
    assert item["entityId"] == ENT_B2G_1


def test_patch_owner_and_non_owner(client, auth, make_activity):
    make_activity("act-owned", date(2026, 3, 12), sales_id=SALES1_ID)

    forbidden = client.patch(
        "/api/activities/act-owned",
        json={"status": "VISITED"},
        headers=auth("sales2"),
    )
    assert forbidden.status_code == 403
    assert forbidden.json()["message"] == (
        "Anda hanya dapat mengubah kunjungan milik Anda."
    )

    allowed = client.patch(
        "/api/activities/act-owned",
        json={"status": "VISITED"},
        headers=auth("sales1"),
    )
    assert allowed.status_code == 200
    assert allowed.json()["status"] == "VISITED"
    assert allowed.json()["canEdit"] is True


def test_patch_missing_activity_returns_404(client, auth, reset_data):
    response = client.patch(
        "/api/activities/act-tidak-ada",
        json={"status": "VISITED"},
        headers=auth(),
    )

    assert response.status_code == 404
    assert response.json()["message"] == "Kunjungan tidak ditemukan."


def test_patch_rejects_invalid_status(client, auth, make_activity):
    make_activity("act-status", date(2026, 3, 12))

    response = client.patch(
        "/api/activities/act-status",
        json={"status": "SELESAI"},
        headers=auth(),
    )

    assert response.status_code == 422
    assert response.json()["errors"]["status"] == (
        "Status harus VISITED atau NOT_VISITED."
    )


def test_summary_matches_items(client, auth, make_activity):
    make_activity("act-summary-1", date(2026, 3, 10), status="VISITED")
    make_activity("act-summary-2", date(2026, 3, 11), status="VISITED")
    make_activity(
        "act-summary-3", date(2026, 3, 12), status="NOT_VISITED"
    )

    response = client.get(
        "/api/activities",
        params={"segment": "B2G"},
        headers=auth(),
    )

    assert response.status_code == 200
    body = response.json()
    items = body["items"]
    summary = body["summary"]
    assert summary["total"] == len(items) == 3
    assert summary["visited"] == 2
    assert summary["notVisited"] == 1
    assert summary["visited"] + summary["notVisited"] == summary["total"]


def test_empty_result_returns_200_and_empty_items(client, auth, reset_data):
    response = client.get(
        "/api/activities",
        params={"search": "tidak-ada-yang-cocok"},
        headers=auth(),
    )

    assert response.status_code == 200
    assert response.json() == {
        "items": [],
        "summary": {"total": 0, "visited": 0, "notVisited": 0},
    }


def test_can_edit_only_true_for_owner(client, auth, make_activity):
    make_activity("act-own", date(2026, 3, 10), sales_id=SALES1_ID)
    make_activity("act-other", date(2026, 3, 11), sales_id=SALES2_ID)

    response = client.get("/api/activities", headers=auth("sales1"))

    assert response.status_code == 200
    flags = {item["id"]: item["canEdit"] for item in response.json()["items"]}
    assert flags == {"act-own": True, "act-other": False}
