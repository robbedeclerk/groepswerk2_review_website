from flask import Flask
from ..config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os



app = Flask(__name__)
app.config.from_object(Config)
movie_db = SQLAlchemy(app)

from ..app import routes, models