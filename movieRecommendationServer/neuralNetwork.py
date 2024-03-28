#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from config import MOVIE_DATA_PATH, RESULT_DATA_PATH, SESSION_DATA_PATH

# In[2]:


data = pd.read_csv(SESSION_DATA_PATH, engine='python')
matrix = data.to_numpy()


# In[3]:


def read_csv_as_table(file_path):
    table = pd.read_csv(file_path, engine='python')  #read in the entire table 
    return table


# In[4]:


def add_new_row(table, input_data):
    new_row_data = {}  # Create an empty dictionary to hold the data for the new row
    for point in input_data:  # Iterate through each point in the input_data
        divId = str(point['divId'])      #get the movie id 
        timeSpent = point['timeSpent']   #get the time spent watching that movie 
        new_row_data[divId] = timeSpent  # add data to the new_row_data dictionary
    new_row = pd.DataFrame(new_row_data, index=[0])  # Create a new row using the new_row_data dictionary
    table = pd.concat([table, new_row], axis=0, ignore_index=True)   # Concatenate the new row to the table
    return table


# In[5]:


def create_model(input_shape):
    model = models.Sequential([ # Sequential model is a linear stack of layers, where you can easily add layers sequentially
        layers.Dense(64, activation='relu', input_shape=input_shape), # adds a fully connected (dense) layer to the model, has 64 units (neurons) and uses the ReLU (Rectified Linear Unit) activation function
        layers.Dense(64, activation='relu'),  #adds another fully connected (dense) layer to the model, automatically infer the input shape from the preceding layer
        layers.Dense(1) #the output layer to the model. It has 1 unit, representing the output value. no activation function, so outputs raw numeric values
    ])
    model.compile(optimizer='adam', loss='mse')  #compile the model using adam optimizer and loss function mean squared error
    return model  


# In[6]:


X_train = np.argwhere(~np.isnan(matrix))  #indices of non-NaN elements in the matrix
print(X_train)
y_train = matrix[~np.isnan(matrix)].reshape(-1, 1) #column vector containing the non-NaN values from the original matrix
print(y_train)

model = create_model(input_shape=(2,))
model.fit(X_train, y_train, epochs=50, batch_size=16, verbose=0)


# In[15]:


def neural_network_single_row(matrix):
    missing_indices = np.argwhere(np.isnan(matrix[-1]))
    missing_indices_with_row = np.column_stack((np.full_like(missing_indices[:, 0], matrix.shape[0]-1), missing_indices[:, 0]))
    predicted_values = model.predict(missing_indices_with_row).reshape(-1)
    predicted_matrix = matrix.copy()
    for idx, val in zip(missing_indices_with_row, predicted_values):  # iterate over the missing indices
        predicted_matrix[tuple(idx)] = val   #set the value
    return predicted_matrix[-1]


# In[19]:


def neural_network_reccomendations(input_data, previosuly_recommended_movie_ids): 
    table = data  # read in the table from the csv file 
    table = add_new_row(table, input_data)  # add the new row to the table 
    M = table.values      #convert to NumPy array
    #M = np.nan_to_num(M, nan=0)  # replace all nan with 0 
    result_row = neural_network_single_row(M)    #perform matrix factorization 
    combined_tuples = [(table.columns[i], result_row[i]) for i in range(len(table.columns))]   #combine the resulting row (time values) with the column names (movie ids) 
    sorted_tuples = sorted(combined_tuples, key=lambda x: x[1], reverse=True)   #sort them from greatest to smallest 
    ids = [tup[0] for tup in sorted_tuples]  #get just the movie ids from the sorted tuples 
    ids_integer = [int(x) for x in ids]
    result = [movie_id for movie_id in ids_integer if movie_id not in previosuly_recommended_movie_ids] # remove any previosuly recommended movies 
    return result[:24] 


# In[20]:


#neural_netwrok_single_row(matrix)
# input_data = [{'divId': 666277, 'timeSpent': 310},{'divId': 78769, 'timeSpent': 7483}, {'divId': 66278, 'timeSpent': 310}]
# result = neural_network_reccomendations(input_data, [78769])
# print(len(result))
#print(result)


# In[ ]:




