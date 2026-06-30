from datetime import datetime

from pydantic import BaseModel


class GenreModel(BaseModel):
    name: str


class MovieModel(BaseModel):
    id: int
    name: str
    description: str
    genreId: int
    imageUrl: str | None = None
    price: int
    rating: float
    location: str
    published: bool
    createdAt: datetime
    genre: GenreModel


class MoviesResponseModel(BaseModel):
    movies: list[MovieModel]
    count: int
    page: int
    pageSize: int
    pageCount: int
