'''
This is a python flask server.
It recieves liked movies and recommended movies.
Calls the recommendation function from the movieReccomednations file.  
Sends back the recommended movies as a json.
'''
from flask import Flask #core of the Flask web framework 
from flask import request #way to handle HTTP request
from flask import jsonify #convert python dictionaries to JSON format
from flask_cors import CORS #Cross Origin Sharing allows web pages to make request to different domains than one served in original web page
from movieRecommendations7 import mult_input_recommendations   # import the reccomend movie function, this makes the entire movieRecommendation file run, it calculates the cosine similarity
from addToCSV import addMoviesToCSV     #import the add movies to csv function
from startPage import get_star_page_movies_info   #import the function that generates the movies for the starting page 
import json   #need to make the start page info a json format
from flask import session  #session variables, maintained over multiple api calls
import os # used to generate secret key 
from flask import make_response
from neo4jFunctions import create_relationships, collabritive_mult_input_recommendations


app = Flask(__name__)   # Create a Flask application instance
app.secret_key = os.urandom(24) 
CORS(app, supports_credentials=True)


@app.route('/start_page', methods=['GET'])
def another_function():
    result = get_star_page_movies_info()  #get the movies for the start page
    movie_ids = [movie['id'] for movie in result]  #get the tmdb ids for all the movie
    session['recommended_movie_tmdbids'] = []    #make the session variable empty
    session['recommended_movie_tmdbids'].extend(movie_ids)  # add all the ids of the start page movies
    session.modified = True   # let the session know this variable is modifified
    addMoviesToCSV(movie_ids)    #add the movies to the csv if nessecary 
    return jsonify(json.dumps(result)) # return the result as a json


@app.route('/recommendations', methods=['POST'])  # Define a route for your API, which listens for POST requests at '/my_api'
def my_function():
    data = request.get_json() # Extract JSON data from the incoming request
    allLikedMovies = data.get("allLikedMovies")  # get all the liked movies
    result = mult_input_recommendations(allLikedMovies, session['recommended_movie_tmdbids'])  # get newly recommended movies
    session['recommended_movie_tmdbids'].extend(result)   # add them to the previosuly recommemnded movies
    session.modified = True #let the session know the this varaible is modified
    return jsonify(result)  # Return the result in form JSON

@app.route('/collaborative_recommendations', methods=['POST'])
def collabritive_recommendations():
    data = request.get_json()
    timeSpentData = data.get("timeSpentData")
    result = collabritive_mult_input_recommendations(timeSpentData, session['recommended_movie_tmdbids'])
    session['recommended_movie_tmdbids'].extend(result)
    session.modified = True
    return jsonify(result)

@app.route('/time_data', methods=['POST'])  # Define a route for your API, which listens for POST requests at '/my_api'
def time_data_function():
    data = request.get_json() # Extract JSON data from the incoming request
    timeSpentData = data.get("timeSpentData")
    create_relationships(timeSpentData)
    return make_response('', 200)
    
    
if __name__ == '__main__':  # Check if this script is the main program
    app.run(host='0.0.0.0', port=5001)
    #app.run()  #run the Flask application

    