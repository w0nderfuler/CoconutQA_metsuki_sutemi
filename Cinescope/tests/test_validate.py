import pytest
from pydantic import ValidationError

from Cinescope.DataGeneratorMovies import MovieData
from Cinescope.resources.models.user_model import RequestUserRegisterModel


class TestInvalidValidate:
    def test_invalid_validate_email(self, test_user):
        user_data = test_user.model_dump()
        user_data["email"] = MovieData.generate_invalid_email()

        with pytest.raises(ValidationError):
            RequestUserRegisterModel(**user_data)

    def test_invalid_validate_password_repeat(self, test_user):
        user_data = test_user.model_dump()
        user_data["passwordRepeat"] = MovieData.generate_password_repeat()

        with pytest.raises(ValidationError):
            RequestUserRegisterModel(**user_data)

    def test_invalid_validate_password_min_len(self, test_user):
        user_data = test_user.model_dump()
        user_data["password"] = MovieData.generate_password_min()
        user_data["passwordRepeat"] = user_data["password"]

        with pytest.raises(ValidationError):
            RequestUserRegisterModel(**user_data)
