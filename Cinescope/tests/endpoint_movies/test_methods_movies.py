from Cinescope.DataGeneratorMovies import MovieData
from faker import Faker
import random


class TestMethodsPositive:
    def test_get(self, api_manager, login_admin):  # список фильмов
        response = login_admin.movies_api.get_movies()
        assert response.status_code == 200

    def test_post(self, api_manager, login_admin):  # создание фильма
        movie_data = MovieData.create_movie()
        response = login_admin.movies_api.create_movie(movie_data)
        assert response.status_code == 201

    def test_get_movie_id(self, login_admin, created_movie):  # запрашиваем конкретный фильм
        movie_id = created_movie["id"]
        response = login_admin.movies_api.get_movie_by_id(movie_id)
        assert response.status_code == 200

    def test_delete_movie_id(self, login_admin, movie_for_delete):  # удаляем фильм по id
        movie_id = movie_for_delete["id"]
        response = login_admin.movies_api.delete_movie_by_id(movie_id)
        assert response.status_code == 200

    def test_update_movie_body(self, login_admin, created_movie):  # обновляем имя и описание фильма
        movie_id = created_movie["id"]
        fake = Faker()
        update_data = {"name": fake.name(), "description": fake.text()}
        response = login_admin.movies_api.patch_movie(movie_id, update_data)
        assert response.status_code == 200
        updated_movie = response.json()
        assert updated_movie["name"] == update_data["name"]


class TestMethodsNegative:
    def test_get_invalid(self, api_manager, login_admin): #получаем фильм с неверными параметрами
        response = login_admin.movies_api.get_movies_invalid()
        assert response.status_code == 400

    def test_post_invalid(self, api_manager, login_admin): #создать фильм с пустым именем
        movie_data = MovieData.create_movie()
        movie_data["name"] = " "
        response = login_admin.movies_api.create_movie(movie_data, expected_status=400)
        assert response.status_code == 400

    def test_post_duplicate_movie_name(self, created_movie, login_admin): #создаем дубликат
        movie_data = MovieData.create_movie()
        movie_data["name"] = created_movie["name"]
        response = login_admin.movies_api.create_movie(movie_data, expected_status=409)
        assert response.status_code == 409

    def test_get_by_invalid_id(self, api_manager, login_admin): #получаем фильм с неправильным id
        fake_movie_id = random.randint(-100, -1)
        response = login_admin.movies_api.get_movie_by_id(
            movies_id=fake_movie_id, expected_status=404
        )
        assert response.status_code == 404

    def test_delete_movie_negative_id(self, movie_for_delete, login_admin): #удаляем с неверным id
        fake_movie_id = random.randint(-100, -1)
        response = login_admin.movies_api.delete_movie_by_id(
            movie_id=fake_movie_id, expected_status=404
        )
        assert response.status_code == 404

    def test_delete_movie_invalid_id(self, login_admin, movie_for_delete): #удаляем с неправильным форматом id
        response = login_admin.movies_api.delete_movie_by_id(
            movie_id="a", expected_status=404
        )
        assert response.status_code == 404

    def test_update_movie_invalid_name(self, created_movie, login_admin): #создаем и обновляем фильм с пустым именем
        fake = Faker()
        movie_data = created_movie["id"]
        update_movie_data = {"name": " ", "description": fake.text()}
        response = login_admin.movies_api.patch_movie(
            movie_data, update_movie_data, expected_status=400
        )
        assert response.status_code == 400
