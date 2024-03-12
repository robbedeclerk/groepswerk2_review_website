from datetime import datetime, timezone, timedelta
from app import app
import pytest, jwt
from app.models import User, Address, Post


@pytest.fixture(scope='function')
def new_user():
    user = User(
        id=1,
        username='benny',
        email='benny@example.com',
        password_hash='password',
        firstname='firstname'.capitalize(),
        family_name='family_name'.capitalize()
    )
    return user


def test_new_user(new_user):
    """
    Given a new_user model, When a new new_user is created,
    Then check the mail, hashed password and role fields are defined correctly
    """

    assert new_user.username == 'benny'
    assert new_user.email == 'benny@example.com'
    assert new_user.firstname == 'firstname'
    assert new_user.family_name == 'family_name'


def test_user_representation(new_user):
    """
    Test the representation of a new_user.
    """

    assert repr(new_user) == 'User: benny, benny@example.com, password, firstname, family_name'


def test_set_password(new_user):
    """
    Tests the password hash is active
    """

    new_user.set_password('password')
    assert new_user.password_hash is not None
    assert new_user.password_hash != 'password'


def test_check_password(new_user):
    """
    Tests if the password checking works like intended.
    """

    new_user.set_password('password')
    assert new_user.check_password('password') == True
    assert new_user.check_password('notthepassword') == False


def test_avatar(new_user):
    """
    Tests the link of the avatar
    """

    avatar_url = new_user.avatar(128)
    assert (avatar_url ==
            'https://www.gravatar.com/avatar/1c5019ed4f6db29150cafc8717352337?d=identicon&s=128')


# def test_get_reset_password_token(new_user):
#     """
#     Tests if the token is made.
#     """
#     token = new_user.get_reset_password_token(expires_in=600)
#     assert token is None

@pytest.fixture(scope='function')
def new_address():
    address = Address(
        id=1,
        country='Country'.capitalize(),
        city='City'.capitalize(),
        postalcode='2400qa',
        street='Street'.capitalize(),
        house_number=100,
        address_suffix='abc1',
    )
    return address


def test_new_address(new_address):
    """
    Test a new instance of an Address.
    """
    assert new_address.id == 1
    assert new_address.country == 'Country'
    assert new_address.city == 'City'
    assert new_address.postalcode == '2400qa'
    assert new_address.street == 'Street'
    assert new_address.house_number == 100
    assert new_address.address_suffix == 'abc1'
