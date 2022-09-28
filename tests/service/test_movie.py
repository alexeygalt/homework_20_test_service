from unittest.mock import MagicMock
import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    movie_one = Movie(id=1, title='Самый', description='Лучший', trailer='Фильм', year=2005, rating=5.2,
                      genre_id=1,
                      director_id=1)
    movie_two = Movie(id=1, title='Это', description='Плохой', trailer='Сериал', year=2007, rating=6.4,
                      genre_id=2,
                      director_id=2)
    movie_three = Movie(id=3, title='Фильм', description='Получил', trailer='Оскар', year=2013, rating=7.3,
                        genre_id=3,
                        director_id=3)
    dict_objects = {1: movie_one, 2: movie_two, 3: movie_three}
    movie_dao.get_one = MagicMock(side_effect=dict_objects.get)
    movie_dao.get_all = MagicMock(return_value=[movie_one, movie_two, movie_three])
    movie_dao.create = MagicMock(return_value=Movie(id=1))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()
    movie_dao.partially_update = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0

    def test_create(self):
        movie_data ={
            "title": "New_film",
            "description": "new_description",
            "trailer": "in far far galaxy",
            "year": 2026,
            "rating": 11
        }
        movie = self.movie_service.create(movie_data)
        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_data = {
            "id": 1,
            "title": "Film_update",
            "description": "desc",
            "trailer": "...",
            "year": 2025,
            "rating": 11
        }
        self.movie_service.update(movie_data)

    def test_partially_update(self):
        movie_data = {
            "id": 3,
            "title": "Movie_update"
        }
        self.movie_service.partially_update(movie_data)

    def test_get_one_out(self):
        movie = self.movie_service.get_one(100)
        assert movie is None


