from turtle import title
from app import app, db
from app.new_tmdb_api import Tmdb
from flask import render_template, request, redirect, url_for, session, jsonify, flash
import psycopg2
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import (LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm,
                       EditProfileForm, PostForm, EmptyForm)
from app.models import User, Post, Address
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


@app.route('/<type>/<id>', methods=['GET', 'POST'])
def search(type, id=None):
    if type == "film":
        if id.isnumeric():
            posts = db.session.execute(sa.select(Post).where(Post.movie_id == id, Post.is_movie == True)).fetchall()
            movie_details = movie.get_small_details_out_single_movie(True, movie.get_data(id))
            movie_similars = movie.get_small_details_out_big_data(movie.get_similar_data(id))
            form = PostForm()
            if form.validate_on_submit():
                submit_post(id, True, current_user.id)

            return render_template('film_profile.html', movie=movie_details, movieapi=movie, id=id,
                                   similars=movie_similars, posts=posts, form=form)
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
            posts = db.session.execute(sa.select(Post).where(Post.movie_id == id, Post.is_movie == False)).fetchall()
            serie_details = serie.get_small_details_out_single_movie(False, serie.get_data(id))
            serie_similars = serie.get_small_details_out_big_data(serie.get_similar_data(id))
            form = PostForm()
            if form.validate_on_submit():
                submit_post(id, False, current_user.id)

            return render_template('film_profile.html', movie=serie_details, movieapi=serie, id=id,
                                   similars=serie_similars, posts=posts, form=form)
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


@app.route('/genre/<type>/popular/<int:genre_id>')
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


@app.route('/submit_post', methods=['GET', 'POST'])
def submit_post(movie_id, is_movie, user_id):
    form = PostForm(request.form)
    if current_user.is_authenticated:
        if request.method == 'POST' and form.validate():
            # Access form data
            if form.validate_on_submit():
                post = Post(post_message=form.post_message.data, rating=form.rating.data,
                            user_id=current_user.id, movie_id=movie_id, is_movie=is_movie, upvote=1, downvote=0)
                db.session.add(post)
                db.session.commit()
                flash('Your post is now live!')
                return redirect(url_for('index'))

    movie_list = movie.get_small_details_out_big_data(movie.get_popular_data())
    return render_template('index.html', movie_list=movie_list, movieapi=movie)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Creates a new user.
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            firstname=(form.firstname.data.capitalize()),
            family_name=(form.family_name.data.capitalize()),
        )
        address = Address(
            country=(form.country.data.capitalize()),
            city=form.city.data,
            postalcode=form.postalcode.data,
            street=(form.street.data.capitalize()),
            house_number=form.house_number.data,
            address_suffix=form.address_suffix.data
        )
        user.set_password(form.password.data)
        db.session.add(user, address)
        db.session.commit()
        flash('Your account has been created!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function makes it possible for the user to login
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
        return redirect(next_page)
    return render_template("login.html", title="Login", form=form)


@app.route('/logout')
@login_required
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
    return render_template('email/reset_password_request.html', title='Reset Password', form=form)


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
    return render_template('reset_password.html', form=form, title='Edit Profile')


@app.route('/profile/<user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    if user_id is None:
        form = EditProfileForm(current_user.username)
        if form.validate_on_submit():
            current_user.username = form.username.data
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('edit_profile'))
        elif request.method == 'GET':
            form.username.data = current_user.username
        return render_template('profile.html', user=current_user,
                               form=form)
    else:
        user = db.first_or_404(sa.select(User).where(User.id == user_id))
        page = request.args.get('page', 1, type=int)
        query = user.posts.select().order_by(Post.time_of_posting.desc())
        posts = db.paginate(query, page=page, per_page=10, error_out=False)
        next_url = url_for('profile', user_id=user_id, page=posts.next_num) \
            if posts.has_next else None
        prev_url = url_for('profile', user_id=user_id, page=posts.prev_num) \
            if posts.has_prev else None
        form = EmptyForm()
        return render_template('profile.html', user=user, posts=posts.items, next_url=next_url,
                               prev_url=prev_url, form=form)
