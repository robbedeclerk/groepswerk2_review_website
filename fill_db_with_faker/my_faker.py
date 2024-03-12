from faker import Faker
from app import app, db
from app.models import User, Address, Post


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
id_number = 0
for user in User.query.all():
    post = Post(
        post_message=fake.paragraph(),
        rating=fake.random_int(min=0, max=10),
        upvote=fake.random_int(),
        downvote=fake.random_int(),
        user_id=user.id
    )
    db.session.add(post)

db.session.commit()
