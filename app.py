import streamlit as st
import pickle
import pandas as pd
import requests
import time

def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=e9639ade75d9242a24298740293640f7&language=en-US'
        response = requests.get(url, timeout=5)  
        
        if response.status_code == 200:
            data = response.json()
            if 'poster_path' in data and data['poster_path']:
                return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
            return "https://via.placeholder.com/500x750?text=No+Image"  
        
        elif response.status_code == 401:
            st.error("Invalid API Key! Please check your TMDb API key.")
        elif response.status_code == 404:
            st.error(f"Movie ID {movie_id} not found on TMDb.")
        else:
            st.warning(f"Error {response.status_code}: Unable to fetch movie poster.")
    
    except requests.exceptions.ConnectionError:
        st.error("Connection error! Check your internet or API access.")
        time.sleep(2)  
    except requests.exceptions.Timeout:
        st.error("Request timed out! TMDb API might be slow.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

    return "https://via.placeholder.com/500x750?text=No+Image"  

def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []

        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id  
            
            recommended_movies.append(movies.iloc[i[0]].title)  
            recommended_movies_posters.append(fetch_poster(movie_id))  

        return recommended_movies, recommended_movies_posters
    
    except IndexError:
        st.error("Movie not found in the dataset! Please select a different movie.")
        return [], []
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return [], []

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('🎬 MOVIERecommendator 🍿')

selected_movie_name = st.selectbox("Select a movie to get recommendations:", movies['title'].values)


if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    if names:  
        cols = st.columns(5)  
        for idx, col in enumerate(cols):
            with col:
                st.text(names[idx])
                st.image(posters[idx])