from Cinescope.resources.models.user_model import ResponseUserRegisterModel
import pytest
import allure
class TestUser:
    @pytest.mark.api
    @pytest.mark.smoke
    @allure.title("Тест с перезапусками")
    @pytest.mark.flaky(reruns=2)
    def test_create_user(self, super_admin, creation_user_data, delay_between_retries):
        with allure.step("Шаг 1: Проверка в случае совпадения при создании"):
            response = super_admin.api.user_api.create_user(creation_user_data)
        response_data = ResponseUserRegisterModel.model_validate(response.json())
        assert response_data.email == creation_user_data.email
        assert response_data.fullName == creation_user_data.fullName

    @pytest.mark.api
    @pytest.mark.smoke
    @allure.title("Поиск созданного юзера")
    def test_get_user_by_locator(self, super_admin, creation_user_data):
        with allure.step("Создание юзера"):
            created_user = super_admin.api.user_api.create_user(creation_user_data).json()
        with allure.step("Поиск юзера по id"):
            response_by_id = ResponseUserRegisterModel.model_validate(
            super_admin.api.user_api.get_user(created_user["id"]).json()
        )
        with allure.step("Поиск юзера по email"):
            response_by_email = ResponseUserRegisterModel.model_validate(
            super_admin.api.user_api.get_user(creation_user_data.email).json()
        )

        assert response_by_id == response_by_email
        assert response_by_id.email == creation_user_data.email
        assert response_by_id.fullName == creation_user_data.fullName

    @pytest.mark.api
    @pytest.mark.smoke
    @allure.title("Запрет получения информации о пользователе для роли USER")
    def test_get_user_by_id_common_user(self, common_user):
        with allure.step("Попытка получить информацию о пользователе"):
            common_user.api.user_api.get_user(common_user.email, expected_status=403)
