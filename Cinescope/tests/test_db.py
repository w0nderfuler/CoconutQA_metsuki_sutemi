from Cinescope.db_requester.db_client import get_db_session
from Cinescope.db_models.user import UserDBModel
from Cinescope.DataGeneratorMovies import MovieData
import allure
import pytest
@allure.epic("Тестирование базы данных")
@allure.feature("Тестирование таблицы movies совместно с эндпоинтом /movies")
class TestDBSession:
    @allure.story("Корректность подключения сессии к БД")
    @allure.description("""
        1. Использование метода get
        2. Использование метода post
        3. Использование метода put
        4. Использование метода patch
        5. Использование метода delete
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("QA", "metsuki_sutemi")
    @allure.title("Создание пользователя и сохранение его в БД")
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.bd

    def test_db_requests(self, super_admin, db_helper, created_test_user):
        with allure.step("Создание пользователя и сохранение его в БД"):
            assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
        assert db_helper.user_exists_by_email("api1@gmail.com")

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.bd
    @allure.title("Тест генерации данных не созданного фильма и отсутствия его в БД")
    def test_db_absent_movie(self, super_admin, db_helper):
        movie_data = MovieData.create_movie()
        movie_name = movie_data["name"]
        with allure.step("Поиск фильма по имени"):
            movie_from_db = db_helper.get_movie_by_name(movie_name)
        assert movie_from_db is None

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.bd
    @allure.title("Тест поиска созданного фильма в БД")
    def test_db_get_movie_by_id(self, super_admin, db_helper):
        movie_data = MovieData.create_movie()
        with allure.step("Создание фильма"):
            response = super_admin.api.movies_api.create_movie(movie_data)
        movie_name = response.json()["name"]
        with allure.step("Поиск фильма по имени"):
            movie_from_db = db_helper.get_movie_by_name(movie_name)
        assert movie_from_db is not None
        assert movie_from_db.name == movie_data["name"]

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.bd
    @allure.title("Тест на удаления фильма и отсутствия его в БД")
    def test_db_delete_movie(self, super_admin, db_helper, movie_for_delete):
        movie_id = movie_for_delete["id"]
        movie_name = movie_for_delete["name"]
        with allure.step("Поиск фильма по имени"):
            movie_from_db = db_helper.get_movie_by_name(movie_name)
        assert movie_from_db is not None
        with allure.step("Удаление фильма"):
            super_admin.api.movies_api.delete_movie_by_id(movie_id)
        with allure.step("Проверка отсутствия фильма в БД"):
            movie_is_missing_db = db_helper.get_movie_by_name(movie_name)
        assert movie_is_missing_db is None

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.bd
    @allure.title("Тест полного сценария от создания до удаления фильма из БД")
    def test_movie_create_and_delete_reflected_in_db(self, super_admin, db_helper):
        with allure.step("Генерация данных"):
            movie_data = MovieData.create_movie()
        movie_name = movie_data["name"]

        with allure.step("Проверка отсутствия данных в БД"):
            movie_from_db = db_helper.get_movie_by_name(movie_name)
        assert movie_from_db is None

        with allure.step("Создание фильма через API"):
            create_response = super_admin.api.movies_api.create_movie(movie_data)
        movie_id = create_response.json()["id"]

        with allure.step("Проверка наличия фильма в БД"):
            movie_from_db = db_helper.get_movie_by_name(movie_name)
        assert movie_from_db is not None
        assert movie_from_db.name == movie_name

        with allure.step("Удаление фильма через API"):
            super_admin.api.movies_api.delete_movie_by_id(movie_id)

        with allure.step("Отсутствие данных в БД"):
            movie_from_db = db_helper.get_movie_by_name(movie_name)
        assert movie_from_db is None

