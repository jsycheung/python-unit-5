"""Script to seed database from starter code"""
import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

db_uri, db_username, db_password = (os.environ["POSTGRES_URI"], os.environ["POSTGRES_USERNAME"], os.environ["POSTGRES_PASSWORD"])

# os.system(f"dropdb -U postgres ratings")
cmd1 = f'SET "PGPASSWORD={db_password}"'
cmd2 = f'dropdb -U {db_username} ratings'
cmd3 = f'createdb -U {db_username} ratings'
os.system(cmd1 + ' && ' + cmd2)
os.system(cmd1 + ' && ' + cmd3)
model.connect_to_db(server.app)
model.db.create_all()

# Load movies data from JSON file
with open("data/movies.json") as f:
    movie_data = json.loads(f.read())

# Create moview and store them in a list
movies_in_db = []
for movie in movie_data:
    title, overview, poster_path = (movie["title"], movie["overview"], movie["poster_path"])
    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")
    new_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(new_movie)

model.db.session.add_all(movies_in_db)
model.db.session.commit()