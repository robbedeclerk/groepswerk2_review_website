from faker import Faker
from app import app, db
from app.models import User, Post
from app.new_tmdb_api import make_faker_list

fake = Faker()
# Create app context
app.app_context().push()

# Country Codes
country_List = [{'country': 'United States', 'locale': 'en_US'}, {'country': 'United Kingdom', 'locale': 'en_GB'},
                {'country': 'Germany', 'locale': 'de_DE'}, {'country': 'France', 'locale': 'fr_FR'},
                {'country': 'Spain', 'locale': 'es_ES'}, {'country': 'Italy', 'locale': 'it_IT'},
                {'country': 'Japan', 'locale': 'ja_JP'}, {'country': 'Brazil', 'locale': 'pt_BR'},
                {'country': 'China', 'locale': 'zh_CN'}, {'country': 'Russia', 'locale': 'ru_RU'},
                {'country': 'Belgium', 'locale': 'nl_BE'}]

# Create fake users
users = []
for _ in range(1000):
    country_choice = fake.random.choice(country_List)
    fake_Country = Faker(country_choice['locale'])
    my_user = User(
        country=country_choice['country'],
        username=fake_Country.user_name() + str(fake.random.randint(0, 1000)),
        email=str(fake.random.randint(0, 1000)) + fake_Country.email(),
        firstname=fake_Country.first_name(),
        family_name=fake_Country.last_name(),
    )
    my_user.set_password(fake.password())
    users.append(my_user)
    db.session.add(my_user)

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

    other_users = [u for u in users if u.id != user.id]
    if other_users:
        num_upvotes = fake.random.randint(0, len(other_users))
        upvoters = fake.random.sample(other_users, num_upvotes)
        for upvoter in upvoters:
            post.upvoters.append(upvoter)
    if other_users:
        num_downvotes = fake.random.randint(0, len(other_users))
        downvoters = fake.random.sample(other_users, num_downvotes)
        for downvoter in downvoters:
            post.downvoters.append(downvoter)

db.session.commit()
