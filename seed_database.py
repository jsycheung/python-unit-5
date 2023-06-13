"""Script to seed database from starter code"""
import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

cmd2 = 'dropdb -U postgres ratings'
cmd3 = 'createdb -U postgres ratings'
model.connect_to_db(server.app)
model.db.create_all()

# Load movies data from JSON file
with open("data/movies.json") as f:
    movie_data = json.loads(f.read())

# Create moview and store them in a list
movies_in_db = []
for movie in movie_data:
    title, overview, poster_path = (
        movie["title"], movie["overview"], movie["poster_path"])
    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")
    new_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(new_movie)

model.db.session.add_all(movies_in_db)

for n in range(10):
    email = f'user{n}@test.com'
    password = 'test'
    user = crud.create_user(email, password)
    model.db.session.add(user)

    for _ in range(10):
        random_movie = choice(movies_in_db)
        score = randint(1, 5)

        rating = crud.create_rating(score, random_movie, user)
        model.db.session.add(rating)

model.db.session.commit()
