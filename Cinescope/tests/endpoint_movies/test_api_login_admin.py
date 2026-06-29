import pytest
import allure
class TestAuthAdminApi:
    @pytest.mark.api
    @pytest.mark.smoke
    @allure.step("Аутентификация ADMIN")
    def test_login_admin(self, api_manager, test_admin):  # логинимся
        with allure.step("Аутентификация пользователя с ролью ADMIN"):
            response = api_manager.admin_auth_api.login_admin(test_admin)
        assert response.status_code == 201
