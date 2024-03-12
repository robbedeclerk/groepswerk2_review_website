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
popular = [{'id': 1096197, 'Type': 'film'}, {'id': 932420, 'Type': 'film'}, {'id': 1011985, 'Type': 'film'}, {'id': 1239251, 'Type': 'film'}, {'id': 940551, 'Type': 'film'}, {'id': 693134, 'Type': 'film'}, {'id': 792307, 'Type': 'film'}, {'id': 870404, 'Type': 'film'}, {'id': 1072790, 'Type': 'film'}, {'id': 787699, 'Type': 'film'}, {'id': 969492, 'Type': 'film'}, {'id': 984249, 'Type': 'film'}, {'id': 438631, 'Type': 'film'}, {'id': 848538, 'Type': 'film'}, {'id': 866398, 'Type': 'film'}, {'id': 1227816, 'Type': 'film'}, {'id': 636706, 'Type': 'film'}, {'id': 714567, 'Type': 'film'}, {'id': 609681, 'Type': 'film'}, {'id': 949429, 'Type': 'film'}, {'id': 13945, 'Type': 'serie'}, {'id': 22980, 'Type': 'serie'}, {'id': 45789, 'Type': 'serie'}, {'id': 2261, 'Type': 'serie'}, {'id': 94722, 'Type': 'serie'}, {'id': 8590, 'Type': 'serie'}, {'id': 65701, 'Type': 'serie'}, {'id': 2224, 'Type': 'serie'}, {'id': 59941, 'Type': 'serie'}, {'id': 137228, 'Type': 'serie'}, {'id': 11890, 'Type': 'serie'}, {'id': 63770, 'Type': 'serie'}, {'id': 126308, 'Type': 'serie'}, {'id': 206559, 'Type': 'serie'}, {'id': 52814, 'Type': 'serie'}, {'id': 240909, 'Type': 'serie'}, {'id': 117817, 'Type': 'serie'}, {'id': 219109, 'Type': 'serie'}, {'id': 2734, 'Type': 'serie'}, {'id': 14981, 'Type': 'serie'}]

for user in User.query.all():
    choice = fake.random.choices(popular, k=1)
    post = Post(
        post_message=fake.paragraph(),
        rating=fake.random_int(min=0, max=10),
        upvote=fake.random_int(),
        downvote=fake.random_int(),
        movie_id=choice[0]['id'],
        is_movie=choice[0]['Type'] == 'film',
        user_id=user.id
    )
    db.session.add(post)

db.session.commit()
