def test_login_success_returns_token_and_user(client, reset_data):
    response = client.post(
        "/api/auth/login",
        json={"username": "sales1", "password": "password123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token"]
    assert body["user"] == {"id": 1, "name": "Sales Satu"}


def test_login_wrong_password_returns_401(client, reset_data):
    response = client.post(
        "/api/auth/login",
        json={"username": "sales1", "password": "salah"},
    )

    assert response.status_code == 401
    assert response.json()["message"] == "Username atau password salah."


def test_protected_endpoints_require_token(client, reset_data):
    responses = [
        client.get("/api/activities"),
        client.get("/api/entities"),
        client.post(
            "/api/activities",
            json={
                "entityId": "ent-b2g-1",
                "segment": "B2G",
                "visitDate": "2026-03-10",
            },
        ),
        client.patch("/api/activities/act-x", json={"status": "VISITED"}),
    ]

    for response in responses:
        assert response.status_code == 401
        assert response.json()["message"] == "Token autentikasi diperlukan."


def test_invalid_token_returns_401(client, reset_data):
    response = client.get(
        "/api/activities",
        headers={"Authorization": "Bearer token-tidak-valid"},
    )

    assert response.status_code == 401
    assert response.json()["message"] == "Sesi tidak valid atau sudah kedaluwarsa."


def test_sales_id_cannot_be_supplied_in_body(client, auth, reset_data):
    response = client.post(
        "/api/activities",
        headers=auth("sales2"),
        json={
            "entityId": "ent-b2g-1",
            "segment": "B2G",
            "visitDate": "2026-03-10",
            "salesId": 1,
        },
    )

    assert response.status_code == 422
