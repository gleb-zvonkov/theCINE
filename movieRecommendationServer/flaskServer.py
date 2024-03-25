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
from contentBased import recommendations_kmean, recommendations_knn
from addToCSV import addMoviesToCSV     #import the add movies to csv function
from startPage import get_star_page_movies_info   #import the function that generates the movies for the starting page 
import json   #need to make the start page info a json format
from flask import session  #session variables, maintained over multiple api calls
import os # used to generate secret key 
from flask import make_response
from graphBased import create_relationships, collabritive_mult_input_recommendations
from matrixFactorization import matrix_factorization_reccomendations, write_to_csv
from timeDataStorage import record_time_data, record_click_data
import random
from neuralNetwork import neural_network_reccomendations
# from config import MOVIE_DATA_PATH, RESULT_DATA_PATH, SESSION_DATA_PATH


app = Flask(__name__)   # Create a Flask application instance
app.secret_key = os.urandom(24) 
CORS(app, supports_credentials=True)


@app.route('/start_page', methods=['GET'])
def another_function():
    result = get_star_page_movies_info()  #get the movies for the start page
    #result = [{'adult': False, 'backdrop_path': '/9R2FuGT0BeZl8usfsfqIcO7KK7v.jpg', 'genre_ids': [28, 53, 27], 'id': 514847, 'original_language': 'en', 'original_title': 'The Hunt', 'overview': "Twelve strangers wake up in a clearing. They don't know where they are—or how they got there. In the shadow of a dark internet conspiracy theory, ruthless elitists gather at a remote location to hunt humans for sport. But their master plan is about to be derailed when one of the hunted turns the tables on her pursuers.", 'popularity': 29.895, 'poster_path': '/wxPhn4ef1EAo5njxwBkAEVrlJJG.jpg', 'release_date': '2020-03-11', 'title': 'The Hunt', 'video': False, 'vote_average': 6.645, 'vote_count': 2971}, {'adult': False, 'backdrop_path': '/fGe1ej335XbqN1j9teoDpofpbLX.jpg', 'genre_ids': [53, 9648, 80], 'id': 915935, 'original_language': 'fr', 'original_title': "Anatomie d'une chute", 'overview': "A woman is suspected of her husband's murder, and their blind son faces a moral dilemma as the sole witness.", 'popularity': 301.092, 'poster_path': '/kQs6keheMwCxJxrzV83VUwFtHkB.jpg', 'release_date': '2023-08-23', 'title': 'Anatomy of a Fall', 'video': False, 'vote_average': 7.667, 'vote_count': 1346}, {'adult': False, 'backdrop_path': '/bdD39MpSVhKjxarTxLSfX6baoMP.jpg', 'genre_ids': [18, 36, 10752], 'id': 857, 'original_language': 'en', 'original_title': 'Saving Private Ryan', 'overview': 'As U.S. troops storm the beaches of Normandy, three brothers lie dead on the battlefield, with a fourth trapped behind enemy lines. Ranger captain John Miller and seven men are tasked with penetrating German-held territory and bringing the boy home.', 'popularity': 63.503, 'poster_path': '/uqx37cS8cpHg8U35f9U5IBlrCV3.jpg', 'release_date': '1998-07-24', 'title': 'Saving Private Ryan', 'video': False, 'vote_average': 8.213, 'vote_count': 15114}, {'adult': False, 'backdrop_path': '/4l65BWqJBl7hBwdIwp2nQdwsOuw.jpg', 'genre_ids': [18, 36], 'id': 850165, 'original_language': 'en', 'original_title': 'The Iron Claw', 'overview': 'The true story of the inseparable Von Erich brothers, who made history in the intensely competitive world of professional wrestling in the early 1980s. Through tragedy and triumph, under the shadow of their domineering father and coach, the brothers seek larger-than-life immortality on the biggest stage in sports.', 'popularity': 94.05, 'poster_path': '/nfs7DCYhgrEIgxKYbITHTzKsggf.jpg', 'release_date': '2023-12-21', 'title': 'The Iron Claw', 'video': False, 'vote_average': 7.528, 'vote_count': 337}, {'adult': False, 'backdrop_path': '/wE5JGzujfvDPMIfFjJyrhXFjZLc.jpg', 'genre_ids': [16, 10751, 35], 'id': 10193, 'original_language': 'en', 'original_title': 'Toy Story 3', 'overview': "Woody, Buzz, and the rest of Andy's toys haven't been played with in years. With Andy about to go to college, the gang find themselves accidentally left at a nefarious day care center. The toys must band together to escape and return home to Andy.", 'popularity': 84.484, 'poster_path': '/AbbXspMOwdvwWZgVN0nabZq03Ec.jpg', 'release_date': '2010-06-16', 'title': 'Toy Story 3', 'video': False, 'vote_average': 7.795, 'vote_count': 14122}, {'adult': False, 'backdrop_path': '/syozWkk4Qi4s9RWefcfwCmBqRrt.jpg', 'genre_ids': [35], 'id': 1022690, 'original_language': 'en', 'original_title': 'Ricky Stanicky', 'overview': 'When three childhood best friends pull a prank gone wrong, they invent the imaginary Ricky Stanicky to get them out of trouble. Twenty years later, the trio still uses the nonexistent Ricky as a handy alibi for their immature behavior. But when their spouses and partners get suspicious and demand to finally meet the fabled Mr. Stanicky, the guilty trio decide to hire a washed-up actor and raunchy celebrity impersonator to bring him to life.', 'popularity': 105.067, 'poster_path': '/oJQdLfrpl4CQsHAKIxd3DJqYTVq.jpg', 'release_date': '2024-02-21', 'title': 'Ricky Stanicky', 'video': False, 'vote_average': 5.9, 'vote_count': 90}, {'adult': False, 'backdrop_path': '/deLWkOLZmBNkm8p16igfapQyqeq.jpg', 'genre_ids': [14, 12, 28], 'id': 763215, 'original_language': 'en', 'original_title': 'Damsel', 'overview': "A young woman's marriage to a charming prince turns into a fierce fight for survival when she's offered up as a sacrifice to a fire-breathing dragon.", 'popularity': 369.411, 'poster_path': '/sMp34cNKjIb18UBOCoAv4DpCxwY.jpg', 'release_date': '2024-03-08', 'title': 'Damsel', 'video': False, 'vote_average': 7.369, 'vote_count': 366}, {'adult': False, 'backdrop_path': '/dmiN2rakG9hZW04Xx7mHOoHTOyD.jpg', 'genre_ids': [35], 'id': 673593, 'original_language': 'en', 'original_title': 'Mean Girls', 'overview': 'New student Cady Heron is welcomed into the top of the social food chain by the elite group of popular girls called ‘The Plastics,’ ruled by the conniving queen bee Regina George and her minions Gretchen and Karen. However, when Cady makes the major misstep of falling for Regina’s ex-boyfriend Aaron Samuels, she finds herself prey in Regina’s crosshairs. As Cady sets to take down the group’s apex predator with the help of her outcast friends Janis and Damian, she must learn how to stay true to herself while navigating the most cutthroat jungle of all: high school.', 'popularity': 369.035, 'poster_path': '/fbbj3viSUDEGT1fFFMNpHP1iUjw.jpg', 'release_date': '2024-01-10', 'title': 'Mean Girls', 'video': False, 'vote_average': 6.23, 'vote_count': 265}, {'adult': False, 'backdrop_path': '/ctMserH8g2SeOAnCw5gFjdQF8mo.jpg', 'genre_ids': [35, 12], 'id': 346698, 'original_language': 'en', 'original_title': 'Barbie', 'overview': 'Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land. However, when they get a chance to go to the real world, they soon discover the joys and perils of living among humans.', 'popularity': 337.972, 'poster_path': '/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg', 'release_date': '2023-07-19', 'title': 'Barbie', 'video': False, 'vote_average': 7.101, 'vote_count': 7665}, {'adult': False, 'backdrop_path': '/6SLyu9ygASsrOqkCpjAwtyG9PWW.jpg', 'genre_ids': [10751, 878, 28, 35], 'id': 1094556, 'original_language': 'en', 'original_title': 'The Thundermans Return', 'overview': "Twins Phoebe and Max are enjoying their superhero lifestyle, but when one 'save' goes awry, the Thundermans are sent back to Hiddenville. While Hank and Barb enjoy their return, and Billy and Nora look forward to a normal high school life, Max and Phoebe are determined to regain their superhero status.", 'popularity': 332.441, 'poster_path': '/2J5eeroLDY0d45mVjpuGhcLZs3W.jpg', 'release_date': '2024-03-07', 'title': 'The Thundermans Return', 'video': False, 'vote_average': 7.85, 'vote_count': 20}, {'adult': False, 'backdrop_path': '/ilRyazdMJwN05exqhwK4tMKBYZs.jpg', 'genre_ids': [878, 18], 'id': 335984, 'original_language': 'en', 'original_title': 'Blade Runner 2049', 'overview': "Thirty years after the events of the first film, a new blade runner, LAPD Officer K, unearths a long-buried secret that has the potential to plunge what's left of society into chaos. K's discovery leads him on a quest to find Rick Deckard, a former LAPD blade runner who has been missing for 30 years.", 'popularity': 137.373, 'poster_path': '/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg', 'release_date': '2017-10-04', 'title': 'Blade Runner 2049', 'video': False, 'vote_average': 7.6, 'vote_count': 12886}, {'adult': False, 'backdrop_path': '/e9GbzPawXDFvLwSseCXpHkbCyAP.jpg', 'genre_ids': [18, 80], 'id': 627, 'original_language': 'en', 'original_title': 'Trainspotting', 'overview': "Heroin addict Mark Renton stumbles through bad ideas and sobriety attempts with his unreliable friends -- Sick Boy, Begbie, Spud and Tommy. He also has an underage girlfriend, Diane, along for the ride. After cleaning up and moving from Edinburgh to London, Mark finds he can't escape the life he left behind when Begbie shows up at his front door on the lam, and a scheming Sick Boy follows.", 'popularity': 42.699, 'poster_path': '/y0HmDV0bZDTtXWHqqYYbT9XoshB.jpg', 'release_date': '1996-02-23', 'title': 'Trainspotting', 'video': False, 'vote_average': 7.969, 'vote_count': 9264}]
    movie_ids = [movie['id'] for movie in result]  #get the tmdb ids for all the movie 
    session['recommended_movie_tmdbids'] = []    #make the session variable empty
    session['recommended_movie_tmdbids'].extend(movie_ids)  # add all the ids of the start page movies
    session.modified = True   # let the session know this variable is modifified
    addMoviesToCSV(movie_ids)    #add the movies to the csv if nessecary 
    return jsonify(json.dumps(result)) # return the result as a json



@app.route('/knn', methods=['POST'])
def knn_reccomendations():
    data = request.get_json()
    timeSpentData = data.get("timeSpentData")
    divIds = [entry['divId'] for entry in timeSpentData]
    result = recommendations_knn(divIds, session['recommended_movie_tmdbids'])
    session['recommended_movie_tmdbids'].extend(result)   # add them to the previosuly recommemnded movies
    session.modified = True #let the session know the this varaible is modified
    
    return jsonify(result)  # Return the result in form JSON


@app.route('/kmeans', methods=['POST'])
def kmeans_reccomendations():
    data = request.get_json()
    timeSpentData = data.get("timeSpentData")
    divIds = [entry['divId'] for entry in timeSpentData]
    result = recommendations_kmean(divIds, session['recommended_movie_tmdbids'])
    session['recommended_movie_tmdbids'].extend(result)   # add them to the previosuly recommemnded movies
    session.modified = True #let the session know the this varaible is modified
    return jsonify(result)  # Return the result in form JSON


@app.route('/graphBased', methods=['POST'])
def graphBased_reccomendations():
    data = request.get_json()
    timeSpentData = data.get("timeSpentData")
    if timeSpentData:
        result = collabritive_mult_input_recommendations(timeSpentData, session['recommended_movie_tmdbids'])
        session['recommended_movie_tmdbids'].extend(result)
        session.modified = True
    else:
        result = []
    
    print("returning now")
    return jsonify(result)


@app.route('/matrixFactorization', methods=['POST'])
def matrixFactorization_reccomendations():
    data = request.get_json()
    timeSpentData = data.get("timeSpentData")
    result = matrix_factorization_reccomendations(timeSpentData, session['recommended_movie_tmdbids'])
    session['recommended_movie_tmdbids'].extend(result)
    session.modified = True
    return jsonify(result)


@app.route('/neuralNetwork', methods=['POST'])
def neuralNetwork_reccomendations():
    data = request.get_json()
    timeSpentData = data.get("timeSpentData")
    result = neural_network_reccomendations(timeSpentData, session['recommended_movie_tmdbids'])
    session['recommended_movie_tmdbids'].extend(result)
    session.modified = True
    return jsonify(result)


@app.route('/hybrid', methods=['POST'])
def hybrid_reccomendations():
    data = request.get_json()
    timeSpentData = data.get("timeSpentData")
    divIds = [entry['divId'] for entry in timeSpentData]
    result1 = recommendations_knn(divIds, session['recommended_movie_tmdbids'])
    result2 = matrix_factorization_reccomendations(timeSpentData, session['recommended_movie_tmdbids'])
    combined_results = list(set(result1 + result2))
    random.shuffle(combined_results)
    result = combined_results[:24]
    session['recommended_movie_tmdbids'].extend(result)
    session.modified = True
    print("returning hybrid results")
    return jsonify(result)



@app.route('/time_data', methods=['POST'])  # Define a route for your API, which listens for POST requests at '/my_api'
def time_data_function():
    data = request.form.get('timeSpentData')
    time_spent_data = json.loads(data)
    data2 = request.form.get('recommendationMethod')
    method = json.loads(data2)
    data3 = request.form.get('clickData')
    click_data = json.loads(data3)

    if time_spent_data: 
        print("the method is: ")
        print(method)
        create_relationships(time_spent_data)     # for graph based 
        write_to_csv(time_spent_data)   # for matrix factorization
        record_time_data(time_spent_data, method)
        record_click_data(click_data, method)
        # for general storage 

    return make_response('', 200)
    
    
if __name__ == '__main__':  # Check if this script is the main program
    app.run(host='0.0.0.0', port=5001)
    #app.run()  #run the Flask application



