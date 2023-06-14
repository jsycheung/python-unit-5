from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange


class RatingForm(FlaskForm):
    movie_selection = SelectField("Movie name: ", validators=[DataRequired()])
    score = IntegerField("Rating on the scale of 1 (worst) to 5 (best): ", validators=[
                         DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField("submit")

    def update_movies(self, movies):
        self.movie_selection.choices = [
            (movie.movie_id, movie.title) for movie in movies]
