from Cinescope.constants import BASE_URL, AUTH_URL
from Cinescope.custom_requester.custom_requester import CustomRequester


class UserAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_URL)

    def get_user(self, user_locator, expected_status=200):
        return self.send_request(method="GET", endpoint=f'/user/{user_locator}', expected_status=expected_status)

    def create_user(self, user_data, expected_status = 201):
        return self.send_request(
            method="POST",
            endpoint = "/user",
            data=user_data,
            expected_status = expected_status
        )

    def update_user(self, user_id, user_data, expected_status = 200):
        return self.send_request(
            method="PATCH",
            endpoint = f'/user/{user_id}',
            data=user_data,
            expected_status = expected_status
        )