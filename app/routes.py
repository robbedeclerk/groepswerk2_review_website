from app import app, db
from app.new_tmdb_api import Tmdb
from flask import render_template, request, redirect, url_for, session, jsonify, flash
import psycopg2
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import (LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm,
                       EditProfileForm, PostForm, EmptyForm)
from app.models import User, Post, downvotes, upvotes
from urllib.parse import urlsplit
import sqlalchemy as sa
from sqlalchemy import desc, func
from app.usermail import send_password_reset_email

movie = Tmdb(True)
serie = Tmdb(False)


@app.context_processor
def inject_movie():
    return dict(movie_tmdb=movie, serie_tmdb=serie)


@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    movie_list = movie.get_small_details_out_big_data(movie.get_popular_data(page))
    return render_template('index.html', title='Homepage', movies=movie_list, current_page=page,
                           title_string="Popular Movies")


@app.route('/search_movies')
def search_movies():
    title = request.args.get('title')
    if title:
        results = movie.get_10_Titles_for_both(title, 1)
        sorted_movie_list = sorted(results, key=lambda x: x['Popularity'], reverse=True)
        return sorted_movie_list
    else:
        return {'error': 'No title provided'}


def get_sorted_posts(id=None, movie_type=None, sort_by='newest', current_user_country=None, page=1, per_page=5,
                     user_id=None):
    query = Post.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if movie_type == 'film':
        query = query.filter_by(movie_id=id, is_movie=True)
    if movie_type == 'serie':
        query = query.filter_by(movie_id=id, is_movie=False)

    if sort_by == 'newest':
        sorted_query = query.order_by(desc(Post.time_of_posting))
    elif sort_by == 'oldest':
        sorted_query = query.order_by(Post.time_of_posting)
    elif sort_by == 'rating_high':
        sorted_query = query.order_by(desc(Post.rating))
    elif sort_by == 'rating_low':
        sorted_query = query.order_by(Post.rating)
    elif sort_by == 'upvotes':
        sorted_query = query.outerjoin(upvotes).group_by(Post.id).order_by(desc(func.count(upvotes.c.post_id)))
    elif sort_by == 'downvotes':
        sorted_query = query.outerjoin(downvotes).group_by(Post.id).order_by(desc(func.count(downvotes.c.post_id)))
    elif sort_by == 'my_country' and current_user.is_authenticated:
        sorted_query = query.join(Post.author).filter(User.country == current_user_country).order_by(
            desc(Post.time_of_posting))
    else:
        sorted_query = query.order_by(desc(Post.time_of_posting))

    # Pagination
    posts = sorted_query.paginate(page=page, per_page=per_page)

    return posts


@app.route('/<type>/<id>', methods=['GET', 'POST'])
def search(type, id=None):
    if type == "film":
        if id.isnumeric():
            sort_by = request.args.get('sort_by', 'newest', type=str)
            page = request.args.get('page', 1, type=int)

            if current_user.is_authenticated:
                posts = get_sorted_posts(id=id, movie_type=type, sort_by=sort_by,
                                         current_user_country=current_user.country, page=page)
            else:
                posts = get_sorted_posts(id=id, movie_type=type, sort_by=sort_by, page=page)
            movie_details = movie.get_small_details_out_single_movie(True, movie.get_data(id))
            movie_similars = movie.get_small_details_out_big_data(movie.get_similar_data(id))
            form = PostForm()
            if form.validate_on_submit():
                post = Post(post_message=form.post_message.data, rating=form.rating.data, author=current_user,
                            movie_id=id, is_movie=True)
                db.session.add(post)
                db.session.commit()
                return redirect(url_for('search', type=type, id=id, sort_by=sort_by))
            return render_template('film_profile.html', movie=movie_details, movieapi=movie, id=id,
                                   similars=movie_similars, posts=posts, form=form, sort_by=sort_by)
        else:
            if id == "popular":
                page = request.args.get('page', 1, type=int)  # Get the current page from the request arguments
                movie_list = movie.get_small_details_out_big_data(movie.get_popular_data(page))
                return render_template('index.html', movies=movie_list, current_page=page, type=type, id=id,
                                       title_string="Popular Movies")
            elif id == "top-rated":
                page = request.args.get('page', 1, type=int)  # Get the current page from the request arguments
                movie_list = movie.get_small_details_out_big_data(movie.get_top_rated_data(page))
                return render_template('index.html', movies=movie_list, current_page=page, type=type, id=id,
                                       title_string="Top Rated Movies")
            elif id == "trending":
                page = request.args.get('page', 1, type=int)  # Get the current page from the request arguments
                movie_list = movie.get_small_details_out_big_data(movie.get_trending_data(page))
                return render_template('index.html', movies=movie_list, current_page=page, type=type, id=id,
                                       title_string="Trending Movies")
            elif id == "now-playing":
                page = request.args.get('page', 1, type=int)  # Get the current page from the request arguments
                movie_list = movie.get_small_details_out_big_data(movie.get_now_playing_data(page))
                return render_template('index.html', movies=movie_list, current_page=page, type=type, id=id,
                                       title_string="Now Playing Movies")
            movie_list = movie.get_small_details_out_big_data(movie.get_popular_data())
            page = request.args.get('page', 1, type=int)  # Get the current page from the request arguments
            return render_template(url_for('index'))
    elif type == "serie":
        if id.isnumeric():
            sort_by = request.args.get('sort_by', 'newest', type=str)
            page = request.args.get('page', 1, type=int)

            if current_user.is_authenticated:
                posts = get_sorted_posts(id=id, movie_type=type, sort_by=sort_by,
                                         current_user_country=current_user.country, page=page)
            else:
                posts = get_sorted_posts(id=id, movie_type=type, sort_by=sort_by, page=page)
            serie_details = serie.get_small_details_out_single_movie(False, serie.get_data(id))
            form = PostForm()
            if form.validate_on_submit():
                post = Post(post_message=form.post_message.data, rating=form.rating.data, author=current_user,
                            movie_id=id, is_movie=False)
                db.session.add(post)
                db.session.commit()
                return redirect(url_for('search', type=type, id=id, sort_by=sort_by))
            return render_template('film_profile.html', movie=serie_details, movieapi=serie, id=id, posts=posts,
                                   form=form, sort_by=sort_by)
        else:
            if id == "popular":
                page = request.args.get('page', 1, type=int)  # Get the current page from the request arguments
                movie_list = serie.get_small_details_out_big_data(serie.get_popular_data(page))
                return render_template('index.html', movies=movie_list, current_page=page, type=type, id=id,
                                       title_string="Popular Series")
            elif id == "top-rated":
                page = request.args.get('page', 1, type=int)  # Get the current page from the request arguments
                movie_list = serie.get_small_details_out_big_data(serie.get_top_rated_data(page))
                return render_template('index.html', movies=movie_list, current_page=page, type=type, id=id,
                                       title_string="Top Rated Series")
            elif id == "trending":
                page = request.args.get('page', 1, type=int)  # Get the current page from the request arguments
                movie_list = serie.get_small_details_out_big_data(serie.get_trending_data(page))
                return render_template('index.html', movies=movie_list, current_page=page, type=type, id=id,
                                       title_string="Trending Series")
            elif id == "now-playing":
                page = request.args.get('page', 1, type=int)  # Get the current page from the request arguments
                movie_list = serie.get_small_details_out_big_data(serie.get_now_playing_data(page))
                return render_template('index.html', movies=movie_list, current_page=page, type=type, id=id,
                                       title_string="Now Playing Series")
            page = request.args.get('page', 1, type=int)  # Get the current page from the request arguments
            movie_list = serie.get_small_details_out_big_data(serie.get_popular_data(page))
            return render_template('index.html', movies=movie_list, current_page=page, type=type, id=id,
                                   title_string="Popular Series")


@app.route('/search_title/')
def search_title():
    title = request.args.get('title')
    if title:
        page = request.args.get('page', 1, type=int)
        results = movie.get_10_Titles_for_both(title, page)
        sorted_movie_list = sorted(results, key=lambda x: x['Popularity'], reverse=True)
        return render_template('index.html', movies=sorted_movie_list, current_page=page, title=title,
                               title_string="Search Results for : " + str(title))
    else:
        return render_template(url_for('index'))


@app.route('/genre/<type>/popular/<int:genre_id>')
def popular(type, genre_id):
    page = request.args.get('page', 1, type=int)  # Get the current page from the request arguments
    if type not in ["film", "serie"]:
        return render_template('index.html', movies=movie.get_small_details_out_big_data(movie.get_popular_data(page)),
                               current_page=page, title_string="Popular Movies")
    if type == "film":
        genre_name = movie.get_genre_name(genre_id)
        movie_list = movie.get_small_details_out_big_data(
            movie.get_data_filtered_genres_on_popularity(genre_id, page=page))
        return render_template('index.html', movies=movie_list, type=type, genre=genre_id, current_page=page,
                               title_string="Popular Movies for Genre: " + str(genre_name))
    elif type == "serie":
        genre_name = serie.get_genre_name(genre_id)
        serie_list = serie.get_small_details_out_big_data(
            serie.get_data_filtered_genres_on_popularity(genre_id, page=page))
        return render_template('index.html', movies=serie_list, type=type, genre=genre_id, current_page=page,
                               title_string="Popular Series for Genre: " + str(genre_name))


@login_required
@app.route('/submit_post', methods=['GET', 'POST'])
def submit_post(movie_id, is_movie):
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

    movie_list = movie.get_small_details_out_big_data(movie.get_popular_data(1))
    return render_template('index.html', movie_list=movie_list, movieapi=movie, page=1)


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
            country=(form.country.data.capitalize())
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function makes it possible for the user to login
    """
    # If the user is already logged in, he gets redirected to homepage.
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == 'GET':
        if 'next' in request.args:
            session['next'] = request.args.get('next')
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(
            User.username == form.username.data))
        # db.session.scalar() will return the user object if it exists, or None if it does not.
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password!")
            return redirect(url_for("login", next=request.args.get('next')))
        # .scalar() returned None or login failed on password check redirect to the login again.
        login_user(user, remember=form.remember_me.data)
        next_url = session.pop('next', None)
        if next_url:
            return redirect(next_url)
        else:
            return redirect(url_for('index'))
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
    return render_template('reset_password.html', form=form, title='Edit Profile')


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        # If the form is valid, update the user profile with the form data
        current_user.firstname = form.firstname.data.capitalize()
        current_user.family_name = form.family_name.data.capitalize()
        current_user.country = form.country.data.capitalize()
        db.session.commit()  # Commit the changes to the database
        flash('Your changes have been saved.')  # Show a flash message to the user
        return redirect(url_for('index'))  # Redirect the user back to the profile page

    # If it's a GET request, pre-populate the form fields with the current user data
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.family_name.data = current_user.family_name
        form.country.data = current_user.country

    # Render the posts for the current user
    return render_template('edit_profile.html', title='Edit Profile', form=form, user=current_user)


@app.route('/profile')
def profile():
    user_id = request.args.get('user_id')
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort_by', 'newest', type=str)
    if user_id is None:
        user_id = current_user.id
    user = User.query.get_or_404(user_id)
    posts = get_sorted_posts(user_id=user_id, page=page, sort_by=sort_by)
    return render_template('profile.html', title='Profile', user=user, posts=posts, page=page, sort_by=sort_by)


@login_required
@app.route('/upvote/<int:post_id>', methods=['POST'])
def upvote(post_id):
    post = Post.query.get_or_404(post_id)

    # Check if the user has already upvoted the post
    if current_user not in post.upvoters:

        # Add the user's ID to the list of upvoters
        current_user.upvote_post(post)

        # Commit the changes to the database
        db.session.commit()

        flash('Post upvoted successfully!', 'success')
    else:
        post.upvoters.remove(current_user)
        db.session.commit()

        flash('You have removed your upvote!', 'danger')
    if post.is_movie:
        type = 'film'
    else:
        type = 'serie'
    return redirect(url_for('search', type=type, id=post.movie_id))


@login_required
@app.route('/downvote/<int:post_id>', methods=['POST'])
def downvote(post_id):
    post = Post.query.get_or_404(post_id)

    # Check if the user has already downvoted the post
    if current_user not in post.downvoters:

        # Add the user's ID to the list of upvoters
        current_user.downvote_post(post)

        # Commit the changes to the database
        db.session.commit()

        flash('Post downvoted successfully!', 'success')
    else:
        post.downvoters.remove(current_user)
        db.session.commit()

        flash('You have removed your downvote!', 'danger')
    if post.is_movie:
        type = 'film'
    else:
        type = 'serie'
    return redirect(url_for('search', type=type, id=post.movie_id))
