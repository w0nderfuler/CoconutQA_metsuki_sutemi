from faker import Faker


class MovieData:
    @staticmethod
    def create_movie():
        fake = Faker(locale="ru_RU")
        location = ["SPB", "MSK"]
        return {
            "name": fake.name(),
            "imageUrl": fake.url(),
            "price": fake.random_int(min=100, max=1000),
            "description": fake.text(),
            "location": fake.random_element(elements=location),
            "published": fake.boolean(),
            "genreId": fake.random_element(elements=range(1, 6)),
        }
