from turtle import title
from app import app, db
from app.new_tmdb_api import Tmdb
from flask import render_template, request, redirect, url_for, session, jsonify, flash
import psycopg2
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, EditProfileForm
from app.models import User
from urllib.parse import urlsplit
import sqlalchemy as sa
from app.usermail import send_password_reset_email


movie = Tmdb(True)
serie = Tmdb(False)


@app.route('/')
@app.route('/index')
def index():
    movie_list = movie.get_small_details_out_big_data(movie.get_popular_data())
    return render_template('index.html', title='Homepage', movies=movie_list, movieapi=movie)


@app.route('/search_movies')
def search_movies():
    title = request.args.get('title')
    if title:
        results = movie.get_5_Titles_for_both(title)
        sorted_movie_list = sorted(results, key=lambda x: x['Popularity'], reverse=True)
        return jsonify(sorted_movie_list)
    else:
        return jsonify({'error': 'No title provided'})


@app.route('/<type>/<id>')
def search(type, id=None):
    if type == "film":
        if id.isnumeric():
            movie_details = movie.get_small_details_out_single_movie(True, movie.get_data(id))
            movie_similars = movie.get_small_details_out_big_data(movie.get_similar_data(id))
            # movie_details = movie.get_details(id)
            # movie_similars = movie.get_small_details_out_data(movie.get_similar_data(id))
            return render_template('film_profile.html', movie=movie_details, movieapi=movie, id=id,
                                   similars=movie_similars)
        else:
            if id == "popular":
                movie_list = movie.get_small_details_out_big_data(movie.get_popular_data())
                return render_template('index.html', movies=movie_list, movieapi=movie)
            elif id == "top-rated":
                movie_list = movie.get_small_details_out_big_data(movie.get_top_rated_data())
                return render_template('index.html', movies=movie_list, movieapi=movie)
            elif id == "trending":
                movie_list = movie.get_small_details_out_big_data(movie.get_trending_data())
                return render_template('index.html', movies=movie_list, movieapi=movie)
            elif id == "now-playing":
                movie_list = movie.get_small_details_out_big_data(movie.get_now_playing_data())
                return render_template('index.html', movies=movie_list, movieapi=movie)
            movie_list = movie.get_small_details_out_big_data(movie.get_popular_data())
            return render_template('index.html', movies=movie_list, movieapi=movie)
    elif type == "serie":
        if id.isnumeric():
            serie_details = serie.get_small_details_out_single_movie(False, serie.get_data(id))
            serie_similars = serie.get_small_details_out_big_data(serie.get_similar_data(id))
            # serie_details = serie.get_details(id)
            # serie_similars = serie.get_small_details_out_data(serie.get_similar_data(id))
            return render_template('film_profile.html', movie=serie_details, movieapi=serie, id=id,
                                   similars=serie_similars)
        else:
            if id == "popular":
                movie_list = serie.get_small_details_out_big_data(serie.get_popular_data())
                return render_template('index.html', movies=movie_list, movieapi=serie)
            elif id == "top-rated":
                movie_list = serie.get_small_details_out_big_data(serie.get_top_rated_data())
                return render_template('index.html', movies=movie_list, movieapi=serie)
            elif id == "trending":
                movie_list = serie.get_small_details_out_big_data(serie.get_trending_data())
                return render_template('index.html', movies=movie_list, movieapi=serie)
            elif id == "now-playing":
                movie_list = serie.get_small_details_out_big_data(serie.get_now_playing_data())
                return render_template('index.html', movies=movie_list, movieapi=serie)
            movie_list = serie.get_small_details_out_big_data(serie.get_popular_data())
            return render_template('index.html', movies=movie_list, movieapi=serie)





@app.route('/<type>/popular/<int:genre_id>')
def popular(type, genre_id):
    if type not in ["film", "serie"]:
        return render_template('index.html', movies=movie.get_small_details_out_big_data(movie.get_popular_data()),
                               movieapi=movie)
    if type == "film":
        movie_list = movie.get_small_details_out_big_data(movie.get_data_filtered_genres_on_popularity(genre_id))
        print('Test')
        print(f"Type: {type}, Genre ID: {genre_id}")
        print(f"{movie.get_small_details_out_big_data(movie.get_data_filtered_genres_on_popularity(genre_id))}")

        return render_template('index.html', movies=movie_list, movieapi=movie, genre=genre_id)
    elif type == "serie":
        serie_list = serie.get_small_details_out_big_data(serie.get_data_filtered_genres_on_popularity(genre_id))
        return render_template('index.html', movies=serie_list, movieapi=serie, genre=genre_id)




@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Creates a new user.
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This functionmakes it possible for the user to login
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))
        # If the user is already logged in, he gets redirected to homepage.
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(
            User.username == form.username.data))
        # db.session.scalar() will return the user object if it exists, or None if it does not.
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password!")
            return redirect(url_for("login"))
        # .scalar() returned None or login failed on password check redirect to the login again.
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        # If user exists and password is correct, then log the user in and redirect to homepage.
        return redirect(url_for(next_page))
    return render_template("login.html", title="Login", form=form)


@app.route('/logout')
def logout():
    """
    Logs the user out.
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """
    This function deals with a password reset request.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # If the user is logged in already, he gets redirected to homepage.
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        # If the user address exists, the email will be sent.
        flash("We have send an email with instructions to reset your password!")
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    Reset the user's password using a token.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password_new.html', form=form, title='Edit Profile')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('profile.html', title='Edit Profile',
                           form=form)





