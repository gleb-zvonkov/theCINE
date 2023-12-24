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
from movieRecommendations5 import mult_input_recommendations   # import the reccomend movie function, this makes the entire movieRecommendation file run, it calculates the cosine similarity
from addToCSV import addMoviesToCSV
from startPage import get_star_page_movies_info

# the app.js makes request to this flask server 

app = Flask(__name__)   # Create a Flask application instance
CORS(app) # apply cors on the application 


@app.route('/my_api', methods=['POST'])  # Define a route for your API, which listens for POST requests at '/my_api'
def my_function():
    data = request.get_json() # Extract JSON data from the incoming request
    allLikedMovies = data.get("allLikedMovies", [])
    allRecommendedMovies = data.get("allRecommendedMovies", [])
    addMoviesToCSV(allRecommendedMovies)  # in the case that movies are not in the csv, this should be adding to database  
    result = mult_input_recommendations(allLikedMovies,allRecommendedMovies) #.tolist()
    return jsonify(result)  # Return the result in form JSON


@app.route('/start_page', methods=['POST'])
def another_function():
    result = get_star_page_movies_info() 
    return jsonify(result)


if __name__ == '__main__':  # Check if this script is the main program
    app.run()  #run the Flask application

    