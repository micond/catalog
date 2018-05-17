# Catalog Project

## Summary
Catalog application for favorite movies. User can add any movie from The Movie Database online provider. Application is using search/add function. Any movie in THE MOVIE DATABASE can be added to catalog. Categories are automatically populated according to movie specification. User can also edit specific fields for each movie he/she created. User can also delete each movie he/she created. Application also allows user to call list of all movies or last 5 movies added via API call in JSON format. Application is using google and facebook login. User needs to login via google or facebook to add/edit or delete movie items in the catalog.

#### Instructions
Program is writen in Python2.7 programing language. Run ```python2 project.py``` in terminal.
For more details please see Installation section.

### Catalog functions
Reporting tool is based on python script with these main functions:
* view movies in specific categories
* view all movies in catalog
* view specific category with all relevant movies
* view specific movie with more details in catalog (overview, ratings, ....)
* add / edit or delete movie in catalog
* API to show 5 last added movies in catalog
* API to show all movies in catalog

## Links to GitHub Repository (Master Branch)
* GitHub Project Repository: [https://github.com/micond/catalog](https://github.com/micond/catalog "GitHub project repository")

## Installation
Installation instructions are for Linux debian based distributions.

1. Download the GitHub zip file or clone the repository into your local workstation:
	* zip file [https://github.com/micond/catalog/archive/master.zip](https://github.com/micond/catalog/archive/master.zip "download zip file")
	* git clone [https://github.com/micond/catalog.git](https://github.com/micond/catalog.git "git clone repository")
2. Install [Python](https://www.python.org/)
3. Install python libraries via ```requirements.txt``` included with the app:
    run ```$ pip install -r requirements.txt``` in terminal.
4. Install python libraries manualy:
   - flask - [Installation Documentation](http://flask.pocoo.org/docs/0.12/installation/)
   - sqlalchemy - ```$ pip install SQLAlchemy``` 
   - oauth2client - [Installation Documentation](https://oauth2client.readthedocs.io/en/latest/)
   - httplib2 ```$ pip install httplib2```
   - requests ```$ pipenv install requests```
   - flask_httpauth ```$ pip install Flask-HTTPAuth```
   - passlib [Installation Documentation](http://passlib.readthedocs.io/en/stable/install.html)
4. For database install sqlite3 on your machine:
   - ```$ sudo apt-get update```
   - ```$ sudo apt-get install sqlite3 libsqlite3-dev```
5. Open terminal and navigate to the project.py file in your application's directory.
6. To run the application please run ```$ python project.py``` in terminal.
7. If  you would like to prepopulate catalog database with movie items for each available category run ```$ python DB_items_setup.py```

8. Fill client_secrets.json file with your google, facebook and themoviedb keys/secrets/ etc.. 
    - format of the file:
```json
{
    "web": {
    	"app_id":"Facebook app id",
    	"app_secret":"Facebook app secret",
        "client_id": "google id",
        "client_secret": "google secret",
        "project_id": "your project in google dev console",
        "client_email":"same as client_id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "redirect_uris": [
            "http://localhost:5000",
        ],
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/" + "dev google id",
        "javascript_origins": [
            "http://localhost:5000",
            "http://localhost",
            "https://accounts.google.com"
        ],
        "themoviedb_key": "The movie Database key"
    }
}    
```
## API Restfull
#### Method name: getlastMovies
- List last 5 movies added into the catalog database:
    - method type: GET
    - output format: JSON
    - endpoint: http://localhost:5000/API/v1/getlastMovies
    - response example:
```json
{
  "categoryMovies": [
    {
      "backdrop_path": "/bOGkgRGdhrBYJSLpXaxhXVstddV.jpg", 
      "category_id": 1, 
      "created_by": "Admin", 
      "id": 1, 
      "original_language": "en", 
      "original_title": "Avengers: Infinity War", 
      "overview": "As the Avengers and their allies have continued to protect the world from threats too large for any one hero to handle, a new danger has emerged from the cosmic shadows: Thanos. A despot of intergalactic infamy, his goal is to collect all six Infinity Stones, artifacts of unimaginable power, and use them to inflict his twisted will on all of reality. Everything the Avengers have fought for has led up to this moment - the fate of Earth and existence itself has never been more uncertain.", 
      "popularity": 541.656849, 
      "poster_path": "/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg", 
      "release_date": "2018-04-25", 
      "themoviedb_movie_id": 299536, 
      "time_created": 1526479468.823073, 
      "time_updated": 1526479468.823074, 
      "title": "Avengers: Infinity War", 
      "video": "0", 
      "vote_average": 8.5, 
      "vote_count": 3443
    }, 
```
#### Method name: getAllMovies
- List all movies available in db:
         - method type: GET
         - output format: JSON
         - endpoint: http://localhost:5000/API/v1/getAllMovies
    - response example:
```json
{
  "item": [
    {
      "backdrop_path": "/bOGkgRGdhrBYJSLpXaxhXVstddV.jpg", 
      "category_id": 1, 
      "created_by": "Admin", 
      "id": 1, 
      "original_language": "en", 
      "original_title": "Avengers: Infinity War", 
      "overview": "As the Avengers and their allies have continued to protect the world from threats too large for any one hero to handle, a new danger has emerged from the cosmic shadows: Thanos. A despot of intergalactic infamy, his goal is to collect all six Infinity Stones, artifacts of unimaginable power, and use them to inflict his twisted will on all of reality. Everything the Avengers have fought for has led up to this moment - the fate of Earth and existence itself has never been more uncertain.", 
      "popularity": 541.656849, 
      "poster_path": "/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg", 
      "release_date": "2018-04-25", 
      "themoviedb_movie_id": 299536, 
      "time_created": 1526479468.823073, 
      "time_updated": 1526479468.823074, 
      "title": "Avengers: Infinity War", 
      "video": "0", 
      "vote_average": 8.5, 
      "vote_count": 3443
    }, 
    {
      "backdrop_path": "/AlFqBwJnokrp9zWTXOUv7uhkaeq.jpg", 
      "category_id": 1, 
      "created_by": "Admin", 
      "id": 2, 
      "original_language": "en", 
      "original_title": "Black Panther", 
      "overview": "King T'Challa returns home from America to the reclusive, technologically advanced African nation of Wakanda to serve as his country's new leader. However, T'Challa soon finds that he is challenged for the throne by factions within his own country as well as without. Using powers reserved to Wakandan kings, T'Challa assumes the Black Panther mantel to join with girlfriend Nakia, the queen-mother, his princess-kid sister, members of the Dora Milaje (the Wakandan 'special forces') and an American secret agent, to prevent Wakanda from being dragged into a world war.", 
      "popularity": 276.266641, 
      "poster_path": "/uxzzxijgPIY7slzFvMotPv8wjKA.jpg", 
      "release_date": "2018-02-13", 
      "themoviedb_movie_id": 284054, 
      "time_created": 1526479468.849654, 
      "time_updated": 1526479468.849655, 
      "title": "Black Panther", 
      "video": "0", 
      "vote_average": 7.3, 
      "vote_count": 5209
    }
  ] 
```
#### Method name: getAvailableCategories
- List all categories available in db:
         - method type: GET
         - output format: JSON
         - endpoint: http://localhost:5000/API/v1/getAvailableCategories
    - response example:
```json
{
  "item": [
    {
      "created_by": "admin", 
      "id": 1, 
      "name": "Action"
    }, 
    {
      "created_by": "admin", 
      "id": 2, 
      "name": "Adventure"
    }, 
    {
      "created_by": "admin", 
      "id": 3, 
      "name": "Animation"
    }, 
    {
      "created_by": "admin", 
      "id": 4, 
      "name": "Comedy"
    }, 
    {
      "created_by": "admin", 
      "id": 5, 
      "name": "Crime"
    }, 
    {
      "created_by": "admin", 
      "id": 6, 
      "name": "Documentary"
    }, 
    {
      "created_by": "admin", 
      "id": 7, 
      "name": "Drama"
    }, 
    {
      "created_by": "admin", 
      "id": 8, 
      "name": "Family"
    }, 
    {
      "created_by": "admin", 
      "id": 9, 
      "name": "Fantasy"
    }, 
    {
      "created_by": "admin", 
      "id": 10, 
      "name": "History"
    }, 
    {
      "created_by": "admin", 
      "id": 11, 
      "name": "Horror"
    }, 
    {
      "created_by": "admin", 
      "id": 12, 
      "name": "Music"
    }, 
    {
      "created_by": "admin", 
      "id": 13, 
      "name": "Mystery"
    }, 
    {
      "created_by": "admin", 
      "id": 14, 
      "name": "Romance"
    }, 
    {
      "created_by": "admin", 
      "id": 15, 
      "name": "Science Fiction"
    }, 
    {
      "created_by": "admin", 
      "id": 16, 
      "name": "TV Movie"
    }, 
    {
      "created_by": "admin", 
      "id": 17, 
      "name": "Thriller"
    }, 
    {
      "created_by": "admin", 
      "id": 18, 
      "name": "War"
    }, 
    {
      "created_by": "admin", 
      "id": 19, 
      "name": "Western"
    }
  ]
}
```
#### Method name: getMovieDetails
- List movie details:
         - method type: GET
         - output format: JSON
         - endpoint: http://localhost:5000/API/v1/getMovieDetails/<movie_title>
    - response example:
```json
{
  "item": [
    {
      "backdrop_path": "/mhdeE1yShHTaDbJVdWyTlzFvNkr.jpg", 
      "category_id": 2, 
      "created_by": "Admin", 
      "id": 6, 
      "original_language": "en", 
      "original_title": "Zootopia", 
      "overview": "Determined to prove herself, Officer Judy Hopps, the first bunny on Zootopia's police force, jumps at the chance to crack her first case - even if it means partnering with scam-artist fox Nick Wilde to solve the mystery.", 
      "popularity": 173.225696, 
      "poster_path": "/sM33SANp9z6rXW8Itn7NnG1GOEs.jpg", 
      "release_date": "2016-02-11", 
      "themoviedb_movie_id": 269149, 
      "time_created": 1526479469.935533, 
      "time_updated": 1526479469.935533, 
      "title": "Zootopia", 
      "video": "0", 
      "vote_average": 7.7, 
      "vote_count": 7240
    }
  ]
}
```
#### Method name: getCategoryMovies
- List all movies in specific category:
         - method type: GET
         - output format: JSON
         - endpoint: http://localhost:5000/API/v1/getCategoryMovies/<category_name>
    - response example:
```json
{
  "categoryMovies": [
    {
      "backdrop_path": "/mhdeE1yShHTaDbJVdWyTlzFvNkr.jpg", 
      "category_id": 2, 
      "created_by": "Admin", 
      "id": 6, 
      "original_language": "en", 
      "original_title": "Zootopia", 
      "overview": "Determined to prove herself, Officer Judy Hopps, the first bunny on Zootopia's police force, jumps at the chance to crack her first case - even if it means partnering with scam-artist fox Nick Wilde to solve the mystery.", 
      "popularity": 173.225696, 
      "poster_path": "/sM33SANp9z6rXW8Itn7NnG1GOEs.jpg", 
      "release_date": "2016-02-11", 
      "themoviedb_movie_id": 269149, 
      "time_created": 1526479469.935533, 
      "time_updated": 1526479469.935533, 
      "title": "Zootopia", 
      "video": "0", 
      "vote_average": 7.7, 
      "vote_count": 7240
    }, 
    {
      "backdrop_path": "/askg3SMvhqEl4OL52YuvdtY40Yb.jpg", 
      "category_id": 2, 
      "created_by": "Admin", 
      "id": 8, 
      "original_language": "en", 
      "original_title": "Coco", 
      "overview": "Despite his family\u2019s baffling generations-old ban on music, Miguel dreams of becoming an accomplished musician like his idol, Ernesto de la Cruz. Desperate to prove his talent, Miguel finds himself in the stunning and colorful Land of the Dead following a mysterious chain of events. Along the way, he meets charming trickster Hector, and together, they set off on an extraordinary journey to unlock the real story behind Miguel's family history.", 
      "popularity": 95.476977, 
      "poster_path": "/eKi8dIrr8voobbaGzDpe8w0PVbC.jpg", 
      "release_date": "2017-10-27", 
      "themoviedb_movie_id": 354912, 
      "time_created": 1526479469.986587, 
      "time_updated": 1526479469.986587, 
      "title": "Coco", 
      "video": "0", 
      "vote_average": 7.8, 
      "vote_count": 4397
    }
  ]
}
```
## Tools / Techniques
- Python 2.7
- mysql
- VM Linux - Debian distribution

## List of Resources

- [Python](https://www.python.org/)
- [PEP8 style guide ](https://www.python.org/dev/peps/pep-0008/)
- [Postgresql](https://www.postgresql.org/)
- [Oracle - VirtualBox Linux - Debian distribution](https://www.virtualbox.org/)
- Recommended Linux Distributions [Ubuntu](https://www.ubuntu.com/) , [Mint](https://linuxmint.com/)
