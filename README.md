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
3. Install python libraries:
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

8. Create client_secrets.json file, fill with your google, facebook and themoviedb keys/secrets/ etc.. and correct the path to the file in project.py on lines: 26,31,107,110,184
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
- List all movies in catalog database:
    - method type: GET
    - output format: JSON
    - endpoint: http://localhost:5000/movies/JSON
- List last 5 movies added into the catalog database:
    - method type: GET
    - output format: JSON
    - endpoint: http://localhost:5000/last/JSON

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