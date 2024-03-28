

# method 
# input_data = [{'divId': 666277, 'timeSpent': 310},{'divId': 78769, 'timeSpent': 7483}, {'divId': 66278, 'timeSpent': 310}]

import pandas as pd
from tmdbFetchFunctions import fetchMovieById
from config import MOVIE_DATA_PATH, RESULT_DATA_PATH, SESSION_DATA_PATH, METHOD_DATA_PATH

def record_method_data(input_data, click_data, method):
    table = pd.read_csv(METHOD_DATA_PATH, index_col=None)
    total_time_spent = int(sum(entry['timeSpent'] for entry in input_data) / 1000)
    total_clicks = sum(click_data.values())

    empty_row_index = table.index[table[f'{method}Time'].isna()].min() 

    if pd.notna(empty_row_index):
        table.loc[empty_row_index, f'{method}Time'] = total_time_spent
        table.loc[empty_row_index, f'{method}Clicks'] = total_clicks
    else:
        table.loc['', f'{method}Time'] = total_time_spent
        table.loc['', f'{method}Clicks'] = total_clicks

    table.to_csv(METHOD_DATA_PATH, index=False)



def record_time_data(input_data, method):

    table = pd.read_csv(RESULT_DATA_PATH, index_col='type')
    total_time_spent = int(sum(entry['timeSpent'] for entry in input_data) / 1000)  
    
    if method in table.columns:
        # Method already exists in columns
        table.loc['watchtime', method] += total_time_spent
    else:
        # Create a new column with the method name
        table[method] = 0
        table.loc['watchtime', method] = total_time_spent

    table.loc['sessions', method] += 1
    
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


def calculate_interaction_per_session():
    table = pd.read_csv(RESULT_DATA_PATH, index_col='type')
    for method in table.columns:
        table.loc['averageWatchtime', method] = int(table.loc['watchtime', method]/table.loc['sessions', method])
        table.loc['totalClicks', method] = int(table.loc['screenClick', method] + table.loc['youtubeClick', method] + table.loc['googleClick', method] + table.loc['streamingClick', method])
        table.loc['averageClicks', method] = int(table.loc['totalClicks', method] / table.loc['sessions', method])
    table.to_csv(RESULT_DATA_PATH)


def calculate_most_watch_trailer():
    table = pd.read_csv(SESSION_DATA_PATH, index_col=0) #first row is the index 
    column_sums = table.sum(axis=0)
    ranked_columns = column_sums.sort_values(ascending=False)

    top_hundred = ranked_columns[:100]

    for index, sum_value in top_hundred.items():
        movie_info = fetchMovieById(index)
        original_title = movie_info.get('original_title', 'Unknown Title')  # Get the original title, default to 'Unknown Title' if not found
        print(f"{original_title}, {sum_value/(1000 * 3600)}")





# Example usage:
input_data = [{'divId': 666277, 'timeSpent': 310}, {'divId': 78769, 'timeSpent': 7483}, {'divId': 66278, 'timeSpent': 310}]

click_data = {'screenClick': 1, 'youtubeClick': 1, 'googleClick': 2, 'streamingClick': 0}

method = "knn"
record_time_data(input_data, method)
# record_click_data(click_data, method)

# print_time_data()

#record_method_data(input_data, click_data, method)



#calculate_most_watch_trailer() 
#calculate_interaction_per_session()
print_time_data()