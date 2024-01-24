import csv
import requests
import json
from tmdbFetchFunctions import fetchMovieById, getMovieCrewById 

#this function adds a movie to the CSV
#it fetches movie data and crew data
#rearanges it into the proper format 
#writes it to a csv
csv_file_path = '45000_movies/movies_metadata_final_added.csv'
tmdb_ids_in_csv = set() #built-in data type that represents an unordered collection of unique elements


# collect all the information to be added to the csv
def getMovieInfoForCSV(tmdbId):
    movie_data = fetchMovieById(tmdbId)
    crew_data = getMovieCrewById(tmdbId)
    
    genres = [genre['name'] for genre in movie_data.get('genres', [])] # get the genres 
    popularity = movie_data.get('popularity')    # get the popularity score
    release_date = movie_data.get('release_date')  # get the release data 
    title = movie_data.get('title')               # get the title 
    vote_average = movie_data.get('vote_average')  # get the averge vote 
    vote_count = movie_data.get('vote_count')    # the the number of votes the movies has 
    
    crew_list = crew_data.get("crew", [])  #get the crew 
    director = next((crew_member for crew_member in crew_list if crew_member.get("job") == "Director"), None)   # get the director 
    director_name = director.get("name", " ")  # get the director name
    
    cast_list = crew_data.get("cast", []) # get the cast 
    sorted_cast = sorted(cast_list, key=lambda x: x.get("order", 0))  # sort the cast list based on the 'order' key
    top_3_actor_names = [actor['name'] for actor in sorted_cast[:3]]  # get the top 3 actors
    
    return [genres, tmdbId, popularity, release_date, title, vote_average, vote_count, director_name, top_3_actor_names]   # put it all together 


# add new movie to csv 
# does not check if it already exists
def addMovieToCSV(tmdbId):
    new_data = getMovieInfoForCSV(tmdbId) 
    with open(csv_file_path, 'a', newline='') as file:   # open the csv
        csv_writer = csv.writer(file)  #csv writer object 
        csv_writer.writerow(new_data)  #write the data
        print(f"Data for tmdbId {tmdbId} added to the CSV.") # print a statment indicating its been added 

        
# need to calculate the tmdb_ids_in_csv once and then add to it
# right now you calcaulting each time you try to add a movie to the csv
def findMoviesInCSV():
    global tmdb_ids_in_csv
    try:
        with open(csv_file_path, 'r', newline='') as csvfile:  # open csv file 
            csv_reader = csv.reader(csvfile)   # create a csv reader object 
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                tmdb_ids_in_csv.add(int(row[1]))  # Assuming tmdbId is in the second column at it to the tmdb_id
    except FileNotFoundError:
        pass  # If the file doesn't exist, no need to check tmdbIds


# checks if id already exist 
def addMoviesToCSV(tmdbIds):  
    global tmdb_ids_in_csv
    tmdb_ids_to_add = [Id for Id in tmdbIds if Id not in tmdb_ids_in_csv]   # the tmdb ids not already in the csv 
    for Id in tmdb_ids_to_add:  # add them to the csv 
        addMovieToCSV(Id)
        tmdb_ids_in_csv.add(Id)

findMoviesInCSV()
