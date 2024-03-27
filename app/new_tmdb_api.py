from cachetools import TTLCache, cached
import requests
import json


def stringify_page(page=1):
    return 'page=%s' % page


class Tmdb:

    def __init__(self, isMovie):
        # Initializing the TMDB class with required parameters
        self.isMovie = isMovie
        self.cache = TTLCache(maxsize=1000, ttl=3600)
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
        }
        self.genres = self.list_of_genres()

    # Utility functions
    def get_type(self):
        if self.isMovie:
            return "film"
        else:
            return "serie"

    def is_movie_arg(self):
        if self.isMovie:
            return "movie"
        else:
            return "tv"

    def title_arg(self):
        if self.isMovie:
            return 'title'
        else:
            return 'name'

    def connected(self):
        # Checking connection status with TMDB
        url = "https://api.themoviedb.org/3/authentication"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            print("Connected to TheMovieDB")
        else:
            print("Failed to connect to TheMovieDB")

    # Cached API calls
    @cached(cache={})
    def list_of_genres(self):
        """
        A function to fetch a list of genres from a movie database API.
        """
        url = f"https://api.themoviedb.org/3/genre/{self.is_movie_arg()}/list?language=en"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    def get_genre_name(self, id):
        for genre in self.genres["genres"]:
            if genre["id"] == id:
                return genre["name"]

    # Fetching data
    @cached(cache={})
    def get_trending_data(self, page=1):
        # Fetching trending data
        url = f"https://api.themoviedb.org/3/trending/{self.is_movie_arg()}/day?{stringify_page(page)}&language=en-US"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    @cached(cache={})
    def get_top_rated_data(self, page=1):
        # Fetching top rated data
        url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/top_rated?{stringify_page(page)}&language=en-US&page=1"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    @cached(cache={})
    def get_popular_data(self, page=1):
        # Fetching popular data
        url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/popular?{stringify_page(page)}&language=en-US"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    @cached(cache={})
    def get_similar_data(self, id, page=1):
        url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/{id}/similar?{stringify_page(page)}&language=en-US&page=1"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    @cached(cache={})
    def get_recommendation_data(self, id, page=1):
        url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/{id}/recommendations?{stringify_page(page)}&language=en-US&page=1"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    def get_now_playing_data(self, page=1):
        if self.isMovie:
            url = f"https://api.themoviedb.org/3/movie/now_playing?language=en-US&{stringify_page(page)}"
        else:
            url = f"https://api.themoviedb.org/3/tv/on_the_air?language=en-US&{stringify_page(page)}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    @cached(cache={})
    def get_data(self, id):
        """Get single data by id"""
        url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/{id}?language=en-US"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    # Other utility functions

    @cached(cache={})
    def get_data_filtered_genres_on_popularity(self, genre_id, page=1):
        url = f"https://api.themoviedb.org/3/discover/{self.is_movie_arg()}?{stringify_page(page)}&sort_by=popularity.desc&with_genres={genre_id}"  # 28=Action 35=Comedy

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            print("Data fetched from API.")
            data = response.json()
            return data

    @cached(cache={})
    def get_data_filtered_genres_on_release(self, genre_id, page=1):
        url = f"https://api.themoviedb.org/3/discover/{self.is_movie_arg()}?{stringify_page(page)}&sort_by=primary_release_date.desc&with_genres={genre_id}"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    ####DATA GETTING OUT DATA####
    def get_small_details_out_single_movie(self, isMovie, data):
        """Get small details out of Single movie or serie """
        poster_path = data['poster_path']
        poster_base_url = 'https://image.tmdb.org/t/p/original'
        genres = data['genres']
        genre_ids = [each['id'] for each in genres]
        if poster_path:
            poster_url = poster_base_url + poster_path
        else:
            poster_url = 'https://image.tmdb.org/t/p/original/xypWiOvbEjyLTHRQp4G57hAcb0.jpg'
        if isMovie:
            movie_info = {
                "Title": data['title'],
                "Poster": poster_url,
                "Id": data['id'],
                "Type": "film",
                "Popularity": data['popularity'],
                "Genre": genres,
                "Overview": data['overview']
            }
        else:
            movie_info = {
                "Title": data['name'],
                "Poster": poster_url,
                "Id": data['id'],
                "Type": "serie",
                "Popularity": data['popularity'],
                "Genre": genres,
                "Overview": data['overview']
            }
        return movie_info

    def get_small_details_out_single_data(self, isMovie, data):
        """Get small details out of for loop data"""
        poster_path = data['poster_path']
        poster_base_url = 'https://image.tmdb.org/t/p/original'

        if poster_path:
            poster_url = poster_base_url + poster_path
        else:
            poster_url = 'https://image.tmdb.org/t/p/original/xypWiOvbEjyLTHRQp4G57hAcb0.jpg'
        if isMovie:
            movie_info = {
                "Title": data['original_title'],
                "Poster": poster_url,
                "Id": data['id'],
                "Type": "film",
                "Popularity": data['popularity'],
                "Genre": data['genre_ids'],
                "Overview": data['overview']
            }
        else:
            movie_info = {
                "Title": data['original_name'],
                "Poster": poster_url,
                "Id": data['id'],
                "Type": "serie",
                "Popularity": data['popularity'],
                "Genre": data['genre_ids'],
                "Overview": data['overview']
            }
        return movie_info

    def get_10_Titles_for_both(self, title, page=1):
        if page % 2 == 0:
            start_result = 10
            end_result = 20
            page_cor = page // 2
        else:
            start_result = 0
            end_result = 10
            page_cor = page // 2 + page % 2
        print("Fetching data...")
        film_details = []
        serie_details = []
        url = f"https://api.themoviedb.org/3/search/tv?query={title}&include_adult=true&language=en-US&{stringify_page(page_cor)}"
        url2 = f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=true&language=en-US&-{stringify_page(page_cor)}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            print("Data fetched from API.")
            data = response.json()
            serie_data = data['results'][start_result:end_result]
            for each in serie_data:
                serie_details.append(self.get_small_details_out_single_data(False, each))

        response = requests.get(url2, headers=self.headers)
        if response.status_code == 200:
            print("Data fetched from API.")
            data = response.json()
            film_data = data['results'][start_result:end_result]
            for each in film_data:
                film_details.append(self.get_small_details_out_single_data(True, each))
        return serie_details + film_details

    def get_small_details_out_big_data(self, data):
        """Get small details out of big data"""
        new_details = []
        new_data = data['results']
        for each in new_data:
            new_details.append(self.get_small_details_out_single_data(self.isMovie, each))
        return new_details


def make_faker_list():
    """Make a list of Popular movies and series for faker to use"""
    movie_id_list = []
    serie_id_list = []

    movie = Tmdb(True)
    serie = Tmdb(False)
    data_getters_movie = [movie.get_popular_data(), movie.get_trending_data(), movie.get_now_playing_data()]
    data_getters_serie = [serie.get_popular_data(), serie.get_trending_data(), serie.get_now_playing_data()]
    for each in data_getters_movie:
        movie_list = movie.get_small_details_out_big_data(each)
        for each in movie_list:
            movieBLa = {'Id': each['Id'], 'Type': each['Type']}
            movie_id_list.append(movieBLa)
    for each in data_getters_serie:
        serie_list = serie.get_small_details_out_big_data(each)
        for each in serie_list:
            serieBLa = {'Id': each['Id'], 'Type': each['Type']}
            serie_id_list.append(serieBLa)
    big_id_list = movie_id_list + serie_id_list
    return big_id_list

