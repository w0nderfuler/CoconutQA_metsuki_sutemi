from faker import Faker

fake = Faker("ru_Ru")
class MovieData:
    @staticmethod
    def create_movie():
        location = ["SPB", "MSK"]
        return {
            "name": fake.catch_phrase(),
            "imageUrl": fake.url(),
            "price": fake.random_int(min=100, max=1000),
            "description": fake.text(),
            "location": fake.random_element(elements=location),
            "published": fake.boolean(),
            "genreId": fake.random_element(elements=range(1, 6)),
        }

    @staticmethod
    def generate_movie_data():
        return fake.catch_phrase()

    @staticmethod
    def invalid_movie_id():
        return fake.random_int(min=-100, max=-1)