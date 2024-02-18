from abc import ABC, abstractmethod
import requests
import redis
import json

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


class Tmdb:

    def __init__(self, isMovie):
        self.isMovie = isMovie
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
        }

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

    def get_trending_data(self):
        url = f"https://api.themoviedb.org/3/trending/{self.is_movie_arg()}/day?language=en-US"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    def get_top_rated_data(self):
        url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/top_rated?language=en-US&page=1"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

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

    def get_data_filtered_genres_on_popularity(self, genre):
        genre_id = self.get_genre_id(genre)
        url = f"https://api.themoviedb.org/3/discover/{self.is_movie_arg()}?sort_by=popularity.desc&with_genres={genre_id}"  # 28=Action 35=Comedy

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    def get_poster(self, id):
        url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/{id}?language=en-US"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            poster_path = data['poster_path']
            poster_base_url = 'https://image.tmdb.org/t/p/original'
            poster_url = poster_base_url + poster_path
            return poster_url

    def get_id(self, title):
        url = f"https://api.themoviedb.org/3/search/{self.is_movie_arg()}?query={title}&include_adult=true&language=en-US&page=1"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data["results"][0]["id"]

    def get_data(self, id):
        url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/{id}?language=en-US"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    def get_details(self, id):
        cached_data = redis_client.get(f'{self.isMovie}_{id}')
        if cached_data:
            return json.loads(cached_data)
        else:
            url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/{id}?language=en-US"

            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
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
                redis_client.set(f'{self.isMovie}_{id}', json.dumps(movie_info))
                redis_client.expire(f'{self.isMovie}_{id}', 3600)
                return movie_info

    def get_list_details(self, data_list):
        list_details = []
        for title in data_list:
            list_details.append(self.get_details(self.get_id(title)))
        return list_details

    def get_details_filtered_on_genre(self, genre):
        list_details = self.get_list_details(self.get_titles(self.get_data_filtered_genres_on_popularity(genre)))
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


movie = Tmdb(True)
serie = Tmdb(False)

popular_details_data = movie.get_popular_details()
movie.print_titles(movie.get_popular_data())
print()

serie.print_titles(serie.get_popular_data())

for thing in popular_details_data:
    print(thing)
