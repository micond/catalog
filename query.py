import json
import jsonify
import requests
from sqlalchemy import create_engine, select, func, text
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Movie, Genre

engine = create_engine('sqlite:///mymoviedb.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

THEMOVIEDB_KEY = json.loads(
    open('client_secrets.json', 'r').read())['web']['themoviedb_key']

# movie_count = session.query(Movie.id).filter_by(Category.id).count()
# print movie_count

exists = session.query(Movie).filter_by(
    id=93)
print exists

                         
# sql = text('select count() from movie where category_id = 1')
# result = session.execute(sql)
# names = []
# for row in result:
#     names.append(row[0])

# print result
   
