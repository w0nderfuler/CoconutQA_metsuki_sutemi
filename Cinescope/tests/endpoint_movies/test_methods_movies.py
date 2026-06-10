from Cinescope.DataGeneratorMovies import MovieData



class TestMethodsPositive:
    def test_get(self, api_manager, login_admin):  # список фильмов
        response = login_admin.movies_api.get_movies()
        assert response.status_code == 200
        response_data = response.json()
        assert "movies" in response_data
        assert "count" in response_data
        assert "pageSize" in response_data
        assert "pageCount" in response_data

    def test_get_params(self, api_manager, login_admin):
        params = {"page":1,
                  "minPrice":1,
                  "maxPrice":1000}
        response = login_admin.movies_api.get_movies(params=params)
        response_data = response.json()
        assert response_data["page"]== params["page"]
        assert "movies" in response_data
        assert isinstance(response_data["movies"], list)
        movies = response_data["movies"]
        assert movies, f"Фильтр вернул пустой список: {response_data}"
        for movie in movies:
            assert movie["price"] >= params["minPrice"]
            assert movie["price"] <= params["maxPrice"]

    def test_post(self, api_manager, login_admin):  # создание фильма
        movie_data = MovieData.create_movie()
        response = login_admin.movies_api.create_movie(movie_data)
        assert response.status_code == 201
        response_data = response.json()
        assert movie_data["name"] == response_data["name"]
        assert movie_data["price"] == response_data["price"]
        assert movie_data["description"] == response_data["description"]
        assert movie_data["genreId"] == response_data["genreId"]

    def test_post_get_id_params(self, created_published_movie, login_admin):
        movie_id = created_published_movie["id"]
        price = created_published_movie["price"]
        params = {
            "locations": created_published_movie["location"],
            "genreId": created_published_movie["genreId"],
            "published": created_published_movie["published"],
            "minPrice": price - 1,
            "maxPrice": price + 1,
        }
        response = login_admin.movies_api.get_movies(params=params)
        assert response.status_code == 200
        response_data = response.json()
        movies = response_data["movies"]
        assert movies, f"Фильтр вернул пустой список. params={params}"
        assert any(movie["id"] == movie_id for movie in movies)

        for movie in movies:
            assert movie["published"] is True
            assert movie["location"] == created_published_movie["location"]
            assert movie["genreId"] == created_published_movie["genreId"]
            assert params["minPrice"] <= movie["price"] <= params["maxPrice"]

    def test_get_movie_id(self, login_admin, created_movie):  # запрашиваем конкретный фильм
        movie_id = created_movie["id"]
        response = login_admin.movies_api.get_movie_by_id(movie_id)
        assert response.status_code == 200
        response_data = response.json()
        assert movie_id == response_data["id"]
        assert response_data["name"] == created_movie["name"]
        assert response_data["description"] == created_movie["description"]
        assert response_data["genreId"] == created_movie["genreId"]

    def test_delete_movie_id(self, login_admin, movie_for_delete):  # удаляем фильм по id
        movie_id = movie_for_delete["id"]
        response = login_admin.movies_api.delete_movie_by_id(movie_id)
        assert response.status_code == 200
        response_data = response.json()
        assert movie_id == response_data["id"]

    def test_update_movie_body(self, login_admin, created_movie):  # обновляем имя и описание фильма
        movie_id = created_movie["id"]
        new_name = MovieData.generate_movie_data()
        update_data = {"name": new_name}
        response = login_admin.movies_api.patch_movie(movie_id, update_data)
        assert response.status_code == 200
        updated_movie = response.json()
        assert updated_movie["name"] == update_data["name"]



class TestMethodsNegative:
    def test_get_invalid_params(self, api_manager, login_admin):
        invalid_page = MovieData.invalid_movie_id() #получаем фильм с неверными параметрами
        response = login_admin.movies_api.get_movies(params={"page":invalid_page}, expected_status=400)
        assert response.status_code == 400

    def test_post_invalid(self, api_manager, login_admin): #создать фильм с пустым именем
        movie_data = MovieData.create_movie()
        movie_data["name"] = " "
        response = login_admin.movies_api.create_movie(movie_data, expected_status=400)
        assert response.status_code == 400
        error_data = response.json()
        assert "message" in error_data

    def test_post_duplicate_movie_name(self, created_movie, login_admin): #создаем дубликат
        movie_data = MovieData.create_movie()
        movie_data["name"] = created_movie["name"]
        response = login_admin.movies_api.create_movie(movie_data, expected_status=409)
        assert response.status_code == 409
        error_data = response.json()
        assert "message" in error_data

    def test_get_by_invalid_id(self, api_manager, login_admin): #получаем фильм с неправильным id
        fake_movie_id = MovieData.invalid_movie_id()
        response = login_admin.movies_api.get_movie_by_id(
            movie_id=fake_movie_id, expected_status=404
        )
        assert response.status_code == 404

    def test_delete_movie_negative_id(self, movie_for_delete, login_admin): #удаляем с неверным id
        fake_movie_id = MovieData.invalid_movie_id()
        response = login_admin.movies_api.delete_movie_by_id(
            movie_id=fake_movie_id, expected_status=404
        )
        assert response.status_code == 404

    def test_delete_movie_invalid_id(self, login_admin, movie_for_delete): #удаляем с неправильным форматом id
        response = login_admin.movies_api.delete_movie_by_id(
            movie_id="a", expected_status=404
        )
        assert response.status_code == 404 #Возвращает 404, ожидаемый результат по Swagger 400

    def test_update_movie_invalid_name(self, created_movie, login_admin): #создаем и обновляем фильм с пустым именем
        movie_data = created_movie["id"]
        update_movie_data = {"name": " "}
        response = login_admin.movies_api.patch_movie(
            movie_data, update_movie_data, expected_status=400
        )
        assert response.status_code == 400
