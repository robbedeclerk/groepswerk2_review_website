import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI') or (f"postgresql://"
                                                           f"{os.environ.get('DB_USER')}:"
                                                           f"{os.environ.get('DB_USER_PASSWORD')}"
                                                           f"@{os.environ.get('DB_HOST')}"
                                                           f"/{os.environ.get('DB_NAME')}"
                                                           )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
