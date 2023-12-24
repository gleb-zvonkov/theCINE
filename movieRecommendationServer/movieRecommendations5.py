#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from ast import literal_eval
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[2]:


md = pd.read_csv('45000_movies/movies_metadata_final.csv')  #import the datasets


# In[3]:


md['cast'] = md['cast'].apply(literal_eval)   # create a list 
md['cast'] = md['cast'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])   #lowercase and remove whitespace
md['genres'] = md['genres'].apply(literal_eval)   # create a list
md['director'] = md['director'].astype('str').apply(lambda x: str.lower(x.replace(" ", ""))) #lowercase and remove whitespace
md['director'] = md['director'].apply(lambda x: [x,x])  #repeat it 3 times


# In[4]:


md['release_date'] = pd.to_datetime(md['release_date'], errors='coerce') #convert it to data
md['decade'] = md['release_date'].apply(lambda x: [str((x.year // 10) * 10)] if not pd.isnull(x) else [''])  # get the decade


# In[5]:


def weighted_rating(x, C, m):   
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)


# In[6]:


md['vote_count'] = md[md['vote_count'].notnull()]['vote_count'].astype('int')  # remove null value and convert vote count to integer
md['vote_average'] = md[md['vote_average'].notnull()]['vote_average'].astype('float')  # remove null values and convert vote average to integer
C = md['vote_average'].mean()  # mean of all the vote average
m = md['vote_count'].quantile(0.40)  # get the quantile  
md = md[md['vote_count'] >= m] # remove all movies not in the quantile
md = md.reset_index(drop=True)   # reset the index since you dropped a bunch of columns
md['wr'] = md.apply(weighted_rating, args=(C, m), axis=1)     #caclculate the weighted rating


# In[7]:


md['soup'] =  md['cast'] + md['genres']+ md['director']+ md['decade']   # combine them all into a soup  
md['soup'] = md['soup'].apply(lambda x: ' '.join(x))   # remove white space 
count = CountVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0.0, stop_words='english')   # intialize count object
count_matrix = count.fit_transform(md['soup'])   # essentially creates an array for each movie, where 1 indicates it has that word 
cosine_sim = cosine_similarity(count_matrix, count_matrix)  # big step  essentially computes cosine similiraty for each movie with every other movie using the array from above


# In[8]:


indices = pd.Series(md.index, index=md['title'])
indicesTmdbId = pd.Series(md.index, index=md['id'])  #for each movie tmdb id you can look up its index


# In[9]:


def mult_input_recommendations(liked_movie_ids, previosuly_recommended_movies_ids):
    
    scores_dict = dict() #key is the movie index, value is the sum of the cosine simalrity 
    previosuly_recommended_movies_indices = [indicesTmdbId[id] for id in previosuly_recommended_movies_ids if id in indicesTmdbId]  #get the indices of the movies 

    for id in liked_movie_ids:    # For each liked movie
        if id in indicesTmdbId:   # if the movie id exists  
            idx = indicesTmdbId[id]   # get its index in the md dataframe 
            movie_id_and_similarity_score = list(enumerate(cosine_sim[idx]))  # movie_id_and_similarity_score =(movie index, simalirty score)
            movie_id_and_similarity_score = list(filter(lambda x: x[0] not in previosuly_recommended_movies_indices, movie_id_and_similarity_score ) ) # remove all those previosuly recommended
            
            sorted_similar_movies = sorted(movie_id_and_similarity_score, key=lambda x: x[1], reverse=True)   # sort them according to the similarity score
            top_similar_movies = sorted_similar_movies[1:31]   # get the top 100 movies with the highest similarity score  
            
            for idy in top_similar_movies:   # for top similar movies
                if idy[0] not in scores_dict:   # if the movie index for the movie is not in the dictionary 
                    scores_dict[idy[0]] = idy[1]  # set the movie index as the key and the value as the similarity score 
                else: # If the movie index for the movie is in the dictionary 
                    scores_dict[idy[0]] = scores_dict[idy[0]] + idy[1] # set the value as sum of the similarity scores 

    for key, value in scores_dict.items():
        scores_dict[key] = scores_dict[key] + (md.loc[key, 'popularity'])/100 + (md.loc[key, 'wr'])/10    # similarity score + popularity score + weighted rating

    sorted_movie_indices = sorted(scores_dict, key=scores_dict.get, reverse=True) #sort the movie indices according to there similarity score
    
    movies = md.iloc[sorted_movie_indices]

    return movies['id'].tolist()

