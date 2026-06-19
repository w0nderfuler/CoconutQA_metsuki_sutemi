from Cinescope.api.api_manager import ApiManager
from Cinescope.resources.models.user_model import (
    ResponseUserRegisterModel,
    UserLoginModel,
)


class TestAuthAPI:
    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        response_data = ResponseUserRegisterModel.model_validate(response.json())

        assert response_data.email == test_user.email
        assert test_user.roles[0] in response_data.roles

    def test_register_and_login_user(
        self,
        api_manager: ApiManager,
        registered_user,
    ):
        login_data = UserLoginModel(
            email=registered_user.email,
            password=registered_user.password,
        )
        response_data = api_manager.auth_api.login_user(login_data).json()

        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user.email
