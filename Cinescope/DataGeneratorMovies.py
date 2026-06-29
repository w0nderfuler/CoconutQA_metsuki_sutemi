from faker import Faker
import random
import string
from uuid import uuid4
import datetime
from Cinescope.resources.roles import Roles
fake = Faker("ru_Ru")


class MovieData:
    @staticmethod
    def create_movie():
        location = ["SPB", "MSK"]
        return {
            "name": f"Movie {fake.uuid4()[:8]}",
            "imageUrl": fake.url(),
            "price": fake.random_int(min=100, max=1000),
            "description": fake.sentence(nb_words=8),
            "location": fake.random_element(elements=location),
            "published": fake.boolean(),
            "genreId": fake.random_element(elements=range(2, 5)),
        }

    @staticmethod
    def generate_movie_data():
        return fake.catch_phrase()

    @staticmethod
    def generate_random_int(max_value=10):
        return fake.random_int(min=1, max=max_value)

    @staticmethod
    def generate_account_transaction_data(user_prefix: str, balance: int) -> dict:
        return {
            "user": f"{user_prefix}_{fake.uuid4()[:8]}",
            "balance": balance,
        }

    @staticmethod
    def invalid_movie_id():
        return fake.random_int(min=-100, max=-1)

    @staticmethod
    def generate_email():
        return f"test_{uuid4().hex}@gmail.com"

    @staticmethod
    def generate_invalid_email():
        return f"test_{uuid4().hex}gmail.com"

    @staticmethod
    def generate_password(length=12):
        letters = string.ascii_letters
        digits = string.digits

        password_chars = [
            random.choice(letters),
            random.choice(digits),
        ]

        allowed_chars = letters + digits

        password_chars += random.choices(allowed_chars, k=length - 2)
        random.shuffle(password_chars)

        return "".join(password_chars)

    @staticmethod
    def generate_password_repeat(length=12):
        letters = string.ascii_letters
        digits = string.digits

        password_chars = [
            random.choice(letters),
            random.choice(digits),
        ]

        allowed_chars = letters + digits

        password_chars += random.choices(allowed_chars, k=length - 2)
        random.shuffle(password_chars)
        return "".join(password_chars)

    @staticmethod
    def generate_password_min(length=3):
        letters = string.ascii_letters
        digits = string.digits

        password_chars = [
            random.choice(letters),
            random.choice(digits),
        ]

        allowed_chars = letters + digits

        password_chars += random.choices(allowed_chars, k=length - 2)
        random.shuffle(password_chars)
        return "".join(password_chars)

    @staticmethod
    def generate_user_data() -> dict:
        return {
            "id": f'{uuid4()}',
            "email": MovieData.generate_email(),
            "full_name": f"{fake.first_name()} {fake.last_name()}",
            "password": MovieData.generate_password(),
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "verified": False,
            "banned": False,
            "roles": f"{{{Roles.USER.value}}}"

        }
