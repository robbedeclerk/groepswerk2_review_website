from faker import Faker
from app import app, db
from app.models import User, Address, Post
from app.new_tmdb_api import make_faker_list

fake = Faker()

# Create app context
app.app_context().push()

# Create fake users
for _ in range(100):
    my_user = User(
        username=fake.user_name(),
        email=fake.email(),
        firstname=fake.first_name(),
        family_name=fake.last_name()
    )
    my_user.set_password(fake.password())
    db.session.add(my_user)

# Create fake addresses for users
for user in User.query.all():
    address = Address(
        country=fake.country(),
        city=fake.city(),
        postalcode=fake.postcode(),
        street=fake.street_name(),
        house_number=fake.building_number(),
        address_suffix=fake.secondary_address(),
        user_id=user.id
    )
    db.session.add(address)

# Create fake posts for users
popular = make_faker_list()

for user in User.query.all():
    choice = fake.random.choices(popular, k=1)
    post = Post(
        post_message=fake.paragraph(),
        rating=fake.random_int(min=0, max=10),
        movie_id=choice[0]['Id'],
        is_movie=choice[0]['Type'] == 'film',
        user_id=user.id
    )
    db.session.add(post)

db.session.commit()
