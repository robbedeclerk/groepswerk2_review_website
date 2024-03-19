from app import app, db, login
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import sessionmaker, relationship
from datetime import timezone, datetime
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_login import UserMixin
import jwt



@login.user_loader
def load_user(id):
    """
    This function is used to load the user object from the database.
    The decorator indicates that the function is a callback for a user,
    it retrieves the user from the database session based on the provided id.
    """
    return db.session.get(User, int(id))

upvotes = db.Table('upvotes',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                   db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
                   )
downvotes = db.Table('downvotes',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
                     )

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
    country: so.Mapped[str] = so.mapped_column(sa.String(55), index=True)


    posts: so.WriteOnlyMapped['Post'] = so.relationship('Post', back_populates='author')

    # Define relationship with posts that this user has upvoted
    upvoted_posts = relationship("Post", secondary="upvotes", back_populates="upvoters")
    # Define relationship with posts that this user has downvoted
    downvoted_posts = relationship("Post", secondary="downvotes", back_populates="downvoters")
    def __repr__(self):
        """
        Function defines string representation of the user object.
        """
        return f"User: {self.username}, {self.email}, {self.password_hash}, {self.firstname}, {self.family_name}"

    def upvote_post(self, post):
        self.upvoted_posts.append(post)

    def downvote_post(self, post):
        self.downvoted_posts.append(post)
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
            return None
        return db.session.get(User, id)


class Post(db.Model):
    """
    The posts table in the postgress database.
    """
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    # title: so.Mapped[str] = so.mapped_column(sa.String(120))
    post_message: so.Mapped[str] = so.mapped_column(sa.Text)
    rating: so.Mapped[int] = so.mapped_column(
        sa.Integer)  # While implementing in the code we have to add min =0 and max = 10

    # upvote: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)  # implement thumb up count.
    # downvote: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)  # implement thumbs down count.
    time_of_posting: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    movie_id: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    is_movie: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    # Define relationship with users who downvoted this post
    downvoters = relationship("User", secondary="downvotes", back_populates="downvoted_posts")
    # Define relationship with users who upvoted this post
    upvoters = relationship("User", secondary="upvotes", back_populates="upvoted_posts")

    def __repr__(self):
        """
        Function defines string representation of the Post object.
        """
        return (f"The post contains: "
                f"{self.post_message}, "
                f"{self.rating}, "
                f"{self.upvote_count()}, "
                f"{self.downvote_count()}, "
                f"{self.time_of_posting}")

    def upvote_count(self):
        return len(self.upvoters)

    def downvote_count(self):
        return len(self.downvoters)
