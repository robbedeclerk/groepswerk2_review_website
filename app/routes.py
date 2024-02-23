from app import app
from flask import render_template
from  tmdb_api import Tmdb


movie = Tmdb(True)

@app.route('/')
@app.route('/index')
def index():
    movie_list = movie.get_popular_details()
    return render_template('index.html', movies=movie_list, movieapi=movie)



@app.route('/home')
def home():
    return render_template('home.html')