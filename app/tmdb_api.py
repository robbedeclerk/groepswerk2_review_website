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

    def get_5_Titles_for_both(self, title):
        print("Fetching data...")
        film_details = []
        serie_details = []
        url = f"https://api.themoviedb.org/3/search/tv?query={title}&include_adult=true&language=en-US&page=1"
        url2 = f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=true&language=en-US&page=1"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            print("Data fetched from API.")
            data = response.json()
            serie_data = data['results'][0:5]
            for each in serie_data:
                serie_details.append(self.get_small_details_out_single_data(False, each))

        response = requests.get(url2, headers=self.headers)
        if response.status_code == 200:
            print("Data fetched from API.")
            data = response.json()
            film_data = data['results'][0:5]
            for each in film_data:
                film_details.append(self.get_small_details_out_single_data(True, each))
            print(film_details)
        return serie_details + film_details
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
            # print(response)
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

    def get_similar_data(self, id):
        url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/{id}/similar?language=en-US&page=1"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

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
            if poster_path:
                poster_base_url = 'https://image.tmdb.org/t/p/original'
                poster_url = poster_base_url + poster_path
                return poster_url
            else:
                return 'https://image.tmdb.org/t/p/original/xypWiOvbEjyLTHRQp4G57hAcb0.jpg'

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

    def get_details_out_data(self, data):
        datalist = []
        if data['results']:
            for each in data['results']:
                if self.isMovie:
                    movie_info = {
                        "Title": each['original_title'],
                        "Released": each['release_date'],
                        # "Runtime": each['runtime'],
                        "Overview": each['overview'],
                        "Poster": each['poster_path'],
                        "Id": each['id']
                    }
                else:
                    movie_info = {
                        "Title": each['original_name'],
                        "Released": each['first_air_date'],
                        "Overview": each['overview'],
                        "Poster": each['poster_path'],
                        "Id": each['id']
                    }
                datalist.append(movie_info)
            return datalist
        if self.isMovie:
            movie_info = {
                "Title": data['original_title'],
                "Released": data['release_date'],
                "Runtime": data['runtime'],
                "Overview": data['overview'],
                "Poster": data['poster_path'],
                "Id": data['id']
            }
        else:
            movie_info = {
                "Title": data['original_name'],
                "Released": data['first_air_date'],
                "Overview": data['overview'],
                "Poster": data['poster_path'],
                "Id": data['id']
            }
        return movie_info

    def get_small_details_out_single_data(self,isMovie, data):
        poster_path = data['poster_path']
        poster_base_url = 'https://image.tmdb.org/t/p/original'

        if poster_path:
            poster_url = poster_base_url + poster_path
        else:
            poster_url = 'https://image.tmdb.org/t/p/original/xypWiOvbEjyLTHRQp4G57hAcb0.jpg'
        if isMovie:
            movie_info = {
                "Title": data['title'],
                "Poster": poster_url,
                "Id": data['id'],
                "IsMovie": "film"
            }
        else:
            movie_info = {
                "Title": data['name'],
                "Poster": poster_url,
                "Id": data['id'],
                "IsMovie": "serie"

            }
        return movie_info
    def get_small_details_out_data(self, data):
        datalist = []
        poster_base_url = 'https://image.tmdb.org/t/p/original'

        if data['results']:
            for each in data['results']:
                poster_path = each['poster_path']
                if poster_path:
                    poster_url = poster_base_url + poster_path
                else:
                    poster_url = 'https://image.tmdb.org/t/p/original/xypWiOvbEjyLTHRQp4G57hAcb0.jpg'
                if self.isMovie:
                    movie_info = {
                        "Title": each['title'],
                        "Poster": poster_url,
                        "Id": each['id']
                    }
                else:
                    movie_info = {
                        "Title": each['name'],
                        "Poster": poster_url,
                        "Id": each['id']
                    }
                datalist.append(movie_info)
            return datalist
        poster_path = data['poster_path']
        if poster_path:
            poster_url = poster_base_url + poster_path
        else:
            poster_url = 'https://image.tmdb.org/t/p/original/xypWiOvbEjyLTHRQp4G57hAcb0.jpg'
        if self.isMovie:
            movie_info = {
                "Title": data['title'],
                "Poster": poster_url,
                "Id": data['id']
            }
        else:
            movie_info = {
                "Title": data['name'],
                "Poster": poster_url,
                "Id": data['id']
            }
        return movie_info

    @cached(cache={})
    def get_details(self, id):
        print("Fetching data...")
        url = f"https://api.themoviedb.org/3/{self.is_movie_arg()}/{id}?language=en-US"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            print("Data fetched from API.")
            data = response.json()
            poster_path = data['poster_path']
            poster_base_url = 'https://image.tmdb.org/t/p/original'
            poster_url = poster_base_url + poster_path
            genres = data['genres']
            genre = []
            for each in genres:
                genre.append(each['name'])
            if self.isMovie:
                movie_info = {
                    "Title": data['title'],
                    "Original_title": data['original_title'],
                    "Released": data['release_date'],
                    "Runtime": data['runtime'],
                    "Genre": genre,
                    "Overview": data['overview'],
                    "Poster": poster_url,
                    "Id": data['id']
                }
            else:
                movie_info = {
                    "Title": data['name'],
                    "Original_title": data['original_name'],
                    "Released": data['first_air_date'],
                    "Genre": genre,
                    "Seasons": data['number_of_seasons'],
                    "Episodes": data['number_of_episodes'],
                    "Overview": data['overview'],
                    "Poster": poster_url,
                    "Id": data['id']
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

    def get_similar_details(self, id):
        list_details = self.get_details_from_data(self.get_similar_data(id))
        return list_details


# import time
#
# #
# movie = Tmdb(True)
# serie = Tmdb(False)
# #
# start_time = time.time()
# popular_details_data = movie.get_popular_data()
# end_time = time.time()
# exec_time_1 = end_time - start_time
# # # # movie.print_titles(movie.get_popular_data())
# # # # print()
# # # #
# # # # serie.print_titles(serie.get_popular_data())
# #
# # # for thing in popular_details_data:
# # #     print(thing)
# #
# start_time = time.time()
# popular_details_data2 = movie.get_details_out_data(movie.get_popular_data())
# end_time = time.time()
# exec_time_2 = end_time - start_time
# # # print(popular_details_data2[0])
# # # # Cijfers na ::: is alles cached
# print(f"ZonderCache: {exec_time_1}")  # AVG: 25.3, 25.1, 26.04:::25.4, 25.5
# print(f"MetCaching: {exec_time_2}")  # AVG: 8.57, 8.73, 8.7:::0, 0   TOP
# movie = Tmdb(True)
# serie = Tmdb(False)
# # # similar_details_details = movie.get_similar_details(400)
# # similar_details_data = movie.get_similar_data(1072790)
# # # print(similar_details_details)
# # print(similar_details_data)
# #
# # print(movie.get_small_details_out_data(similar_details_data))
#
#
# # movieshit = movie.get_details_filtered_on_genre("Action")
# # print(movieshit)
# # id = movie.get_id("404")
# # print(id)
# # poster = movie.get_poster(1058048)
# # print(poster)
# movie = Tmdb(True)
# print(movie.get_popular_data())
# print(serie.get_popular_data())

# print(movie.get_5_Titles_for_both("Avatar"))
