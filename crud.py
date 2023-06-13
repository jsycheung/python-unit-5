"""CRUD operations."""
from model import db, User, Movie, Rating, connect_to_db


def create_user(email, password):
    """Create and return a new user"""
    user = User(email=email, password=password)
    return user


def get_users():
    '''return all users'''
    return User.query.all()


def get_user_by_id(user_id):
    return User.query.get(int(user_id))


def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie"""
    movie = Movie(title=title, overview=overview,
                  release_date=release_date, poster_path=poster_path)
    return movie


def get_movies():
    '''return all movies'''
    return Movie.query.all()


def get_movie_by_id(movie_id):
    return Movie.query.get(int(movie_id))


def create_rating(score, movie, user):
    """
    Create and return a new rating.
    movie and user are Movie object and User object.
    """
    rating = Rating(score=score, movie=movie, user=user)
    return rating


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
