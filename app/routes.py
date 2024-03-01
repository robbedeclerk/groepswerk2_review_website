from ..app import app
from ..app import db
from .tmdb_api import Tmdb
from flask import render_template, request, redirect, url_for, session, jsonify
import psycopg2

movie = Tmdb(True)
serie = Tmdb(False)


@app.route('/')
@app.route('/index')
def index():
    # movie_list = movie.get_popular_details()
    movie_list = movie.get_details_out_data(movie.get_popular_data())
    return render_template('index.html', movies=movie_list, movieapi=movie)


@app.route('/home')
def home():
    return render_template("..templates/index.html")

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
            movie_details = movie.get_details(id)
            movie_similars = movie.get_small_details_out_data(movie.get_similar_data(id))
            return render_template('film_profile.html', movie=movie_details, movieapi=movie, id=id, similars=movie_similars)
        else:
            movie_list = movie.get_small_details_out_data(movie.get_popular_data())
            return render_template('index.html', movies=movie_list, movieapi=movie)
    elif type == "serie":
        if id.isnumeric():
            serie_details = serie.get_details(id)
            serie_similars = serie.get_small_details_out_data(serie.get_similar_data(id))
            return render_template('film_profile.html', movie=serie_details, movieapi=serie, id=id, similars=serie_similars)
        else:
            serie_list = serie.get_small_details_out_data(serie.get_popular_data())
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


@app.route('/<type>/popular/<genre>')
def popular(type, genre):
    if type == "film":
        movie_list = movie.get_details_filtered_on_genre(genre)
        return render_template('index.html', movies=movie_list, movieapi=movie, genre=genre)
    elif type == "serie":
        serie_list = serie.get_details_filtered_on_genre(genre)
        return render_template('index.html', movies=serie_list, movieapi=serie, genre=genre)

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


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'post':
        email = request.form['email']
        password = request.form['password']
        # kan meer info onder zetten als we meer toevoegen

        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['user'] = user[0]
            return redirect(url_for('profile'))
        else:
            return "Wrong email or password"


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
        conn=psycopg2.connect(**db_params)
        cur=conn.cursor()
        cur.execute("UPDATE users SET email = %s WHERE email = %s", (new_email, session['user']))
        conn.commit()
        cur.close()
        conn.close()
        session['email']= new_email
        return redirect(url_for('profile'))

@app.route('/change_username', methods=['POST'])
def change_username():
    if request.method == 'POST':
        new_username = request.form['new_username']
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("UPDATE gebruikers SET username = %s WHERE email = %s", (new_username, session['email']))
        conn.commit()
        cur.close()
        conn.close()
        session['user'] = new_username
        return redirect(url_for('profile'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        token = 'example_token'
        reset_link = url_for('reset_password', token=token, _external=True)
        return "Password reset link sent to your email."
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = request.form['new_password']
        return "Password reset successful. Redirect to login page."
    return render_template('reset_password.html', token=token)