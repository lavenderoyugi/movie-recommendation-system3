import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import requests
import streamlit as st
import os

# st.set_page_config(layout='wide')

url = 'https://image.tmdb.org/t/p/original'


# Load the dataset
file_path = 'movies_step2 - movies_step2.csv'  # Ensure the CSV is in the same directory
movies_df = pd.read_csv(file_path)

# Select relevant features
features = movies_df.drop(columns=['tconst', 'titleType', 'startYear', 'runtimeMinutes', 'averageRating', 'numVotes', 'title', 'language'])

# Compute cosine similarity matrix
similarity_matrix = cosine_similarity(features, features)

# Store movie titles for easy lookup
movie_titles = movies_df['title'].tolist()

def get_recommendations(title, similarity_matrix, movie_titles, top_n=10):
    # Find the index of the movie
    try:
        idx = movie_titles.index(title)
    except ValueError:
        return ["Movie not found in the dataset."]
    
    # Get similarity scores for all movies
    sim_scores = list(enumerate(similarity_matrix[idx]))
    
    # Sort the movies based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the indices of the top_n most similar movies
    top_indices = [i[0] for i in sim_scores[1:top_n+1]]
    
    # Return the titles of the top_n most similar movies
    return [movie_titles[i] for i in top_indices]



# Streamlit application
st.title("Movie Recommendation System")

movie_title = st.text_input("Enter a movie title:")
if movie_title:
    st.write(movie_title)
    # recommendations = get_recommendations(movie_title, similarity_matrix, movie_titles)
    # if "Movie not found in the dataset." in recommendations:
    #     st.write("Movie not found in the dataset.")
    # else:
    #     st.write("Recommended Movies:")
    #     for movie in recommendations:
    #         st.write(movie)
    #         poster_url = fetch_movie_poster(movie)
    #         if poster_url:
    #            st.image(poster_url, width=150)
