from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, make_response, abort, g
from sqlalchemy import create_engine, Column, Integer,String, Boolean, ForeignKey, DateTime, Sequence, Float, desc
from sqlalchemy.orm import sessionmaker,defer, undefer
from database_setup import Category, Base, Movie, Genre, User
import datetime
import time
import json
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
import random
import string
from flask.httpauth import HTTPBasicAuth 


auth = HTTPBasicAuth()

# CLIENT_ID = json.loads(
#     open('client_secrets.json', 'r').read())['web']['client_id']
# APPLICATION_NAME = "Restaurant Menu Application"


engine = create_engine('sqlite:///mymoviedb.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@auth.verify_password
def verify_password(username, password):
    print "Looking for user %s" % username
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print "User not found"
        return False
    elif not user.verify_password(password):
        print "Unable to verfy password"
        return False
    else:
        g.user = user
        return True


@app.route('/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        print "missing arguments"
        abort(400)

    if session.query(User).filter_by(username=username).first() is not None:
        print "existing user"
        user = session.query(User).filter_by(username=username).first()
        # , {'Location': url_for('get_user', id = user.id, _external = True)}
        return jsonify({'message': 'user already exists'}), 200

    user = User(username=username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    # , {'Location': url_for('get_user', id = user.id, _external = True)}
    return jsonify({'username': user.username}), 201


@app.route('/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@app.route('/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@app.route('/')
@app.route('/categories/')
def showCategories():
    categories = session.query(Category).all()
    lastMovies = session.query(Movie).order_by(desc(Movie.time_created)).limit(5)
    return render_template('categories.html', categories=categories, lastMovies=lastMovies)

@app.route('/movies/')
def showMovies():
    movies = session.query(Movie).all()    
    return render_template('allMovies.html', movies=movies)

@app.route('/category/<int:category_id>/')
def categorySelect(category_id):
    categoryName = session.query(Category.name).filter_by(id=category_id).one()
    print categoryName
    category = session.query(Category).filter_by(id=category_id).one()
    categoryMovies = session.query(Movie).filter_by(category_id=category.id)
    return render_template('category.html', categoryMovies=categoryMovies, categoryName=categoryName)
    # return jsonify(items=[i.serialize for i in items])

@app.route('/last/JSON')
def lastAddedMovies():    
    item = session.query(Movie).order_by(desc(Movie.time_created)).limit(5)
    return jsonify(item=[i.serialize for i in item])

@app.route('/movie/<int:movie_id>')
def movie(movie_id):
    movie = session.query(Movie).filter_by(id=movie_id)
    return render_template('movie.html', movie=movie)
    # return jsonify(item=[i.serialize for i in item])

@app.route('/movie/new/', methods=['GET', 'POST'])
def newMovie():
    if request.method == 'POST':
        newMovie = Movie(
            title=request.form['title'], overview=request.form['overview'], category_id=request.form['category_id'], time_created=time.time())
        session.add(newMovie)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newMovie.html')

@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')


@app.route('/movie/<int:movie_id>/edit/',
           methods=['GET', 'POST'])
def editMovie(movie_id):
    editedMovie = session.query(Movie).filter_by(id=movie_id).one()
    if request.method == 'POST':
        editedMovie.time_updated = time.time()
        if request.form['backdrop_path']:
            editedMovie.backdrop_path = request.form['backdrop_path']
        if request.form['themoviedb_movie_id']:
            editedMovie.themoviedb_movie_id = request.form['themoviedb_movie_id']
        if request.form['original_title']:
            editedMovie.original_title = request.form['original_title']
        if request.form['overview']:
            editedMovie.overview = request.form['overview']
        if request.form['release_date']:
            editedMovie.release_date = request.form['release_date']
        if request.form['poster_path']:
            editedMovie.poster_path = request.form['poster_path']
        if request.form['popularity']:
            editedMovie.popularity = request.form['popularity']
        if request.form['title']:
            editedMovie.title = request.form['title']
        if request.form['video']:
            editedMovie.video = request.form['video']
        if request.form['vote_average']:
            editedMovie.vote_average = request.form['vote_average']
        if request.form['vote_count']:
            editedMovie.vote_count = request.form['vote_count']
        if request.form['category_id']:
            editedMovie.category_id = request.form['category_id']
        session.add(editedMovie)
        session.commit()
        return redirect(url_for('showMovies'))
    else:
        return render_template(
            'editMovie.html',  movie_id=movie_id, item=editMovie)


@app.route('/movie/<int:movie_id>/delete',
           methods=['GET', 'POST'])
def deleteMovie(movie_id):
    movieToDelete = session.query(Movie).filter_by(id=movie_id).one()
    if request.method == 'POST':
        session.delete(movieToDelete)
        session.commit()
        return redirect(url_for('showMovies'))
    else:
        return render_template('deleteMenuItem.html', item=movieToDelete)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
