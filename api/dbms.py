import requests

test_movie = "John Wick"


def connected():
    url = "https://api.themoviedb.org/3/authentication"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)

    print(response.text)


def top_rated():
    url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"

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
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data


def print_movie_titles_tmdb(data):
    # print(data["results"][0]["title"])
    nr = 1
    for each in data["results"]:
        print(f"{nr}: {each['title']}")
        nr += 1


def get_movie_titles_tmdb(data):
    movie_list = []
    for each in data["results"]:
        movie_list.append(each['title'])
    return movie_list


# data = top_rated()
# print_movie_titles_tmdb(data)
# print()
# print()
# data = popular()
# print_movie_titles_tmdb(data)


def list_of_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for each in data["genres"]:
            print(f"id:{each['id']} | Genre:{each['name']}")
        print(data)
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
    url = f"https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&with_genres={genre_id}"  # 28=Action 35=Comedy

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # print(data)
        return data


print_movie_titles_tmdb(data_filtered_genres_on_popularity("comedy"))
print_movie_titles_tmdb(data_filtered_genres_on_popularity("action"))


def get_movie_poster(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"

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


def get_movie_id(movie):
    url = f"https://api.themoviedb.org/3/search/movie?query={movie}&include_adult=true&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)
    # print(response.text)
    if response.status_code == 200:
        data = response.json()
        return data["results"][0]["id"]


def get_movie_data(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)


def get_movie_details(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMGU4ZGIyOTNmZGRlOTc3YWEzMDQ0YjUwMmRmMDI5NyIsInN1YiI6IjY1YzIyOTdkZWZlYTdhMDE4NDUyY2I2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1F8ZMiAf1b20cYYmqtAuv7kCNBBHTOvAETk5kxI61I"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        poster_url = get_movie_poster(id)
        genres = data['genres']
        genre = []
        for each in genres:
            genre.append(each['name'])
        print(f"Title: {data['title']}")
        print(f"Released: {data['release_date']}")
        print(f"Runtime: {data['runtime']}")
        print(f"Genre: {genre}")
        print(f"Overview: {data['overview']}")
        print(f"poster_url: {poster_url}")

        movie_info = {
            "Title": data['title'],
            "Released": data['release_date'],
            "Runtime": data['runtime'],
            "Genre": genre,
            "Overview": data['overview'],
            "Poster": poster_url
        }
        return movie_info


get_movie_details(get_movie_id("cars"))


def get_list_movie_details(movie_list):
    list_movie_details = []
    for movie_title in movie_list:
        list_movie_details.append(get_movie_details(get_movie_id(movie_title)))
        print()
    return list_movie_details


def get_popular_movies_details_filtered_on_genre(genre):
    movie_list = get_movie_titles_tmdb(data_filtered_genres_on_popularity(genre))
    list_movie_details = get_list_movie_details(movie_list)
    return list_movie_details


def get_popular_movies_details():
    movie_list = get_movie_titles_tmdb(popular())
    list_movie_details = get_list_movie_details(movie_list)
    return list_movie_details


def get_top_rated_movies_details():
    movie_list = get_movie_titles_tmdb(top_rated())
    list_movie_details = get_list_movie_details(movie_list)
    return list_movie_details


# get_movie_data(920)
print(get_movie_poster(920))

get_top_rated_movies_details()
get_movie_details(245891)
