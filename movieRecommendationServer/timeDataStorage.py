

# method 
# input_data = [{'divId': 666277, 'timeSpent': 310},{'divId': 78769, 'timeSpent': 7483}, {'divId': 66278, 'timeSpent': 310}]

import pandas as pd
from config import MOVIE_DATA_PATH, RESULT_DATA_PATH, SESSION_DATA_PATH

def record_time_data(input_data, method):
    total_time_spent = int(sum(entry['timeSpent'] for entry in input_data) / 1000)
    table = pd.read_csv(RESULT_DATA_PATH, index_col='type')  
    
    if method in table.columns:
        # Method already exists in columns
        table.loc['watchtime', method] += total_time_spent
    else:
        # Create a new column with the method name
        table[method] = 0
        table.loc['watchtime', method] = total_time_spent
    
    table.to_csv(RESULT_DATA_PATH)  # No need to specify index=False, it's by default


def record_click_data(click_data, method):
    table = pd.read_csv(RESULT_DATA_PATH, index_col='type')
    
    for click_type, count in click_data.items():
        if click_type in table.index:
            table.loc[click_type, method] += count
        else:
            print("erorr wrong click type")

    table.to_csv(RESULT_DATA_PATH)


def print_time_data(): 
    table = pd.read_csv(RESULT_DATA_PATH)
    print(table)


# Example usage:
# input_data = [{'divId': 666277, 'timeSpent': 310}, {'divId': 78769, 'timeSpent': 7483}, {'divId': 66278, 'timeSpent': 310}]

# click_data = {'screenClick': 1, 'youtubeClick': 0, 'googleClick': 2, 'streamingClick': 0}

# method = "matrixFactorization"
# record_time_data(input_data, method)
# record_click_data(click_data, method)

# print_time_data()



