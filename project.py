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

# Connect to Facebook
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    # 3 Gets info from fb clients secrets
    app_id = json.loads(open('/home/micond/udacity/client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('/home/micond/udacity/client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={0}&client_secret={1}&fb_exchange_token={2}'.format(app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # 4 Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    token = result.split(',')[0].split(':')[1].replace('"', '')
    url = 'https://graph.facebook.com/v2.8/me?access_token={0}&fields=name,id,email'.format(token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token
    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token={0}&redirect=0&height=200&width=200'.format(token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]
    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' "style = "width: 200px; height: 200px;border-radius:' \
        ' 150px;-webkit-border-radius: 150px;' \
        ' -moz-border-radius: 150px;"> '
    flash("Now logged in as {0}".format(login_session['username']))
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/{0}/permissions?access_token={1}'.format(facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"
    # End Facebook

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
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={0}'.format(access_token))
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
    return render_template('categories.html', categories=categories, lastMovies=lastMovies)

@app.route('/movies/')
def showMovies():
    movies = session.query(Movie).all()     
    return render_template('allMovies.html', movies=movies)

@app.route('/category/<string:category_name>/')
def categorySelect(category_name):
    categoryName = session.query(Category.name).filter_by(name=category_name).one()
    category = session.query(Category).filter_by(name=category_name).one()
    categoryMovies = session.query(Movie).outerjoin(
                    Genre, Movie.themoviedb_movie_id == Genre.movie_id).filter(Genre.genre_id == category.themoviedb_genre_id)
    return render_template('category.html', categoryMovies=categoryMovies, categoryName=categoryName)

@app.route('/last/JSON')
def lastAddedMovies():    
    item = session.query(Movie).order_by(desc(Movie.time_created)).limit(5)
    return jsonify(item=[i.serialize for i in item])

@app.route('/movie/<string:movie_title>')
def movie(movie_title):
    movie = session.query(Movie).filter_by(title=movie_title)
    return render_template('movie.html', movie=movie)

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
    if request.method == 'POST':
        print "edit movie POST"
        if request.form['backdrop_path']:
            print "path"
            editedMovie.backdrop_path = request.form['backdrop_path']
        if request.form['original_title']:
            print "title"
            editedMovie.original_title = request.form['original_title']
        if request.form['overview']:
            print "overview"
            editedMovie.overview = request.form['overview']
        if request.form['release_date']:
            print "release date"
            editedMovie.release_date = request.form['release_date']
        if request.form['poster_path']:
            print "path"
            editedMovie.poster_path = request.form['poster_path']
        if request.form['popularity']:
            print "popularity"
            editedMovie.popularity = request.form['popularity']
        if request.form['video']:
            print "video"
            editedMovie.video = request.form['video']
        if request.form['vote_average']:
            print "vote avarage"
            editedMovie.vote_average = request.form['vote_average']
        if request.form['vote_count']:
            print "vote count"
            editedMovie.vote_count = request.form['vote_count']
        session.add(editedMovie)
        session.commit()
        return movie(editedMovie.title)
    else:
        return render_template(
            'editMovie.html',  movie_title=movie_title, item=editedMovie)

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

@app.route('/addMovie/<string:searchTitle>/<int:tmvdb_id>/add', methods=['GET','POST'])
def addMovie(searchTitle,tmvdb_id):
    result = requests.get('https://api.themoviedb.org/3/movie/{0}?api_key={1}&language=en-US'.format(tmvdb_id,THEMOVIEDB_KEY))
    obj = json.loads(result.content)
    if request.method == 'POST':
        checkDuplicity = session.query(Movie.themoviedb_movie_id).filter_by(themoviedb_movie_id=tmvdb_id).all()
        if not checkDuplicity:
            genres_exists = session.query(Genre.movie_id).filter_by(
                movie_id=obj['id']).all()
            movie1 = Movie(
                    created_by=login_session['email'],                    
                    time_created=time.time(),
                    time_updated=time.time(),
                    backdrop_path=obj['backdrop_path'],                    
                    themoviedb_movie_id=obj['id'],
                    original_language=obj['original_language'],
                    original_title=obj['original_title'],
                    overview=obj['overview'],
                    release_date=obj['release_date'],
                    poster_path=obj['poster_path'],
                    popularity=obj['popularity'],
                    title=obj['title'],
                    video=obj['video'],
                    vote_average=obj['vote_average'],
                    vote_count=obj['vote_count'],
                    #category=obj['genres'][0]['id']                 
                    )
            session.add(movie1)
            session.commit()                    

            if not genres_exists:
                if obj['genres']:
                    for y in obj['genres']:
                        genre1 = Genre(
                            movie_id=obj['id'],
                            genre_id=y['id'],
                            title=obj['title'],                            
                        )
                        session.add(genre1)
                        session.commit()          

            for i in obj['genres']:
                q = session.query(Category).filter(Category.themoviedb_genre_id == i['id'])
                checkDuplicity2 = session.query(Category.themoviedb_genre_id).filter_by(themoviedb_genre_id=i['id']).all()
                if not checkDuplicity2:
                    category1 = Category(name = i['name'],
                                         themoviedb_genre_id = i['id'],
                                         created_by = login_session['email'],
                                         )
                    session.add(category1)
                    session.commit()

            return movie(obj['title'])
        else:
            return redirect(url_for('searchMovie'))
    else:
        return render_template('addMovie.html', obj=obj)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
