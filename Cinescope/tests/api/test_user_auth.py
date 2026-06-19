from Cinescope.resources.models.user_model import ResponseUserRegisterModel


class TestUser:
    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)
        response_data = ResponseUserRegisterModel.model_validate(response.json())

        assert response_data.email == creation_user_data.email
        assert response_data.fullName == creation_user_data.fullName

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = ResponseUserRegisterModel.model_validate(
            super_admin.api.user_api.get_user(created_user["id"]).json()
        )
        response_by_email = ResponseUserRegisterModel.model_validate(
            super_admin.api.user_api.get_user(creation_user_data.email).json()
        )

        assert response_by_id == response_by_email
        assert response_by_id.email == creation_user_data.email
        assert response_by_id.fullName == creation_user_data.fullName

    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)
