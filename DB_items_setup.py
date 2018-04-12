import time
import json
import jsonify
import requests
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, Movie, Genre

engine = create_engine('sqlite:///mymoviedb.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

THEMOVIEDB_KEY = json.loads(
    open('client_secrets.json', 'r').read())['web']['themoviedb_key']

genreslist = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key={0}&language=en-US".format(THEMOVIEDB_KEY))
obj = json.loads(genreslist.content)
last_category = obj['genres'][-1]['name']

for i in obj['genres']:    
    getgenres = requests.get("https://api.themoviedb.org/3/genre/{0}/movies?api_key={1}&language=en-US&include_adult=false&sort_by=created_at.asc".format(i['id'],THEMOVIEDB_KEY))
    results = json.loads(getgenres.content)['results']  
    print "Adding movies to Category: ", i['name']
    category1 = Category(name=i['name'], themoviedb_genre_id=i['id'])
    session.add(category1)
    session.commit()
    actual_category = category1.id    
    movie_count = 0
    
    while movie_count <= 4:
        for j in results:
            
            exists = session.query(Movie.themoviedb_movie_id).filter_by(
                themoviedb_movie_id=j['id']).all()        

            genres_exists = session.query(Genre.movie_id).filter_by(
                movie_id=j['id']).all()

            movie_count = session.query(Movie.id).filter_by(
                category_id=actual_category).count()

            if not exists and movie_count <= 4:
                print " -",j['title']
                movie1 = Movie(
                    created_by="Admin",
                    time_created=time.time(),
                    time_updated=time.time(),
                    backdrop_path=j['backdrop_path'],                    
                    themoviedb_movie_id = j['id'],
                    original_language=j['original_language'],
                    original_title=j['original_title'],
                    overview=j['overview'],
                    release_date=j['release_date'],
                    poster_path=j['poster_path'],
                    popularity=j['popularity'],
                    title=j['title'],
                    video=j['video'],
                    vote_average=j['vote_average'],
                    vote_count=j['vote_count'],
                    category=category1
                    )
                session.add(movie1)
                session.commit()  

                if not genres_exists:
                    for y in j['genre_ids']:
                        genre1 = Genre(
                            movie_id=j['id'],
                            genre_id=y,
                            title=j['title'],
                        )
                        session.add(genre1)
                        session.commit()      

                if movie_count == 4 and i['name'] == last_category:
                        print "Database setup completed. Congrats!!!"
                    

   
