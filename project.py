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
# from flask.ext.httpauth import HTTPBasicAuth
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('/home/micond/udacity/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

THEMOVIEDB_KEY = json.loads(
    open('/home/micond/udacity/client_secrets.json', 'r').read())['web']['themoviedb_key']

engine = create_engine('sqlite:///mymoviedb.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token

# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/logout')
def logout():
    if 'username' in login_session:
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
            print "facebook"

        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
            print "google"

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        print "logout rest"
        

    return redirect(url_for('showCategories'))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(
            '/home/micond/udacity/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output



# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response



@app.route('/')
@app.route('/categories/')
def showCategories():
    categories = session.query(Category).all()
    lastMovies = session.query(Movie).order_by(desc(Movie.time_created)).limit(9)
#    if 'username' not in login_session:
#        return render_template('publicCategories.html', categories=categories, lastMovies=lastMovies)
#    else:
    return render_template('categories.html', categories=categories, lastMovies=lastMovies)

@app.route('/movies/')
def showMovies():
    movies = session.query(Movie).all()
#    if 'username' not in login_session:
#        return render_template('publicAllmovies.html', movies=movies)
#    else:        
    return render_template('allMovies.html', movies=movies)

@app.route('/category/<string:category_name>/')
def categorySelect(category_name):
    categoryName = session.query(Category.name).filter_by(name=category_name).one()
    print (categoryName)
    category = session.query(Category).filter_by(name=category_name).one()
    # categoryMovies = session.query(Movie).filter_by(category_name=category.name)   
    categoryMovies = session.query(Movie).outerjoin(Category,Movie.category_id == Category.id).filter(Category.name == category_name)
#    print categoryMovies[0]
#    if 'username' not in login_session:
#        return render_template('publicCategory.html', categoryMovies=categoryMovies, categoryName=categoryName)
#    else:
    return render_template('category.html', categoryMovies=categoryMovies, categoryName=categoryName)

    # return jsonify(items=[i.serialize for i in items])

@app.route('/last/JSON')
def lastAddedMovies():    
    item = session.query(Movie).order_by(desc(Movie.time_created)).limit(5)
    return jsonify(item=[i.serialize for i in item])

#@app.route('/movie/<int:movie_id>')
#def movie(movie_id):
#    movie = session.query(Movie).filter_by(id=movie_id)
    # movieCreator = session.query(Movie).filter_by(id=movie_id).first().created_by
    # movieCreator = login_session['email']
    # print movieCreator
#    if 'username' not in login_session:
#        return render_template('publicMovie.html', movie=movie)
#    else:
        # movieCreator = login_session['email']
#        print login_session['email']
#        return render_template('movie.html', movie=movie, movieCreator=login_session['email'])
    # return jsonify(item=[i.serialize for i in item])

@app.route('/movie/<string:movie_title>')
def movie(movie_title):
    movie = session.query(Movie).filter_by(title=movie_title)
    # movieCreator = session.query(Movie).filter_by(id=movie_id).first().created_by
    # movieCreator = login_session['email']
    # print movieCreator
 #   if 'username' not in login_session:
 #       return render_template('publicMovie.html', movie=movie)
 #   else:
#        # movieCreator = login_session['email']
#        print login_session['email']
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


@app.route('/movie/<string:movie_title>/edit/',
           methods=['GET', 'POST'])
def editMovie(movie_title):
    editedMovie = session.query(Movie).filter_by(title=movie_title).one()
    print "EDITMOVIE***********************************",editMovie
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
            'editMovie.html',  movie_title=movie_title, item=editMovie)





@app.route('/search/', methods=['GET','POST'])
def searchMovie():
    if request.method == 'POST':
        searchTitle = request.form['title']
        result = requests.get('https://api.themoviedb.org/3/search/movie?api_key={0}&language=en-US&query={1}&page=1&include_adult=false'.format(THEMOVIEDB_KEY, searchTitle))
        obj = json.loads(result.content)['results']
        return render_template('searchResults.html', obj=obj) 
    else:
        return render_template('search.html')


@app.route('/movie/<string:movie_title>/delete', methods=['GET', 'POST'])
def deleteMovie(movie_title):
    movieToDelete = session.query(Movie).filter_by(title=movie_title).one()
    if request.method == 'POST':
        session.delete(movieToDelete)
        session.commit()
        return redirect(url_for('showMovies'))
    else:
        return render_template('deleteMenuItem.html', item=movieToDelete)

@app.route('/addMovie/<string:searchTitle>/add', methods=['GET','POST'])
def addMovie(searchTitle):
    if request.method == 'POST':        
        result = requests.get(
            'https://api.themoviedb.org/3/search/movie?api_key={0}&language=en-US&query={1}&page=1&include_adult=false'.format(THEMOVIEDB_KEY, searchTitle))
        obj = json.loads(result.content)['results']
        return render_template('search.html')
    else:
        return render_template('addMovie.html', obj=obj)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
