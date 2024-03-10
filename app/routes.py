from turtle import title
from app import app, db
from app.new_tmdb_api import Tmdb
from flask import render_template, request, redirect, url_for, session, jsonify, flash
import psycopg2
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from urllib.parse import urlsplit
import sqlalchemy as sa
from app.email import send_password_reset_email


movie = Tmdb(True)
serie = Tmdb(False)


@app.route('/')
@app.route('/index')
def index():
    movie_list = movie.get_small_details_out_big_data(movie.get_popular_data())
    return render_template('index.html', movies=movie_list, movieapi=movie)


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
            movie_list = movie.get_small_details_out_big_data(movie.get_popular_data())
            return render_template('index.html', movies=movie_list, movieapi=movie)
    elif type == "serie":
        if id.isnumeric():
            serie_details = serie.get_small_details_out_single_movie(True, serie.get_data(id))
            serie_similars = serie.get_small_details_out_big_data(serie.get_similar_data(id))
            # serie_details = serie.get_details(id)
            # serie_similars = serie.get_small_details_out_data(serie.get_similar_data(id))
            return render_template('film_profile.html', movie=serie_details, movieapi=serie, id=id,
                                   similars=serie_similars)
        else:
            serie_list = serie.get_small_details_out_big_data(serie.get_popular_data())
            return render_template('index.html', movies=serie_list, movieapi=serie)


# @app.route('/film/popular')
# def movie_popular():
#     movie_list = movie.get_popular_details()
#     return render_template('index.html', movies=movie_list, movieapi=movie)
#
#
# @app.route('/serie/popular')
# def serie_popular():
#     serie_list = serie.get_popular_details()
#     return render_template('index.html', movies=serie_list, movieapi=serie)


@app.route('/<type>/popular/<genre_id>')
def popular(type, genre_id):
    if type not in ["film", "serie"]:
        return render_template('index.html', movies=movie.get_small_details_out_big_data(movie.get_popular_data()), movieapi=movie)
    if type == "film":
        movie_list = movie.get_data_filtered_genres_on_popularity(genre_id)
        print('Test')
        return render_template('index.html', movies=movie_list, movieapi=movie, genre=genre_id)
    elif type == "serie":
        serie_list = serie.get_data_filtered_genres_on_popularity(genre_id)
        return render_template('index.html', movies=serie_list, movieapi=serie, genre=genre_id)


# @app.route('/film/popular/<genre>')
# def movie_popular(genre):
#     movie_list = movie.get_details_filtered_on_genre(genre)
#     return render_template('index.html', movies=movie_list, movieapi=movie, genre=genre)
#
#
# @app.route('/serie/popular/<genre>')
# def serie_popular(genre):
#     serie_list = serie.get_details_filtered_on_genre(genre)
#     return render_template('index.html', movies=serie_list, movieapi=serie, genre=genre)


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
    form = ResetpasswordRequestForm()
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
    return render_template('reset_password_new.html', form=form)


@app.route('/profile')
def profile():
    if 'user' in session:
        return f"profile - logged in as {session['user']}"
    else:
        return redirect(url_for('main'))


@app.route('/change_email', methods=['POST'])
def change_email():
    if request.method == 'POST':
        new_email = request.form['new_email']
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("UPDATE users SET email = %s WHERE email = %s", (new_email, session['user']))
        conn.commit()
        cur.close()
        conn.close()
        session['email'] = new_email
        return redirect(url_for('profile'))