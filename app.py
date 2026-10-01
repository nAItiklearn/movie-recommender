import streamlit as st
import pickle
import pandas as pd

movieDict =pickle.load(open('movieDict.pkl','rb'))

def recommend(movie):
    movie_index = movies[movies['title_movies'] ==movie].index[0]
    distances =similty[movie_index]
    movie_list =sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommendMovies=[]
    for i in movie_list:
        recommendMovies.append(movies.iloc[i[0]].title_movies)
    return recommendMovies

movies=pd.DataFrame(movieDict)

st.title('Movie recommender')
similty=pickle.load(open('similarity.pkl','rb'))
selectMovieName = st.selectbox(
    'whats in your mind!',
     movies['title_movies'].values
)
if st.button('recommend'):
    recommendation =recommend(selectMovieName)
    for i in recommendation:
       st.write(i)

