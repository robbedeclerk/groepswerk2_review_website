import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI') or (f"postgresql://"
    #                                                        f"{os.environ.get('DB_USER')}:"
    #                                                        f"{os.environ.get('DB_USER_PASSWORD')}"
    #                                                        f"@{os.environ.get('localhost')}"
    #                                                        f"/{os.environ.get('DB_NAME')}"
    #                                                        )
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI') or (f"postgresql://"
                                                           f"{os.getenv('DB_USER')}:"
                                                           f"{os.getenv('DB_USER_PASSWORD')}"
                                                           f"@localhost"
                                                           f"/{os.getenv('DB_NAME')}"
                                                           )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

