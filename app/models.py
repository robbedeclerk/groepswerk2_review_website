from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import movie_db
from datetime import timezone, datetime



class User(movie_db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(60), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    firstname: so.Mapped[str] = so.mapped_column(sa.String(60))
    family_name: so.Mapped[str] = so.mapped_column(sa.String(60), index=True)

    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='Author')

    def __repr__(self):
        return f"User: {self.username}"


class Address(movie_db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    country: so.Mapped[str] = so.mapped_column(sa.String(55), index=True)
    city: so.Mapped[str] = so.mapped_column(sa.String(85), index=True)
    postalcode: so.Mapped[str] = so.mapped_column(sa.String(20))
    street: so.Mapped[str] = so.mapped_column(sa.String(58))
    house_number: so.Mapped[int] = so.mapped_column(sa.Integer)
    address_suffix: so.Mapped[str] = so.mapped_column(sa.String(10))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)  # Linked to the User id

    def __repr__(self):
        return f' The Address is: {self.country},\n{self.city},\n {self.street}.'


class Post(movie_db.Model):
    id: so.Mapped[str] = so.mapped_column(primary_key=True)
    post_message: so.Mapped[str] = so.mapped_column(sa.Text)
    rating: so.Mapped[int] = so.mapped_column(sa.Integer)  # While implementing in the code we have to add min =0 and max = 10
    upvote: so.Mapped[int] = so.mapped_column(sa.Integer)  # implement thumb up count.
    downvote: so.Mapped[int] = so.mapped_column(sa.Integer)  # implement thumbs down count.
    time_of_posting: so.Mapped[datetime] = so.mapped_column(
        index=True,
        default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')