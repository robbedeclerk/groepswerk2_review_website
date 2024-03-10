import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI') or (f"postgresql://"
                                                           f"{os.environ.get('DB_USER')}:"
                                                           f"{os.environ.get('DB_USER_PASSWORD')}"
                                                           f"@{os.environ.get('localhost')}"
                                                           f"/{os.environ.get('DB_NAME')}"
                                                           )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

