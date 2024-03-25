#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from ast import literal_eval
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import time
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from config import MOVIE_DATA_PATH

# In[2]:


md = pd.read_csv(MOVIE_DATA_PATH)  #import the datasets


# In[3]:


md.drop_duplicates(subset=['id'], keep='first', inplace=True)


# In[4]:


md['cast'] = md['cast'].apply(literal_eval)   # create a list 
md['cast'] = md['cast'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])   #lowercase and remove whitespace
md['genres'] = md['genres'].apply(literal_eval)   # create a list
md['director'] = md['director'].astype('str').apply(lambda x: str.lower(x.replace(" ", ""))) #lowercase and remove whitespace
md['director'] = md['director'].apply(lambda x: [x,x])  #repeat it 3 times


# In[5]:


md['release_date'] = pd.to_datetime(md['release_date'], errors='coerce') #convert it to data
md['decade'] = md['release_date'].apply(lambda x: [str((x.year // 10) * 10)] if not pd.isnull(x) else [''])  # get the decade


# In[6]:


def weighted_rating(x, C, m):   
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)


# In[7]:


md['vote_count'] = md[md['vote_count'].notnull()]['vote_count'].astype('int')  # remove null value and convert vote count to integer
md['vote_average'] = md[md['vote_average'].notnull()]['vote_average'].astype('float')  # remove null values and convert vote average to integer
C = md['vote_average'].mean()  # mean of all the vote average
m = md['vote_count'].quantile(0.40)  # get the quantile  
md = md[md['vote_count'] >= m] # remove all movies not in the quantile
md = md.reset_index(drop=True)   # reset the index since you dropped a bunch of columns
md['wr'] = md.apply(weighted_rating, args=(C, m), axis=1)     #caclculate the weighted rating


# In[8]:


md['soup'] =  md['cast'] + md['genres']+ md['director']+ md['decade']   # combine them all into a soup  
md['soup'] = md['soup'].apply(lambda x: ' '.join(x))   # remove white space 
count = CountVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0.0, stop_words='english')   # intialize count object
count_matrix = count.fit_transform(md['soup'].values).astype(np.float32)   # creates a sparse matrix for each movie
knn_model = NearestNeighbors(n_neighbors=20, metric='cosine', algorithm='brute')
knn_model.fit(count_matrix)
kmeans = KMeans(n_clusters=50, random_state=42)
cluster_labels = kmeans.fit_predict(count_matrix)
md['cluster_label'] = cluster_labels


# In[9]:


def print_titles(indices):   
    for i, index in enumerate(indices):
        title = md['title'].iloc[index]  
        print("{}".format(title))


# In[10]:


def reccomendations(index):
    movie_vector = count_matrix[index]
    distances, indices = knn_model.kneighbors(movie_vector.reshape(1, -1))
    return indices


# In[11]:


def multi_recommendations(movie_indices):
    movie_vector = count_matrix[movie_indices]    
    feature_means = movie_vector.mean(axis=0)
    query_vector = np.asarray(feature_means)
    distances, indices = knn_model.kneighbors(query_vector)
    indices = np.setdiff1d(indices, np.asarray(movie_indices))
    return indices


# In[12]:


def calculate_movie_rating(similarity, popularity, weighted_rating):
    weight_popularity = 0.2
    weight_wr = 0.8
    rating = (popularity * weight_popularity) + (weighted_rating * weight_wr) + (similarity)
    return rating 


# In[13]:


def multi_recommendations_other(movie_indices):
    movie_vector = count_matrix[movie_indices]    
    feature_means = movie_vector.mean(axis=0)
    query_vector = np.asarray(feature_means)
    distances, indices = knn_model.kneighbors(query_vector)
    indices = np.setdiff1d(indices, np.asarray(movie_indices))
    sorted_indices = sorted(indices, key=lambda idx: calculate_movie_rating( distances[0][np.where(indices == idx)], md['popularity'].iloc[idx], md['wr'].iloc[idx]), reverse=True) 
    return sorted_indices


# In[14]:


indicesTmdbId = pd.Series(md.index, index=md['id'])  #for each movie tmdb id you can look up its


# In[21]:


def recommendations_knn(liked_movie_ids, previosuly_recommended_movie_ids):
    
    liked_movie_indicies = [indicesTmdbId[id] for id in liked_movie_ids if id in indicesTmdbId]  #get the indices for the liked movies
    previosuly_recommended_movies_indices = [indicesTmdbId[id] for id in previosuly_recommended_movie_ids if id in indicesTmdbId]  #get the indices for the prviously recommended movies

    if not liked_movie_indicies:  # Check if liked_movie_indicies is empty
        return []    # if it is just return an empty list

    movie_vector = count_matrix[liked_movie_indicies]    
    feature_means = movie_vector.mean(axis=0)
    query_vector = np.asarray(feature_means)
    distances, indices = knn_model.kneighbors(query_vector) #get the recommend movies from the liked movies
   
    indices = np.setdiff1d(indices, np.asarray(previosuly_recommended_movies_indices))

    sorted_indices = sorted(indices, key=lambda idx: calculate_movie_rating( distances[0][np.where(indices == idx)], md['popularity'].iloc[idx], md['wr'].iloc[idx]), reverse=True) 

    movies = md.iloc[sorted_indices]
    
    return movies['id'].tolist()[:24]


# In[22]:


def recommendations_kmean(liked_movie_ids, previosuly_recommended_movie_ids):

    liked_movie_indicies = [indicesTmdbId[id] for id in liked_movie_ids if id in indicesTmdbId]  #get the indices for the liked movies
    previosuly_recommended_movies_indices = [indicesTmdbId[id] for id in previosuly_recommended_movie_ids if id in indicesTmdbId]  #get the indices for the prviously recommended movies

    
    movie_vector = count_matrix[liked_movie_indicies]    
    feature_means = movie_vector.mean(axis=0)
    query_vector = np.asarray(feature_means)
    new_movie_cluster_label = kmeans.predict(query_vector.reshape(1, -1))[0]
    indices = md[md['cluster_label'].isin([new_movie_cluster_label])].index.tolist() 
    
    indices = np.setdiff1d(indices, np.asarray(previosuly_recommended_movies_indices))

    sorted_indices = sorted(indices, key=lambda idx: calculate_movie_rating( 1, md['popularity'].iloc[idx], md['wr'].iloc[idx]), reverse=True) 

    movies = md.iloc[sorted_indices]
    
    return movies['id'].tolist()[:24]


# In[23]:


def print_titles_from_tmdbid(tmdb_ids): 
    indices = [indicesTmdbId[id] for id in tmdb_ids if id in indicesTmdbId]
    for index in indices:
        title = md['title'].iloc[index]  
        print("{}".format(title))


# In[20]:


def print_movies_info(movie_indices):
    movie_indices = [indicesTmdbId[id] for id in movie_indices if id in indicesTmdbId] 
    for index in movie_indices:
        movie_info = md.iloc[index]
        title = movie_info['title']
        cast = ', '.join(movie_info['cast'])
        genres = ', '.join(movie_info['genres'])
        director = ', '.join(movie_info['director'])
        release_date = movie_info['decade']
        #vote_average = movie_info['vote_average']
        #vote_count = movie_info['vote_count']
        #popularity = movie_info['popularity']
        weighted_rating = int(movie_info['wr']) 
        
        print("{}, {}, {}, {}, {}, {}".format(title, cast, genres, director, release_date, weighted_rating))

