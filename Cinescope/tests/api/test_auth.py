from Cinescope.api.api_manager import ApiManager
from Cinescope.resources.models.user_model import (
    ResponseUserRegisterModel,
    UserLoginModel,
)
import allure
import pytest
import random

class TestAuthAPI:
    @pytest.mark.api
    @pytest.mark.smoke
    @allure.title("Регистрация пользователя самостоятельно")
    def test_register_user(self, api_manager, test_user):
        with allure.step("Регистрация пользователя"):
            response = api_manager.auth_api.register_user(test_user)
        response_data = ResponseUserRegisterModel.model_validate(response.json())

        assert response_data.email == test_user.email
        assert test_user.roles[0] in response_data.roles

    @pytest.mark.api
    @pytest.mark.smoke
    @allure.title("Регистрация и аутентификация пользователя")
    def test_register_and_login_user(self, api_manager: ApiManager,registered_user):
        with allure.step("Формирование тела для авторизации"):
            login_data = UserLoginModel(
            email=registered_user.email,
            password=registered_user.password,
        )
        with allure.step("Аутентификация пользователя"):
            response_data = api_manager.auth_api.login_user(login_data).json()

        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user.email
