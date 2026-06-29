import pytest
from pydantic import ValidationError
import allure
from Cinescope.DataGeneratorMovies import MovieData
from Cinescope.resources.models.user_model import RequestUserRegisterModel

@allure.epic("Тестирование некорректной валидации")
@allure.feature("Тестирование неверного формата данных")
class TestInvalidValidate:
    @allure.story("Корректность данных request/response")
    @allure.description("""
            Этот тест проверяет некорректную валидацию данных
            """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "metsuki_sutemi")
    @allure.title("Тест валидации email")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_invalid_validate_email(self, test_user):
        user_data = test_user.model_dump()
        user_data["email"] = MovieData.generate_invalid_email()

        with pytest.raises(ValidationError):
            RequestUserRegisterModel(**user_data)

    @pytest.mark.api
    @pytest.mark.smoke
    @allure.title("Тест на не сопоставление паролей")
    def test_invalid_validate_password_repeat(self, test_user):
        user_data = test_user.model_dump()
        with allure.step("Подмена пароля для строки 'Повторите пароль'"):
            user_data["passwordRepeat"] = MovieData.generate_password_repeat()

        with pytest.raises(ValidationError):
            RequestUserRegisterModel(**user_data)

    @pytest.mark.api
    @pytest.mark.smoke
    @allure.title("Тест на слишком короткий пароль")
    def test_invalid_validate_password_min_len(self, test_user):
        user_data = test_user.model_dump()
        with allure.step("Создание невалидного пароля"):
            user_data["password"] = MovieData.generate_password_min()
        user_data["passwordRepeat"] = user_data["password"]

        with pytest.raises(ValidationError):
            RequestUserRegisterModel(**user_data)
