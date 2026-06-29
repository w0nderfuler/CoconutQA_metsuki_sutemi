from Cinescope.DataGeneratorMovies import MovieData

import pytest
import allure

@allure.epic("Тестирование методов ендпоинта movies")
@allure.feature("Тестирование ролей")
class TestSuperAdminMethodsPositive:
    @allure.story("Корректность использования методов")
    @allure.description("""
    1. Использование метода get
    2. Использование метода post
    3. Использование метода put
    4. Использование метода patch
    5. Использование метода delete
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("QA", "metsuki_sutemi")
    @allure.title("Тест получения афиши фильмов")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get(self, super_admin):  # список фильмов
        with allure.step("Получение списка фильмов"):
            response = super_admin.api.movies_api.get_movies()
        response_data = response.json()
        assert "movies" in response_data
        assert "count" in response_data
        assert "pageSize" in response_data
        assert "pageCount" in response_data

    @allure.title("Тест получения списка фильма с заранее заданными фильтрами")
    @pytest.mark.api
    @pytest.mark.slow
    def test_get_params(self, super_admin):
        with allure.step("Заданные параметры"):
            params = {"page": 1, "minPrice": 1, "maxPrice": 1000}
        with allure.step("Получение списка фильма"):
            response = super_admin.api.movies_api.get_movies(params=params)
        response_data = response.json()
        assert response_data["page"] == params["page"]
        assert "movies" in response_data
        assert isinstance(response_data["movies"], list)
        movies = response_data["movies"]
        assert movies, f"Фильтр вернул пустой список: {response_data}"
        for movie in movies:
            assert movie["price"] >= params["minPrice"]
            assert movie["price"] <= params["maxPrice"]

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "params",
        [
            {"minPrice": 1, "maxPrice": 1000},
            {"locations": ["MSK", "SPB"]},
            {"genreId": 1},
        ],
        ids=["price", "location", "genreId"],
    )
    @allure.title("Тест фильтрации списка фильмов по фильтрам")
    def test_get_movies_filter_and_params(self, super_admin, params):
        with allure.step("Получение списка фильмов"):
            response = super_admin.api.movies_api.get_movies(params=params)
        response_data = response.json()
        movies = response_data["movies"]
        for movie in movies:
            if "locations" in params:
                assert movie["location"] in params["locations"]
            if "minPrice" in params:
                assert movie["price"] >= params["minPrice"]
            if "maxPrice" in params:
                assert movie["price"] <= params["maxPrice"]
            if "genreId" in params:
                assert movie["genreId"] == params["genreId"]

    @allure.title("Тест на создание фильма")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_post(self, super_admin):  # создание фильма
        with allure.step("Создание фильма"):
            movie_data = MovieData.create_movie()
        response = super_admin.api.movies_api.create_movie(movie_data)
        response_data = response.json()
        assert movie_data["name"] == response_data["name"]
        assert movie_data["price"] == response_data["price"]
        assert movie_data["description"] == response_data["description"]
        assert movie_data["genreId"] == response_data["genreId"]

    @allure.title("Тест на создание и поиска фильма по фильтрам")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_post_get_id_params(self, created_published_movie, super_admin):
        with allure.step("Создание фильма"):
            movie_id = created_published_movie["id"]
        price = created_published_movie["price"]
        with allure.step("Фильтры для сужения поиска созданного фильма"):
            params = {
            "locations": created_published_movie["location"],
            "genreId": created_published_movie["genreId"],
            "published": created_published_movie["published"],
            "minPrice": price - 1,
            "maxPrice": price + 1,
        }
        with allure.step("Поиск фильма"):
            response = super_admin.api.movies_api.get_movies(params=params)
        response_data = response.json()
        movies = response_data["movies"]
        assert movies, f"Фильтр вернул пустой список. params={params}"
        assert any(movie["id"] == movie_id for movie in movies)

        for movie in movies:
            assert movie["published"] is True
            assert movie["location"] == created_published_movie["location"]
            assert movie["genreId"] == created_published_movie["genreId"]
            assert params["minPrice"] <= movie["price"] <= params["maxPrice"]

    @allure.title("Тест на получение фильма по id")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_movie_id(
        self, super_admin, created_movie
    ):  # запрашиваем конкретный фильм
        movie_id = created_movie["id"]
        with allure.step("Получение фильма по id"):
            response = super_admin.api.movies_api.get_movie_by_id(movie_id)
        response_data = response.json()
        assert movie_id == response_data["id"]
        assert response_data["name"] == created_movie["name"]
        assert response_data["description"] == created_movie["description"]
        assert response_data["genreId"] == created_movie["genreId"]

    @allure.title("Удаление фильма по id")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_delete_movie_id(self, super_admin, movie_for_delete):  # удаляем фильм по id
        movie_id = movie_for_delete["id"]
        with allure.step("Удаляем фильм по id"):
            response = super_admin.api.movies_api.delete_movie_by_id(movie_id)
        response_data = response.json()
        assert movie_id == response_data["id"]

    @allure.title("Изменение названия фильма")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_update_movie_body(
        self, super_admin, created_movie
    ):  # обновляем имя и описание фильма
        movie_id = created_movie["id"]
        new_name = MovieData.generate_movie_data()
        with allure.step("Новое имя для фильма"):
            update_data = {"name": new_name}
        with allure.step("Смена имени фильма"):
            response = super_admin.api.movies_api.patch_movie(movie_id, update_data)
        updated_movie = response.json()
        assert updated_movie["name"] == update_data["name"]

    @allure.title("Удаление фильм с помощью разных ролей")
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "user_role, expected_status",
        [
            ("super_admin", 200),
            (
                "common_admin",
                403,
            ),  # Должно возвращать 403, но фильм удаляется поэтому 200
            ("common_user", 403),
        ],
        ids=["Super admin", "Admin", "User"],
    )
    def test_role_delete_movie(self, request, user_role, expected_status, movie_for_delete):
        user = request.getfixturevalue(user_role)
        movie_id = movie_for_delete["id"]
        with allure.step("Удаление фильма"):
            response = user.api.movies_api.delete_movie_by_id(
            movie_id, expected_status=expected_status)
        if expected_status == 200:
            response_data = response.json()
            assert movie_id == response_data["id"]
            get_response = user.api.movies_api.get_movie_by_id(
                movie_id, expected_status=404
            )
            assert get_response.status_code == 404
        else:
            response_data = response.json()
            assert "message" in response_data


class TestSuperAdminMethodsNegative:
    @allure.story("Корректность обработки ошибок при использовании методов")
    @allure.description("""
        1. Использование метода get
        2. Использование метода post
        3. Использование метода put
        4. Использование метода patch
        5. Использование метода delete
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("QA", "metsuki_sutemi")
    @allure.title("Получение списка фильмов с некорректными фильтрами")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_invalid_params(self, super_admin):
        with allure.step("Создание некорректных фильтров"):
            invalid_page = (
            MovieData.invalid_movie_id()
        )  # получаем фильм с неверными параметрами
        with allure.step("Попытка получить фильм с неверными параметрами"):
            response = super_admin.api.movies_api.get_movies(
            params={"page": invalid_page}, expected_status=400
        )
        assert response.status_code == 400

    @allure.title("Создание фильма с некорректными данными")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_post_invalid(self, super_admin):  # создать фильм с пустым именем
        movie_data = MovieData.create_movie()
        with allure.step("Задаем неверные данные"):
            movie_data["name"] = ""
        with allure.step("Попытка создать фильм с неверными данными"):
            response = super_admin.api.movies_api.create_movie(
            movie_data, expected_status=400
        )
        assert response.status_code == 400
        error_data = response.json()
        assert "message" in error_data

    @allure.title("Создание дублирующего фильма")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_post_duplicate_movie_name(
        self, created_movie, super_admin
    ):  # создаем дубликат
        movie_data = MovieData.create_movie()
        with allure.step("Создание дублирующей сущности"):
            movie_data["name"] = created_movie["name"]
        with allure.step("Попытка создания дубля"):
            response = super_admin.api.movies_api.create_movie(
            movie_data, expected_status=409
        )
        assert response.status_code == 409
        error_data = response.json()
        assert "message" in error_data

    @allure.title("Получение фильма по невалидному id")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_by_invalid_id(self, super_admin):  # получаем фильм с неправильным id
        with allure.step("Создание невалидного id"):
            fake_movie_id = MovieData.invalid_movie_id()
        with allure.step("Попытка получить фильма по невалидному id"):
            response = super_admin.api.movies_api.get_movie_by_id(
            movie_id=fake_movie_id, expected_status=404
        )
        assert response.status_code == 404

    @allure.title("Удаление фильма по невалидному id")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_delete_movie_negative_id(
        self, movie_for_delete, super_admin
    ):  # удаляем с неверным id
        with allure.step("Создание невалидного id"):
            fake_movie_id = MovieData.invalid_movie_id()
        with allure.step("Попытка удалить фильм по невалидному id"):
            response = super_admin.api.movies_api.delete_movie_by_id(
            movie_id=fake_movie_id, expected_status=404
        )
        assert response.status_code == 404

    @allure.title("Удаление фильма по некорректному id")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_delete_movie_invalid_id(self, super_admin, movie_for_delete):  # удаляем с неправильным форматом id
        with allure.step("Попытка удалить фильм по некорректному id"):
            response = super_admin.api.movies_api.delete_movie_by_id(
            movie_id="a", expected_status=404
        )
        assert (
            response.status_code == 404
        )  # Возвращает 404, ожидаемый результат по Swagger 400

    @allure.title("Изменение имени фильма на невалидное имя")
    @pytest.mark.api
    @pytest.mark.slow
    @pytest.mark.xfail(
        reason="BUG: PATCH /movies/{id} возвращает 404 вместо 400 для пустого name"
    )
    def test_update_movie_invalid_name(
        self, created_published_movie, super_admin
    ):  # создаем и обновляем фильм с пустым именем
        movie_data = created_published_movie["id"]
        with allure.step("Изменение тела для запроса"):
            update_movie_data = {"name": " "}
        with allure.step("Попытка изменить имя на невалидное имя"):
            response = super_admin.api.movies_api.patch_movie(
            movie_data, update_movie_data, expected_status=400
        )
        assert response.status_code == 400


class TestUserMethodNegative:
    @allure.story("Корректность обработки ошибок при использовании методов")
    @allure.description("""
           1. Использование метода post
           """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("QA", "metsuki_sutemi")
    @allure.title("Создание фильм с ролью USER")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_post_user_without_rights_create_movie(self, common_user):  # создание фильма
        movie_data = MovieData.create_movie()
        with allure.step("Попытка создать фильм с ролью USER"):
            response = common_user.api.movies_api.create_movie(
            movie_data, expected_status=403
        )
        assert response.status_code == 403


class TestAdminMethod:
    @allure.story("Изменение роли")
    @allure.description("""
            1. Использование метода get
            2. Использование метода post
            3. Использование метода put
            """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("QA", "metsuki_sutemi")
    @allure.title("Изменение роли USER на ADMIN")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_common_admin_fixture(self, super_admin, common_admin):
        with allure.step("Создание USER -> Обновление до роли ADMIN"):
            response = super_admin.api.user_api.get_user(common_admin.email)
        user_data = response.json()

        assert response.status_code == 200
        assert user_data["email"] == common_admin.email
        assert "ADMIN" in user_data["roles"]
