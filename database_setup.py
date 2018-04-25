import datetime
import json
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, func, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    themoviedb_genre_id = Column(Integer)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    created_by = Column(String(80), nullable=False)
    time_created = Column(Integer)
    time_updated = Column(Integer)
    backdrop_path = Column(String(250)) 
    themoviedb_movie_id = Column(Integer)
    children = relationship("Genre")
    original_language = Column(String(4))
    original_title = Column(String(250))
    overview = Column(String(250))
    release_date = Column(String(15))
    poster_path = Column(String(250))
    popularity = Column(Integer)
    title = Column(String(80), nullable=False)
    video = Column(String(250))
    vote_average = Column(Integer)
    vote_count = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    children = relationship("Genre")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'created_by': self.user_id,
            'time_created': self.time_created,
            'time_updated': self.time_updated,
            'backdrop_path': self.backdrop_path,      
            'themoviedb_movie_id': self.themoviedb_movie_id,
            'original_language': self.original_language,            
            'original_title': self.original_title,
            'overview': self.overview,
            'release_date': self.release_date,
            'poster_path': self.poster_path,
            'popularity': self.popularity,
            'title': self.title,
            'video': self.video,
            'vote_average': self.vote_average,
            'vote_count': self.vote_count,
            'category_id': self.category_id,
            # 'category': self.category,        
        }


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movie.themoviedb_movie_id"))
    genre_id = Column(Integer)
    title = Column(String(80), nullable=False)
    

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'genre_id': self.genre_id,
            'title': self.title,
        }

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

engine = create_engine('sqlite:///mymoviedb.db')


Base.metadata.create_all(engine)
