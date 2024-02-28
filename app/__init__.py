from flask import Flask
from ..config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config.from_object(Config)
movie_db = SQLAlchemy(app)
db_params = {
    'dbname': 'the database name', 'user': 'the username', 'password': 'the password', 'host': 'the host',
    'port': 'the port'}


from ..app import routes, models
