import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/moviedb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

