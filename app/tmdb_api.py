from cachetools import TTLCache, cached
import requests
import json


class Tmdb:

    def __init__(self, isMovie):
        self.isMovie = isMovie
        self.cache = TTLCache(maxsize=1000, ttl=3600)
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
        }

    def get_type(self):
        if self.isMovie:
            return "film"
        else:
            return "serie"

    def is_movie_arg(self):
        if self.isMovie:
            is_movie_arg = "movie"
        else:
            is_movie_arg = "tv"
        return is_movie_arg

    def title_arg(self):
        if self.isMovie:
            title_arg = 'title'
        else:
            title_arg = 'name'
        return title_arg

    def connected(self):
        url = "https://api.themoviedb.org/3/authentication"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            print("Verbonden met TheMovieDB")
        else:
            print("Kon niet verbinden met TheMovieDB")

    @cached(cache={})
    def list_of_genres(self):
        url = f"https://api.themoviedb.org/3/genre/{self.is_movie_arg()}/list?language=en"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    def get_genre_id(self, genre_name):
        genres_data = self.list_of_genres()
        for genre in genres_data['genres']:
            if genre['name'].lower() == genre_name.lower():
                return genre['id']
        return None

    @cached(cache={})
    def get_trending_data(self):
        url = f"https://api.themoviedb.org/3/trending/{self.is_movie_arg()}/day?language=en-US"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    @cached(cache={})
    def get_top_rated_data(self):
        url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/top_rated?language=en-US&page=1"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    @cached(cache={})
    def get_popular_data(self):
        url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/popular?language=en-US&page=1"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    def print_titles(self, data):
        nr = 1
        for each in data["results"]:
            print(f"{nr}: {each[self.title_arg()]}")
            nr += 1
        print()

    def get_titles(self, data):
        movie_list = []
        for each in data["results"]:
            movie_list.append(each[self.title_arg()])
        return movie_list

    @cached(cache={})
    def get_data_filtered_genres_on_popularity(self, genre):
        genre_id = self.get_genre_id(genre)
        url = f"https://api.themoviedb.org/3/discover/{self.is_movie_arg()}?sort_by=popularity.desc&with_genres={genre_id}"  # 28=Action 35=Comedy

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    @cached(cache={})
    def get_poster(self, id):
        url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/{id}?language=en-US"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            poster_path = data['poster_path']
            poster_base_url = 'https://image.tmdb.org/t/p/original'
            poster_url = poster_base_url + poster_path
            return poster_url

    @cached(cache={})
    def get_id(self, title):
        url = f"https://api.themoviedb.org/3/search/{self.is_movie_arg()}?query={title}&include_adult=true&language=en-US&page=1"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data["results"][0]["id"]

    @cached(cache={})
    def get_data(self, id):
        url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/{id}?language=en-US"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    @cached(cache={})
    def get_details(self, id):
        print("Fetching data...")
        url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/{id}?language=en-US"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            print("Data fetched from API.")
            data = response.json()
            poster_url = self.get_poster(id)
            genres = data['genres']
            genre = []
            for each in genres:
                genre.append(each['name'])
            if self.isMovie:
                movie_info = {
                    "Title": data['title'],
                    "Released": data['release_date'],
                    "Runtime": data['runtime'],
                    "Genre": genre,
                    "Overview": data['overview'],
                    "Poster": poster_url
                }
            else:
                movie_info = {
                    "Title": data['name'],
                    "Released": data['first_air_date'],
                    "Genre": genre,
                    "Seasons": data['number_of_seasons'],
                    "Episodes": data['number_of_episodes'],
                    "Overview": data['overview'],
                    "Poster": poster_url
                }
            return movie_info

    def get_list_details(self, data_list):
        list_details = []
        for title in data_list:
            list_details.append(self.get_details(self.get_id(title)))
        return list_details

    def get_details_from_data(self, data):
        list_details = self.get_list_details(self.get_titles(data))
        return list_details

    def get_details_filtered_on_genre(self, genre):
        list_details = self.get_details_from_data(self.get_data_filtered_genres_on_popularity(genre))
        return list_details

    def get_popular_details(self):
        list_details = self.get_list_details(self.get_titles(self.get_popular_data()))
        return list_details

    def get_top_rated_details(self):
        list_details = self.get_list_details(self.get_titles(self.get_top_rated_data()))
        return list_details

    def get_trending_details(self):
        list_details = self.get_list_details(self.get_titles(self.get_trending_data()))
        return list_details


# import time

# movie = Tmdb(True)
# serie = Tmdb(False)

# start_time = time.time()
# popular_details_data = movie.get_popular_details()
# end_time = time.time()
# exec_time_1 = end_time - start_time
# # movie.print_titles(movie.get_popular_data())
# # print()
# #
# # serie.print_titles(serie.get_popular_data())

# for thing in popular_details_data:
#     print(thing)

# start_time = time.time()
# popular_details_data2 = movie.get_popular_details()
# end_time = time.time()
# exec_time_2 = end_time - start_time
# print(popular_details_data2[0])
# # Cijfers na ::: is alles cached
# print(f"ZonderCache: {exec_time_1}")  # AVG: 25.3, 25.1, 26.04:::25.4, 25.5
# print(f"MetCaching: {exec_time_2}")  # AVG: 8.57, 8.73, 8.7:::0, 0   TOP
