import pandas as pd
import numpy as np
from pandas.errors import ParserError

def preprocessing(url):
    # Read the CSV file from the given URL into a DataFrame
    df = pd.read_csv(url, header=None, names=['Cust_Id', 'Rating'], usecols=[0, 1])

    # Convert the 'Rating' column to float data type
    df.Rating = df.Rating.astype(float)

    # Create a new DataFrame with the indices of missing values in the 'Rating' column
    df_nan = df.Rating.isnull()[df.Rating.isnull() == True].reset_index()

    # Initialize variables for storing movie IDs
    movie_np = []
    movie_id = 1

    # Iterate over the indices of missing values to assign movie IDs
    for i, j in zip(df_nan['index'][1:], df_nan['index'][:-1]):
        # Create a numpy array with movie_id repeated a certain number of times
        temp = np.full((1, i - j - 1), movie_id)
        movie_np = np.append(movie_np, temp)
        movie_id += 1

    # Handle the last block of missing values separately
    last_record = np.full((1, len(df) - df_nan.iloc[-1, 0] - 1), movie_id)
    movie_np = np.append(movie_np, last_record)

    # Remove rows with missing values in the 'Rating' column
    df = df[pd.notnull(df['Rating'])]

    # Add the 'Movie_Id' column to the DataFrame
    df['Movie_Id'] = movie_np.astype(int)
    df['Cust_Id'] = df['Cust_Id'].astype(int)

    # Set the 'Movie_Id' column as the index of the DataFrame
    df.set_index('Movie_Id', inplace=True)

    # Prepare for reading movie titles CSV file
    data = []
    columns = ['Movie_Id', 'Year', 'Movie_Name']

    # Open the movie titles CSV file
    with open('data/movie_titles.csv', 'r', encoding="ISO-8859-1") as file:
        # Iterate over each line in the file
        for line in file:
            try:
                # Split the line by commas to extract the fields
                fields = line.strip().split(',', 2)
                data.append(fields)
            except ParserError:
                # Handle the row with an incorrect field count
                # You can choose to skip, modify, or save it separately for further investigation
                continue

    # Create a DataFrame from the extracted movie title information
    df_title = pd.DataFrame(data, columns=columns)
    df_title['Movie_Id'] = df_title['Movie_Id'].astype(int)

    # Set the 'Movie_Id' column as the index of the DataFrame
    df_title.set_index('Movie_Id', inplace=True)

    # Join the original DataFrame with the movie titles DataFrame based on their common 'Movie_Id' index
    return df.join(df_title)
