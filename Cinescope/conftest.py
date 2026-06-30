import pytest
import requests
import allure
import random
import time
from faker import Faker
from Cinescope.DataGeneratorMovies import MovieData
from Cinescope.api.api_manager import ApiManager
from Cinescope.constants import LOGIN_ADMIN, PASSWORD_ADMIN
from Cinescope.resources.user_creds import SuperAdminCreds
from Cinescope.entities.user import User
from Cinescope.resources.roles import Roles
from Cinescope.resources.models.user_model import (
    RequestUserRegisterModel,
    UserCreateModel,
    UserLoginModel,
    UserUpdateModel,
)
from Cinescope.resources.models.movie_model import MovieModel
from sqlalchemy.orm import Session
from collections.abc import Generator
from Cinescope.db_requester.db_client import engine, get_db_session
from Cinescope.db_requester.db_helper import DBHelper
from Cinescope.db_requester.models import AccountTransactionTemplate, Base
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
def test_user() -> RequestUserRegisterModel:
    password = MovieData.generate_password()
    email = faker.unique.email()
    return RequestUserRegisterModel(
        email=email,
        fullName=faker.name(),
        password=password,
        passwordRepeat=password,
        roles=[Roles.USER],
    )


@pytest.fixture()
def registered_user(api_manager, test_user):
    api_manager.auth_api.register_user(test_user)
    return test_user


@pytest.fixture(scope="session")
def test_admin():
    return UserLoginModel(email=LOGIN_ADMIN, password=PASSWORD_ADMIN)


@pytest.fixture(scope="session")
def login_admin(api_manager, test_admin):
    api_manager.admin_auth_api.authenticate_admin(test_admin)
    return api_manager


@pytest.fixture()
def created_movie(super_admin):
    movie_data = MovieData.create_movie()
    response = super_admin.api.movies_api.create_movie(movie_data)
    movie = MovieModel.model_validate(response.json()).model_dump(mode="json")
    movie_id = movie["id"]

    yield movie
    super_admin.api.movies_api.delete_movie_by_id(movie_id)


@pytest.fixture()
def created_published_movie(super_admin):
    movie_data = MovieData.create_movie()
    movie_data["published"] = True

    response = super_admin.api.movies_api.create_movie(movie_data)
    movie = MovieModel.model_validate(response.json()).model_dump(mode="json")
    movie_id = movie["id"]

    yield movie

    super_admin.api.movies_api.delete_movie_by_id(movie_id)


@pytest.fixture()
def movie_for_delete(super_admin):
    movie_data = MovieData.create_movie()
    response = super_admin.api.movies_api.create_movie(movie_data)
    print(response.json())
    movie = MovieModel.model_validate(response.json()).model_dump(mode="json")
    movie_id = movie["id"]
    yield movie
    try:
        super_admin.api.movies_api.delete_movie_by_id(movie_id, expected_status=200)
    except ValueError:
        pass


@pytest.fixture()
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture()
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session,
    )
    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture(scope="function")
def creation_user_data(test_user: RequestUserRegisterModel):
    return UserCreateModel(
        email=test_user.email,
        fullName=test_user.fullName,
        password=test_user.password,
    )


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session,
    )
    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture()
def common_admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    created_user = super_admin.api.user_api.create_user(creation_user_data).json()
    user_id = created_user["id"]
    admin_admin = UserUpdateModel(
        roles=[Roles.ADMIN],
        verified=True,
        banned=False,
    )
    super_admin.api.user_api.update_user(user_id, admin_admin)
    common_admin = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.ADMIN.value],
        new_session,
    )
    common_admin.api.auth_api.authenticate(common_admin.creds)
    return common_admin

@pytest.fixture(scope="module")
def db_session() -> Generator[Session, None, None]:
    session = get_db_session()

    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    user = db_helper.create_test_user(MovieData.generate_user_data())
    yield user
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)


@pytest.fixture(scope="function")
def account_transaction_pair(db_session):
    Base.metadata.create_all(bind=engine)

    stan = AccountTransactionTemplate(
        **MovieData.generate_account_transaction_data("Stan", 1000)
    )
    bob = AccountTransactionTemplate(
        **MovieData.generate_account_transaction_data("Bob", 500)
    )

    db_session.add_all([stan, bob])
    db_session.commit()
    db_session.refresh(stan)
    db_session.refresh(bob)

    yield stan, bob

    db_session.rollback()
    for account in (stan, bob):
        account_from_db = (
            db_session.query(AccountTransactionTemplate)
            .filter_by(user=account.user)
            .one_or_none()
        )
        if account_from_db:
            db_session.delete(account_from_db)
    db_session.commit()


@pytest.fixture  # была добавлена в файл conftest.py
def delay_between_retries():
    time.sleep(2)  # Задержка в 2 секунды\ это не обязательно, но
    yield  # нужно понимать что такая возможность имеется
