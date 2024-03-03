from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
<<<<<<< HEAD

=======
>>>>>>> 0c757e84895f0cdd8a977791bc14ed4632ea9438

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
<<<<<<< HEAD
#login = LoginManager(app)
=======
# login = LoginManager(app)
>>>>>>> 0c757e84895f0cdd8a977791bc14ed4632ea9438

from app import routes, models, tmdb_api
