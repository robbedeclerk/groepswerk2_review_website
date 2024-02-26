import requests

test_serie = "Queen of the south"


def connected():
    url = "https://api.themoviedb.org/3/authentication"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)

    print(response.text)


def trending():
    url = "https://api.themoviedb.org/3/trending/tv/day?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data


def top_rated():
    url = "https://api.themoviedb.org/3/tv/top_rated?language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # print(data)
        return data


def popular():
    url = "https://api.themoviedb.org/3/tv/popular?language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data


def print_series_titles_tmdb(data):
    # print(data["results"][0]["title"])
    nr = 1
    for each in data["results"]:
        print(f"{nr}: {each['name']}")
        nr += 1
    print()


def get_series_titles_tmdb(data):
    movie_list = []
    for each in data["results"]:
        movie_list.append(each['name'])
    return movie_list


# data = top_rated()
# print_movie_titles_tmdb(data)
# print()
# print()
# data = popular()
# print_movie_titles_tmdb(data)


def list_of_genres():
    url = "https://api.themoviedb.org/3/genre/tv/list?language=en"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # for each in data["genres"]:
        #     print(f"id:{each['id']} | Genre:{each['name']}")
        #     print(data)
        return data


def get_genre_id(genre_name, genres_data):
    for genre in genres_data['genres']:
        if genre['name'].lower() == genre_name.lower():
            return genre['id']
    return None


# print(get_genre_id('action', list_of_genres()))

list_of_genres = list_of_genres()


def data_filtered_genres_on_popularity(genre):
    genre_id = get_genre_id(genre, list_of_genres)
    url = f"https://api.themoviedb.org/3/discover/tv?sort_by=popularity.desc&with_genres={genre_id}"  # 28=Action 35=Comedy

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # print(data)
        return data


print_series_titles_tmdb(data_filtered_genres_on_popularity("comedy"))


# print_movie_titles_tmdb(data_filtered_genres_on_popularity("comedy"))
# print_movie_titles_tmdb(data_filtered_genres_on_popularity("action"))


def get_serie_poster(id):
    url = f"https://api.themoviedb.org/3/tv/{id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        poster_path = data['poster_path']
        poster_base_url = 'https://image.tmdb.org/t/p/original'
        poster_url = poster_base_url + poster_path
        return poster_url


def get_serie_id(serie):
    url = f"https://api.themoviedb.org/3/search/tv?query={serie}&include_adult=true&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)
    # print(response.text)
    if response.status_code == 200:
        data = response.json()
        return data["results"][0]["id"]


# print(get_serie_id(test_serie))
# print(get_serie_poster(get_serie_id(test_serie)))


def get_serie_data(id):
    url = f"https://api.themoviedb.org/3/tv/{id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)


get_serie_data(get_serie_id(test_serie))


def get_serie_details(id):
    url = f"https://api.themoviedb.org/3/tv/{id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        poster_url = get_serie_poster(id)
        genres = data['genres']
        genre = []
        for each in genres:
            genre.append(each['name'])
        print(f"Title: {data['name']}")
        print(f"Released: {data['first_air_date']}")
        print(f"Genre: {genre}")
        print(f"Seasons: {data['number_of_seasons']}")
        print(f"Episodes: {data['number_of_episodes']}")
        print(f"Overview: {data['overview']}")
        print(f"poster_url: {poster_url}")

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


get_serie_details(get_serie_id(test_serie))


# get_movie_details(get_movie_id("cars"))


def get_list_series_details(series_list):
    list_serie_details = []
    for serie_title in series_list:
        list_serie_details.append(get_serie_details(get_serie_id(serie_title)))
        print()
    return list_serie_details


def get_popular_series_details_filtered_on_genre(genre):
    serie_list = get_series_titles_tmdb(data_filtered_genres_on_popularity(genre))
    list_serie_details = get_list_series_details(serie_list)
    return list_serie_details


def get_popular_series_details():
    serie_list = get_series_titles_tmdb(popular())
    list_serie_details = get_list_series_details(serie_list)
    return list_serie_details


def get_top_rated_series_details():
    serie_list = get_series_titles_tmdb(top_rated())
    list_serie_details = get_list_series_details(serie_list)
    return list_serie_details


def get_trending_movies_details():
    serie_list = get_series_titles_tmdb(trending())
    list_serie_details = get_list_series_details(serie_list)
    return list_serie_details


# get_popular_series_details_filtered_on_genre("comedy")
# get_top_rated_series_details()
get_trending_movies_details()
# $$
#
data = get_popular_series_details()
print(data[0]['Title'])
# print_series_titles_tmdb(popular())
# print(get_serie_poster(get_serie_id("Binnelanders")))
