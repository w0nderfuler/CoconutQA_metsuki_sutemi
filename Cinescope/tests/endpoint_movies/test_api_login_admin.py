class TestAuthAdminApi:
    def test_login_admin(self, api_manager, test_admin):  # логинимся
        response = api_manager.admin_auth_api.login_admin(test_admin)
        assert response.status_code == 200
