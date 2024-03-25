import csv
import os
import numpy as np
import pandas as pd
from config import MOVIE_DATA_PATH, RESULT_DATA_PATH, SESSION_DATA_PATH


def matrix_factorization_single_row(R, K=2, row_index=None, steps=5000, alpha=0.0002, beta=0.02):
    max_rating = np.max(R)   # Normalize the input matrix
    R_normalized = R / max_rating

    N, M = R_normalized.shape
    
    if row_index is None:
        row_index = N - 1
    
    P_row = np.random.rand(1, K)  # 1 row and K columns 
    Q = np.random.rand(K, M)   # Initialize item-feature matrix
    
    R_row = R_normalized[row_index, :]    # Select the specified row from the matrix

    for step in range(steps):   # Iterate over the specified number of steps for training
        for j in range(M):  # Loop over each item in the row
            if R_row[j] > 0:    # Check if the rating at position j is non-zero (known rating)
                eij = R_row[j] - np.dot(P_row, Q[:, j])[0]    # Calculate the error for this entry
                for k in range(K):
                    P_row[0, k] += alpha * (2 * eij * Q[k, j] - beta * P_row[0, k])  # Update user-feature matrix
                    Q[k, j] += alpha * (2 * eij * P_row[0, k] - beta * Q[k, j])  # Update item-feature matrix

        eR_row = np.dot(P_row, Q)
        error = np.sum((R_row - eR_row) ** 2)    # Calculate the error for this row
        if error < 0.001:  # If the error is small, break
            break

    nR_row_normalized = np.dot(P_row, Q)

    nR_row = nR_row_normalized * max_rating
    
    return nR_row



def read_csv_as_table(file_path):
    table = pd.read_csv(file_path, engine="python")  #read in the entire table 
    return table


def add_new_row(table, input_data):
    new_row_data = {}  # Create an empty dictionary to hold the data for the new row
    for point in input_data:  # Iterate through each point in the input_data
        divId = str(point['divId'])      #get the movie id 
        timeSpent = point['timeSpent']   #get the time spent watching that movie 
        new_row_data[divId] = timeSpent  # add data to the new_row_data dictionary
    new_row = pd.DataFrame(new_row_data, index=[0])  # Create a new row using the new_row_data dictionary
    table = pd.concat([table, new_row], axis=0, ignore_index=True)   # Concatenate the new row to the table
    return table


def matrix_factorization_reccomendations(input_data, previosuly_recommended_movie_ids):   
    table = read_csv_as_table(SESSION_DATA_PATH)  # read in the table from the csv file 
    table = add_new_row(table, input_data)  # add the new row to the table 
    M = table.values      #convert to NumPy array
    M = np.nan_to_num(M, nan=0)  # replace all nan with 0 
    result_row = matrix_factorization_single_row(M)[0]    #perform matrix factorization 
    combined_tuples = [(table.columns[i], result_row[i]) for i in range(len(table.columns))]   #combine the resulting row (time values) with the column names (movie ids) 
    sorted_tuples = sorted(combined_tuples, key=lambda x: x[1], reverse=True)   #sort them from greatest to smallest 
    ids = [tup[0] for tup in sorted_tuples]  #get just the movie ids from the sorted tuples 
    ids_integer = [int(x) for x in ids]
    result = [movie_id for movie_id in ids_integer if movie_id not in previosuly_recommended_movie_ids] # remove any previosuly recommended movies 
    return result[:24]  

def write_to_csv(data):
    div_ids = [entry['divId'] for entry in data]          #get all the div_ids
    time_spent = [entry['timeSpent'] for entry in data]    #get all the time spent values

    if (os.path.getsize(SESSION_DATA_PATH) == 0):     #if the file is empty     
        with open(SESSION_DATA_PATH, 'w', newline='') as file:
            writer = csv.writer(file)   
            writer.writerow(div_ids)     # write the first line as the div ids 
            writer.writerow(time_spent)  # write the second line as the time values 
    else:
        with open(SESSION_DATA_PATH, 'r') as file:  # open it in read mode
            csv_reader = csv.reader(file)  
            first_row = next(csv_reader)  #get the first row 

        first_row_int = list(map(int, first_row)) # convert them to integers 

        for div_id in div_ids:  # loop going through all the div ids    
            if div_id not in first_row_int: # if the div id is not in the first row 
                first_row_int.append(div_id)   # append it to the first row
        
        with open(SESSION_DATA_PATH, 'r+', newline='') as file:   #open in read and write mode
            csv_writer = csv.writer(file)   
            file.seek(0)  # Move to the beginning of the file
            csv_writer.writerow(first_row_int)   #rewrite the new first row 
            
        new_row = [''] * len(first_row_int)   #preset the length to the size of the first row 

        for div_id, time in zip(div_ids, time_spent):   #for each data point 
            column_index = first_row_int.index(div_id)  #get the index of div id 
            new_row[column_index] = time    #set the time at that index
    
        with open(SESSION_DATA_PATH, 'rb') as file:  # Open the CSV file in binary mode for reading
            file.seek(-1, 2)  # Move the cursor to the second to last byte from the end of the file
            last_char = file.read(1)  # Read the last byte (character) from the file
            if last_char != b'\n':  # Check if the last character is not a newline
                append_newline = True # If the last character is not a newline, set append_newline to True
            else:
                append_newline = False # Otherwise, set append_newline to False

        # Append the new row
        with open(SESSION_DATA_PATH, 'a', newline='') as file:   # open the file in append mode
            if append_newline:   # Check if append_newline is True
                file.write('\n')  # If so, write a newline character to the file
            csv_writer = csv.writer(file)
            csv_writer.writerow(new_row)



#input_data = [{'divId': 666277, 'timeSpent': 310},{'divId': 78769, 'timeSpent': 7483}, {'divId': 66278, 'timeSpent': 310}]

#write_to_csv(input_data)


# input_data = [{'divId': 666277, 'timeSpent': 310},{'divId': 78769, 'timeSpent': 7483}, {'divId': 66278, 'timeSpent': 310}]
# result = matrix_factorization_reccomendations(input_data, [78769])
# print(result)
