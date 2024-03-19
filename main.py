from app import app, db, mail, login, migrate
from app.models import User, Post #Address is er uit gehaald
import sqlalchemy as sa
import sqlalchemy.orm as so
