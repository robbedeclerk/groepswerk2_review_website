from app import app, db, login
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import timezone, datetime, time
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_login import UserMixin
import jwt

# votes = sa.Table('vote', db.metadata,
#                  sa.Column('voter_id', sa.Integer,
#                            sa.ForeignKey('user.id'),
#                            primary_key=True)
#                  )


@login.user_loader
def load_user(id):
    """
    This function is used to load the user object from the database.
    The decorator indicates that the function is a callback for a user,
    it retrieves the user from the database session based on the provided id.
    """
    return db.session.get(User, int(id))


def get_posts(movie_id, is_movie):
    """
    This function gets all posts for a specific movie or user.
    """
    return db.session.query(Post).filter(Post.movie_id == movie_id, Post.is_movie == is_movie)


class User(UserMixin, db.Model):
    """
    The user table in the postgres database
    """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(60), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    firstname: so.Mapped[str] = so.mapped_column(sa.String(60))
    family_name: so.Mapped[str] = so.mapped_column(sa.String(60), index=True)

    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    # voted: so.WriteOnlyMapped['User'] = so.relationship(secondary=votes, primaryjoin=(votes.c.voter_id == id),
    #                                                     back_populates='votes')

    def __repr__(self):
        """
        Function defines string representation of the user object.
        """
        return f"User: {self.username}, {self.email}, {self.password_hash}, {self.firstname}, {self.family_name}"

    def set_password(self, password):
        """
        Function generates a hashed password.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if the password is correct.
        """
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """Generate avatar link"""
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def get_reset_password_token(self, expires_in=600):
        """
        Function generates a token for password reset.
        """

        def get_reset_password_token(self, expires_in=600):
            return jwt.encode(
                {'reset_password': self.id, 'exp': time() + expires_in},
                app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        """
        Verify the reset password token and return the associated user.
        If the token is invalid, return None.
        """
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, id)


class Address(UserMixin, db.Model):
    """
    The address info of the Users stored in an other table for efficiency.
    """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    country: so.Mapped[str] = so.mapped_column(sa.String(55), index=True)
    city: so.Mapped[str] = so.mapped_column(sa.String(85), index=True)
    postalcode: so.Mapped[str] = so.mapped_column(sa.String(20))
    street: so.Mapped[str] = so.mapped_column(sa.String(58))
    house_number: so.Mapped[int] = so.mapped_column(sa.Integer)
    address_suffix: so.Mapped[str] = so.mapped_column(sa.String(10))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)  # Linked to the User id

    def __repr__(self):
        """
        Function defines string representation of the address object.
        """
        return (f'The Address is: {self.country}, {self.city}, {self.street}, '
                f'{self.postalcode}, {self.house_number}, {self.address_suffix}')


class Post(db.Model):
    """
    The posts table in the postgress database.
    """
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    # title: so.Mapped[str] = so.mapped_column(sa.String(120))
    post_message: so.Mapped[str] = so.mapped_column(sa.Text)
    rating: so.Mapped[int] = so.mapped_column(
        sa.Integer)  # While implementing in the code we have to add min =0 and max = 10
    upvote: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)  # implement thumb up count.
    downvote: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)  # implement thumbs down count.
    time_of_posting: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    movie_id: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    is_movie: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        """
        Function defines string representation of the Post object.
        """
        return (f"The post contains: "
                f"{self.post_message}, "
                f"{self.rating}, "
                f"{self.upvote}, "
                f"{self.downvote}, "
                f"{self.time_of_posting}")
