import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Movie

engine = create_engine('sqlite:///mymoviedb.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Menu for UrbanBurger
category1 = Category(name="Action")

session.add(category1)
session.commit()

movie1 = Movie(
                title="Rogue One: A Star Wars Story", 
                overview="A rogue band of resistance fighters unite for a mission to steal the Death Star             plans and bring a new hope to the galaxy.",
                poster="/qjiskwlV1qQzRCjpV0cL9pEMF9a.jpg", 
                homepage="http://www.starwars.com/films/rogue-one",
                original_title="Rogue One: A Star Wars Story",
                moviedb_id="330459", 
                category=category1)

session.add(movie1)
session.commit()