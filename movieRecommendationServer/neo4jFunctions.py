from neo4j import GraphDatabase
from collections import Counter

uri = "bolt://localhost:7687" 
username = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(username, password))

# Creates a time relationship between two movies 
def create_has_duration_relationship(movie1_id, movie2_id, duration):
    query = (
        "MATCH (movie1:Movie {id: $movie1_id})"
        "MATCH (movie2:Movie {id: $movie2_id})"
        "MERGE (movie1)-[rel:HAS_DURATION]->(movie2)"
        "SET rel.duration = COALESCE(rel.duration, 0) + $duration"
    )

    with driver.session() as session:
        session.run(query, movie1_id=movie1_id, movie2_id=movie2_id, duration=duration)

def create_relationships(time_spent_data): # Iterate through the data and create relationships
    num_movies = len(time_spent_data)
    for j in range(num_movies): 
        for i in range(num_movies):
            if j != i:
                movie1_id = time_spent_data[j]['divId']
                movie2_id = time_spent_data[(i) ]['divId']
                duration = time_spent_data[(i) ]['timeSpent']
                create_has_duration_relationship(movie1_id, movie2_id, duration)
    print("created relationships")


def get_relationships_descending(movie_id):
    query = (
        "MATCH (:Movie {id: $movieId})-[r:HAS_DURATION]->(otherMovie) "
        "WITH otherMovie, r.duration as duration "
        "ORDER BY duration DESC "
        "RETURN otherMovie.id, duration"
    )

    with driver.session() as session:
        result = session.run(query, movieId=movie_id)
        movie_data = [(record['otherMovie.id'], record['duration']) for record in result]

    return movie_data



def collabritive_mult_input_recommendations(time_spent_data, previosuly_recommended_movie_ids):
    ranked_data = sorted(time_spent_data, key=lambda x: x['timeSpent'], reverse=True)   #rank the time_spent_data according to timespent 
    largest_time = ranked_data[0]['timeSpent']  #get the largest time
    recommended_movies = {}  # a dictionary for the recommended movies, where the id is the key and the timespent is the value 
    
    for movie in time_spent_data:   #for every single movie 
        weight = movie['timeSpent'] / largest_time   #divide the timeSpent by the largest time, so the largest weight is 1 
        outgoing_relationships = get_relationships_descending(movie['divId'])  #get outgoing relationships, ie the trailers other people watched if they watched this trailer

        for related_movie in outgoing_relationships:  #for each of the movies 
            div_id, duration = related_movie  # Unpack the tuple, it contains the movie id and the cummalitive duration people watch it for 
            if div_id not in recommended_movies:    # if its not yet in the dictionary add it 
                recommended_movies[div_id] = {'timeSpent': duration * weight}
            else:   # if it is in the dictionary, accumulate the duration  
                recommended_movies[div_id]['timeSpent'] += duration * weight

    ranked_recommendations = sorted(recommended_movies.items(), key=lambda x: x[1]['timeSpent'], reverse=True)  # rank all the recommended movies according to duration
    ids = [div_id for div_id, _ in ranked_recommendations]  # get just the ids 
    filtered_ids = [movie_id for movie_id in ids if movie_id not in previosuly_recommended_movie_ids] # remove any ids that already exist in the previosuly_recommended_movie_ids

    return filtered_ids
    
    
time_spent_data = [{'divId': 523607, 'timeSpent': 7645}, {'divId': 569094, 'timeSpent': 6059}, {'divId': 466420, 'timeSpent': 7747}, {'divId': 926393, 'timeSpent': 9397}, {'divId': 489, 'timeSpent': 186}, {'divId': 157336, 'timeSpent': 2513}, {'divId': 414906, 'timeSpent': 9417}, {'divId': 12445, 'timeSpent': 7756}, {'divId': 695721, 'timeSpent': 0}]
previosuly_recommended_movie_ids = [523607]
result = collabritive_mult_input_recommendations(time_spent_data, previosuly_recommended_movie_ids )


# we need to write a flask server recommendation function 



driver.close() # Close the driver when done