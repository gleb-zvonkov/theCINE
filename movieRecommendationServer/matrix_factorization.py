import csv
import os
import numpy as np

def write_to_csv(data, csv_file):
    div_ids = [entry['divId'] for entry in data]          #get all the div_ids
    time_spent = [entry['timeSpent'] for entry in data]    #get all the time spent values

    if (os.path.getsize(csv_file) == 0):     #if the file is empty     
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)   
            writer.writerow(div_ids)     # write the first line as the div ids 
            writer.writerow(time_spent)  # write the second line as the time values 
    else:
        with open(csv_file, 'r') as file:  # open it in read mode
            csv_reader = csv.reader(file)  
            first_row = next(csv_reader)  #get the first row 

        first_row_int = list(map(int, first_row)) # convert them to integers 

        for div_id in div_ids:  # loop going through all the div ids    
            if div_id not in first_row_int: # if the div id is not in the first row 
                first_row_int.append(div_id)   # append it to the first row
        
        with open(csv_file, 'r+', newline='') as file:   #open in read and write mode
            csv_writer = csv.writer(file)   
            file.seek(0)  # Move to the beginning of the file
            csv_writer.writerow(first_row_int)   #rewrite the new first row 
            
        new_row = [''] * len(first_row_int)   #preset the length to the size of the first row 

        for div_id, time in zip(div_ids, time_spent):   #for each data point 
            column_index = first_row_int.index(div_id)  #get the index of div id 
            new_row[column_index] = time    #set the time at that index
    
        with open(csv_file, 'a', newline='') as file:   # open the file in append mode
            file.write('\n')
            csv_writer = csv.writer(file)
            csv_writer.writerow(new_row)  # write the new row at the end 

def read_csv(csv_file):
    # Read CSV file into a list of lists
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)

    first_row = data[0]  # Separate the first row 

    # Replace empty cells with 0
    for row in data:
        for i, cell in enumerate(row):
            if cell == '':
                row[i] = '0'

    # Fill inconsistencies with 0
    num_columns_first_row = len(first_row)
    for row in data:
        while len(row) < num_columns_first_row:
            row.append('0')  # Append '0' until the row has the same number of columns as the first row

    # Convert data to a NumPy array, excluding the first row
    try:
        data_array = np.array(data[1:], dtype=np.float32)
    except ValueError as e:
        print("Error converting data to NumPy array:", e)
        return None

    #print(data_array)

    return first_row, data_array


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


def matrix_factorization_reccomendations(input_data, previosuly_recommended_movie_ids):
    csv_file = 'time_session_data.csv'
    #write_to_csv(input_data, csv_file)
    first_row, M = read_csv(csv_file)
    result_row = matrix_factorization_single_row(M)[0]
    combined_tuples = [(first_row[i], result_row[i]) for i in range(len(first_row))]
    sorted_tuples = sorted(combined_tuples, key=lambda x: x[1], reverse=True)
    ids = [tup[0] for tup in sorted_tuples]
    filtered_ids = [movie_id for movie_id in ids if movie_id not in previosuly_recommended_movie_ids]
    return filtered_ids


input_data = [{'divId': 787699, 'timeSpent': 7483}, {'divId': 666277, 'timeSpent': 310}, {'divId': 76826, 'timeSpent': 926}, {'divId': 558915, 'timeSpent': 1297}, {'divId': 324786, 'timeSpent': 6702}, {'divId': 1056360, 'timeSpent': 1594}, {'divId': 11645, 'timeSpent': 13322}, {'divId': 1072790, 'timeSpent': 6835}, {'divId': 107279, 'timeSpent': 6832}]

x = []

#result = matrix_factorization_reccomendations(input_data, x)
#print(result)

#read_csv('time_session_data.csv')

#write_to_csv(input_data, 'time_session_data.csv')
