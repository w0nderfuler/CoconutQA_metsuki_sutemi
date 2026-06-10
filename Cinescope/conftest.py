import pytest
import requests
from faker import Faker
from Cinescope.DataGeneratorMovies import MovieData
from Cinescope.api.api_manager import ApiManager
from Cinescope.constants import LOGIN_ADMIN, PASSWORD_ADMIN

faker = Faker()


@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


@pytest.fixture()
def test_user():
    password = faker.password(length=12)
    return {
        "email": faker.email(),
        "fullName": faker.name(),
        "password": password,
        "passwordRepeat": password,
        "roles": ["USER"],
    }


@pytest.fixture()
def registered_user(api_manager, test_user):
    api_manager.auth_api.register_user(test_user)
    return test_user


@pytest.fixture(scope="session")
def test_admin():
    return {"email": LOGIN_ADMIN, "password": PASSWORD_ADMIN}


@pytest.fixture(scope="session")
def login_admin(api_manager, test_admin):
    api_manager.admin_auth_api.authenticate_admin(test_admin)
    return api_manager


@pytest.fixture()
def created_movie(login_admin):
    movie_data = MovieData.create_movie()
    response = login_admin.movies_api.create_movie(movie_data)
    movie = response.json()
    movie_id = movie["id"]

    yield movie
    login_admin.movies_api.delete_movie_by_id(movie_id)

@pytest.fixture()
def created_published_movie(login_admin):
    movie_data = MovieData.create_movie()
    movie_data["published"] = True

    response = login_admin.movies_api.create_movie(movie_data)
    movie = response.json()
    movie_id = movie["id"]

    yield movie

    login_admin.movies_api.delete_movie_by_id(movie_id)


@pytest.fixture()
def movie_for_delete(login_admin):
    movie_data = MovieData.create_movie()
    response = login_admin.movies_api.create_movie(movie_data)
    return response.json()
