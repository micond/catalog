import json
import jsonify
import requests
from sqlalchemy import create_engine, exists
from sqlalchemy.sql import text, and_
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Movie, Genre

engine = create_engine('sqlite:///mymoviedb.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

THEMOVIEDB_KEY = json.loads(
    open('client_secrets.json', 'r').read())['web']['themoviedb_key']

exists = session.query(Movie.id).filter_by(
    themoviedb_movie_id=284054).all()

print exists    
