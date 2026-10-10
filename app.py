import streamlit as st
import pickle
import pandas as pd
import requests

def fetchPoster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(
        url,
        params={
            "api_key": st.secrets["TMDB_API_KEY"],
            "language": "en-US"
        },
        timeout=10
    )
    data = response.json()
    if response.status_code!=200:
        print("HTTP ERROR:", response.status_code)
        print("RESPONSE:", data)
        return None
    poster_path = data.get("poster_path")
    if not poster_path:
        print(f"no poster for id{movie_id}")
        return None
    return "https://image.tmdb.org/t/p/w500"+ data['poster_path' ]

def recommend(movie):
    movie_index = movies[movies['title_movies'] ==movie].index[0]
    distances =similty[movie_index]
    movie_list =sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommendMovies=[]
    recommendMoviesPosters=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].id
        recommendMovies.append(movies.iloc[i[0]].title_movies)
        recommendMoviesPosters.append(fetchPoster(movie_id))
    return recommendMovies, recommendMoviesPosters
movies_dict=pickle.load(open('movieDict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

st.title('Movie recommender')
similty=pickle.load(open('similarity.pkl','rb'))
selectMovieName = st.selectbox(
    'whats in your mind!',
     movies['title_movies'].values
)
if st.button('recemmond'):
    names, posters = recommend(selectMovieName)
    cols = st.columns(5)
    for col, name, poster in zip(cols, names , posters):
        with col:
            st.subheader(name)
            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.write("poster unavailable ")