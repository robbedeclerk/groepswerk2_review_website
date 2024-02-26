from ..app import app
from flask import render_template, url_for
from .tmdb_api import Tmdb

movie = Tmdb(True)
serie = Tmdb(False)


@app.route('/')
@app.route('/index')
def index():
    movie_list = movie.get_popular_details()
    return render_template('index.html', movies=movie_list, movieapi=movie)


@app.route('/home')
def home():
    return render_template("..templates/index.html")


@app.route('/<type>/<id>')
def search(type, id=None):
    if type == "film":
        if id:
            movie_details = movie.get_details(id)
            return render_template('film_profile.html', movie=movie_details, movieapi=movie, id=id)
        else:
            movie_list = movie.get_popular_details()
            return render_template('index.html', movies=movie_list, movieapi=movie)
    elif type == "serie":
        if id:
            serie_details = serie.get_details(id)
            return render_template('film_profile.html', serie=serie_details, movieapi=serie, id=id)
        else:
            serie_list = serie.get_popular_details()
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
