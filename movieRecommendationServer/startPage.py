# this api call could be useful to get the more movies for the starting page  
# https://developer.themoviedb.org/reference/movie-now-playing-list 


import requests
from bs4 import BeautifulSoup
import re
import requests
import json
import random
from tmdbFetchFunctions import fetch_trending_movies, fetch_top_rated_movies, getMoviesUsingTitles 

# Function to scrape the Mojo highest grossing page
def scrape_boxofficemojo_year():
    url = 'https://www.boxofficemojo.com/year/world/'   #url of the website we are scraping
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'} #header info so it thinks its a browser
    response = requests.get(url, headers=headers)  #search it
    soup = BeautifulSoup(response.text, 'html.parser') #get the hhml
    movie_titles = soup.select('td.mojo-field-type-release_group a')   #select td tags with class mojo-field-type-release_group in them select a
    final_movie_titles = [] # an array for the movies titles we get from the web scrape
    for title in movie_titles:
        cleaned_title = title.text.strip()  #extract the the text from the html tag, remove leading and trailing white space
        final_movie_titles.append(cleaned_title) # append it to the final array
    return final_movie_titles
    
# Function to scrape the IMDB top chart
def scrape_imdb_top():
    url = 'https://www.imdb.com/chart/top/'     #url of the website we are scraping
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}  #header info so it thinks its a browser
    response = requests.get(url, headers=headers)  #search it
    soup = BeautifulSoup(response.text, 'html.parser')  #get the hhml
    movie_titles = soup.select('a.ipc-title-link-wrapper h3') #selct a tags with class ipc-title-link-wrapper in them select h3
    final_movie_titles = [] # an array for the movies titles we get from the web scrape
    for title in movie_titles:
        cleaned_title = title.text.strip() #extract the the text from the html tag, remove leading and trailing white space
        if re.match(r'^\d', cleaned_title): #If it start with a digit
            cleaned_title = re.sub(r'^\d+\.\s*', '', cleaned_title)  # remove the leading number from the title
            final_movie_titles.append(cleaned_title)  # append it to the final array
    return final_movie_titles #there is 250 movies in the website list
 
# Function to scrape the IMDB popular page
def scrape_imdb_popular():
    url = 'https://www.imdb.com/chart/moviemeter/' #url of the website we are scraping
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}   #header info so it thinks its a browser
    response = requests.get(url, headers=headers) #search it
    soup = BeautifulSoup(response.text, 'html.parser') #get the hhml
    movie_titles = soup.select('a.ipc-title-link-wrapper h3') #selct a tags with class ipc-title-link-wrapper in them select h3
    final_movie_titles = [] # an array for the movies titles we get from the web scrape
    for title in movie_titles:
        cleaned_title = title.text.strip() #extract the the text from the html tag, remove leading and trailing white space
        final_movie_titles.append(cleaned_title)  # append it to the final array
    return final_movie_titles[:100] #there are only 100 movies in the website list

#Extract just movie names from tmdb fetch result
def extract_movie_names(response_text):
    data = json.loads(response_text) # Parse JSON data
    titles = [movie["title"] for movie in data.get("results", [])]   # Extract titles
    return titles
  
#Fetch top 5 pages of top rated movies
#Extract only the movies names
def get_top_rated_movie_names():
    movie_titles = []
    for page_number in range(1, 51):   # get the first 50 pages, 50*20 so 1000 results
        response_text = fetch_top_rated_movies(page=page_number)
        movie_titles.extend(extract_movie_names(response_text))
    return movie_titles

#Fetch top 5 pages of trending movies
#Extract only the movies names 
def get_trending_movie_names():
    movie_titles = []
    for page_number in range(1, 5):    
        response_text = fetch_trending_movies(page=page_number)
        movie_titles.extend(extract_movie_names(response_text))
    return movie_titles

#Get only the common elements in two arrays
def common_strings(array1, array2):
    common_elements = set(array1) & set(array2)
    result_array = list(common_elements)
    return result_array
    
#Return true if two arrays have common elements
def have_common_strings(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)
    return bool(set1.intersection(set2))

# Return an array that contains only the elements not in the second array
def exclude_common_elements(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)
    unique_elements_arr1 = set1.difference(set2)
    return list(unique_elements_arr1)

# Get some number of random elements from an array   
def get_random_strings(string_array, num_strings):
    num_strings = min(num_strings, len(string_array))  # Ensure that the requested number of strings is not greater than the array length
    random_strings = random.sample(string_array, num_strings)  # Use random.sample to get a random subset of the array
    return random_strings




# we use global variables here because we want to find all the movies once, and then just select some number of them 
top_rated_movies_info = []
popular_movies_info = []

def all_movies_info():    #2 minutes
    global top_rated_movies_info 
    global popular_movies_info 
    top_rated_movies = common_strings(get_top_rated_movie_names(),scrape_imdb_top())    # get the movies common to the top rated movies from tmdb and imdb 
    popular_movies = common_strings(get_trending_movie_names(),scrape_imdb_popular())   # get the movies common to the top trending movies from tmdb and popular movies from imdb 
    top_rated_movies = exclude_common_elements(top_rated_movies, popular_movies);   # exlude anything that is in top rated movies and popular movies
    top_rated_movies_info = json.loads(getMoviesUsingTitles(top_rated_movies))
    popular_movies_info = json.loads(getMoviesUsingTitles(popular_movies))


# def all_movies_info():
#     global top_rated_movies_info 
#     global popular_movies_info 
#     top_rated_movies_info = json.loads(getMoviesUsingTitles(["Modern Times", "The Thing"]))
#     popular_movies_info = json.loads(getMoviesUsingTitles(["Barbie", "Oppenheimer", "The Iron Claw", "The Boys In The Boat"]))


def get_star_page_movies_info():
    global top_rated_movies_info 
    global popular_movies_info 
    top_movies = random.sample(top_rated_movies_info, 4)
    popular_movies = random.sample(popular_movies_info, 8)
    all_movies = top_movies + popular_movies
    random.shuffle(all_movies)
    return all_movies


all_movies_info()