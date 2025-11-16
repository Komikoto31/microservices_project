import warnings


def test_register_and_login(client):
    """Регистрация и авторизация пользователя"""
    # Подавляем warning только для этой функции
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message=".*argon2.__version__.*"
        )

        reg_response = client.post("/api/users/", json={
            "email": "user1@example.com",
            "name": "User1",
            "password": "123456"
        })
        assert reg_response.status_code == 200
        data = reg_response.json()
        assert data["email"] == "user1@example.com"

        login_response = client.post("/api/users/login", json={
            "email": "user1@example.com",
            "password": "123456"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        assert token

# def test_get_profile(client):
#     """Проверка доступа к /me с токеном"""
#     # Регистрируем и логинимся
#     reg = client.post("/api/users/", json={
#         "email": "profile@test.com",
#         "name": "Test",
#         "password": "123456"
#     })
#     login = client.post("/api/users/login", json={
#         "email": "profile@test.com",
#         "password": "123456"
#     })
#     token = login.json()["access_token"]
#
#     headers = {"Authorization": f"Bearer {token}"}
#     me = client.get("/api/users/me", headers=headers)
#     assert me.status_code == 200
#     assert "email" in me.json()