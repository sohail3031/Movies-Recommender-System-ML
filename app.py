import json

import streamlit as st
import pandas as pd
import pickle
import requests

movies_dict = pickle.load(open("movies.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))


def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&"
                            f"language=en-US").json()['poster_path']

    return f"https://image.tmdb.org/t/p/w500{response}"


def recommend_movies(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1: 6]
    recommended_movies_list = []
    recommended_movies_posters_list = []

    for i in movies_list:
        recommended_movies_list.append(movies.iloc[i[0]].title)
        recommended_movies_posters_list.append(fetch_poster(movies.iloc[i[0]].movie_id))

    return recommended_movies_list, recommended_movies_posters_list


st.title("Movie Recommender System")

selected_movie_name = st.selectbox("Search Movies Here", movies["title"].values)

if st.button("Recommend"):
    movies_name, movies_posters = recommend_movies(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(movies_name[0])
        st.image(movies_posters[0])
    with col2:
        st.text(movies_name[1])
        st.image(movies_posters[1])
    with col3:
        st.text(movies_name[2])
        st.image(movies_posters[2])
    with col4:
        st.text(movies_name[3])
        st.image(movies_posters[3])
    with col5:
        st.text(movies_name[4])
        st.image(movies_posters[4])
