from Cinescope.constants import LOGIN_ENDPOINT, AUTH_URL
from Cinescope.custom_requester.custom_requester import CustomRequester
from Cinescope.resources.models.user_model import UserLoginModel


class AuthAdmin(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_URL)

    def login_admin(self, admin_data, expected_status=200):
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=admin_data,
            expected_status=expected_status,
        )

    def authenticate_admin(self, admin_data):
        login_data = UserLoginModel(
            email=admin_data.email,
            password=admin_data.password,
        )

        response = self.login_admin(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")

        token = response["accessToken"]
        self._update_session_headers(**{"Authorization": "Bearer " + token})
