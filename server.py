"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db, Movie, User, Rating
import crud
from jinja2 import StrictUndefined
from forms import RatingForm

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

user_id = None


@app.context_processor
def inject_user():
    return dict(user_id=user_id)


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/movies")
def all_movies():
    '''view all movies'''
    movies = crud.get_movies()
    return render_template("all_movies.html", movies=movies)


@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    '''Show details on a particular movie'''
    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie=movie)


@app.route("/users")
def all_users():
    '''view all users'''
    users = crud.get_users()
    return render_template("all_users.html", users=users)


@app.route("/users/<user_id>")
def show_user(user_id):
    '''show details on a particular user'''
    user = crud.get_user_by_id(user_id)
    return render_template("user_details.html", user=user)


@app.route("/users", methods=["POST"])
def register_user():
    '''create a new user'''
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    return redirect("/")


@app.route("/login", methods=["POST"])
def login_user():
    '''log in an existing user'''
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if user:
        if crud.check_login_password(user, password):
            flash("Logged in successfully!")
            global user_id
            user_id = user.user_id
        else:
            flash("Wrong password, please try again.")
    else:
        flash("No registered user, please create an account.")
    return redirect("/")


@app.route("/rating")
def rating():
    if user_id == None:
        flash("Please log in before rating a movie!")
        return redirect("/")
    else:
        rating_form = RatingForm()
        movies = crud.get_movies()
        rating_form.update_movies(movies)
        return render_template("rating.html", rating_form=rating_form)


@app.route("/rating", methods=["POST"])
def submit_rating():
    rating_form = RatingForm()
    user = User.query.filter(User.user_id == user_id).first()
    movie_id = rating_form.movie_selection.data
    movie = Movie.query.filter(Movie.movie_id == movie_id).first()
    score = rating_form.score.data
    rating = crud.create_rating(score, movie, user)
    db.session.add(rating)
    db.session.commit()
    flash("Rating successfully added!")
    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
