import requests
import json


def fetchMovieById(tmdbId):
    url = f"https://api.themoviedb.org/3/movie/{tmdbId}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDIwYzY4ZDMxNmRkMjM0NGVkOWI5ZjRmNDNkMzIyYiIsInN1YiI6IjY1MDc1ODFhM2NkMTJjMDE0ZWJmN2U2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.URBinN5yI5YymjjRmdSmr4nEHXkQfsMFqToTyv9QTt0"
    }
    response = requests.get(url, headers=headers)
    return response.json()   # this is a json 

def searchMovieByTitle(movieName):
    url = f"https://api.themoviedb.org/3/search/movie?query={movieName}&include_adult=false&language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDIwYzY4ZDMxNmRkMjM0NGVkOWI5ZjRmNDNkMzIyYiIsInN1YiI6IjY1MDc1ODFhM2NkMTJjMDE0ZWJmN2U2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.URBinN5yI5YymjjRmdSmr4nEHXkQfsMFqToTyv9QTt0"
    }
    response = requests.get(url, headers=headers)
    return response.text   # this is a json 

def getMovieByTitle(movieName):
    url = f"https://api.themoviedb.org/3/search/movie?query={movieName}&include_adult=false&language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDIwYzY4ZDMxNmRkMjM0NGVkOWI5ZjRmNDNkMzIyYiIsInN1YiI6IjY1MDc1ODFhM2NkMTJjMDE0ZWJmN2U2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.URBinN5yI5YymjjRmdSmr4nEHXkQfsMFqToTyv9QTt0"
    }
    response = requests.get(url, headers=headers)
    first_result = response.json().get("results", [])[0]
    return first_result

def getMoviesUsingTitles(movieTitles):
    results = []
    for title in movieTitles:
        movie_info = getMovieByTitle(title)
        if isinstance(movie_info, dict):  # Check if movie_info is a dictionary
            results.append(movie_info)
    #print(type(results))
    results_json_array = json.dumps(results, indent=2)
    #print(type(results_json_array))
    return results_json_array
    

# get crew 
#so should you return as json or txt
def getMovieCrewById(tmdbId):
    url = f"https://api.themoviedb.org/3/movie/{tmdbId}/credits?language=en-US"  #get movie crew information 
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDIwYzY4ZDMxNmRkMjM0NGVkOWI5ZjRmNDNkMzIyYiIsInN1YiI6IjY1MDc1ODFhM2NkMTJjMDE0ZWJmN2U2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.URBinN5yI5YymjjRmdSmr4nEHXkQfsMFqToTyv9QTt0"
    }
    response = requests.get(url, headers=headers)
    return response.json() 

# Get the top trending movies from tmdb
def fetch_trending_movies(page=1):
    url = f"https://api.themoviedb.org/3/trending/movie/day?language=en-US&page={page}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDIwYzY4ZDMxNmRkMjM0NGVkOWI5ZjRmNDNkMzIyYiIsInN1YiI6IjY1MDc1ODFhM2NkMTJjMDE0ZWJmN2U2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.URBinN5yI5YymjjRmdSmr4nEHXkQfsMFqToTyv9QTt0"
    }
    response = requests.get(url, headers=headers)
    return response.text

# Get the top rated movies from tmdb
def fetch_top_rated_movies(page=1):
    url = f"https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={page}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDIwYzY4ZDMxNmRkMjM0NGVkOWI5ZjRmNDNkMzIyYiIsInN1YiI6IjY1MDc1ODFhM2NkMTJjMDE0ZWJmN2U2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.URBinN5yI5YymjjRmdSmr4nEHXkQfsMFqToTyv9QTt0"
    }
    response = requests.get(url, headers=headers)
    return response.text