
import ast

import numpy as np
import pandas as pd
from rich import print
import nltk
from nltk.stem.porter import PorterStemmer


ps =PorterStemmer()  # to combine all same meaning words ** walk , walking, walked**
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

pd.set_option('display.max_columns', None)

movies = pd.read_csv('movies.csv')
credits = pd.read_csv('movies-credits.csv')


# print(movies.head()) 
# print(movies.describe())

movies = movies.merge(credits, how='left', left_on='id', right_on='movie_id', suffixes=('_movies', '_credits'))
#how= left means to keep every row , even if no matching row in the other dataframe.
#head only displays yje first 5 rows of the dataframe.
 
###DATA CLEANING - many coloumns are not needed for our analysis, so we will drop them.

#all features-genres,homepage,id,keywords,original_language,original_title,overview,popularity,production_companies,production_countries,release_date,revenue,runtime,spoken_languages,status,tagline,title,vote_average,vote_count ,movie_id,title,cast,crew

#useful features - id , genres , keywords, overview, title, crew, cast

#features we may use in v2 - popularity, budget, languages
# print(movies.info())

movies =movies[['id', 'genres', 'keywords', 'overview', 'title_movies', 'crew', 'cast']]
# print(movies.isnull())
movies.dropna(inplace=True) #drop rows with null values
# print(movies.duplicated().sum()) #check for duplicates 
#no dubliicates found

def convert(obj):
    L= []
    for i in ast.literal_eval(obj):  #ast.literal_eval() converts a string list into a python list.
        L.append(i['name'])
    return L
    
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)


def convert_cast(obj):
    L= []; counter=0
    for i in ast.literal_eval(obj):  #ast.literal_eval() converts a string list into a python list.
        if counter <= 4:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L
    
def convert_crew(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job'] =='Director':
            L.append(i['name'])
            break
    return L

movies['cast'] =movies['cast'].apply(convert_cast)
movies['crew'] =movies['crew'].apply(convert_crew)

movies['overview'] = movies['overview'].apply(lambda x:x.split()) #labda creates an anonymous function, here it splits the overview into a list of words.



movies['genres'] =movies['genres'].apply(lambda x:[i.replace(" ", "") for i in x]if x else []) #removes spaces from the genres list
movies['keywords'] =movies['keywords'].apply(lambda x:[i.replace(" ", "") for i in x]if x else []) #removes spaces from the keywords list
movies['cast'] =movies['cast'].apply(lambda x:[i.replace(" ", "") for i in x]if x else []) #removes spaces from the cast list
movies['crew'] =movies['crew'].apply(lambda x:[i.replace(" ", "") for   i in x]if x else []) #removes spaces from the crew list
# print(movies.head())


#CREATING A TAGS COLUMN THAT COMBINES ALL THE USEFUL FEATURES INTO A SINGLE COLUMN
movies['tags']= movies['overview']+movies['genres']+movies['cast']+movies['crew']+movies['keywords']

#creating a new dataframe with only the useful features
new_df = movies[['id', 'title_movies', 'tags']].copy()

new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x)) #join the tags into a single string

#converting the tags to lowercase
new_df['tags']= new_df['tags'].apply(lambda x: x.lower())

new_df['tags']=  new_df['tags'].apply(stem)

#text vectorization - converting text into numbers using bag of words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(stop_words='english', max_features=5000)
vectors = cv.fit_transform(new_df['tags']).toarray()


from sklearn.metrics.pairwise import cosine_similarity

similty=cosine_similarity(vectors)


## will find similar movies now 

def recommend(movie):
    movie_index = new_df[new_df['title_movies'] ==movie].index[0]
    distances =similty[movie_index]
    movie_list =sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    for i in movie_list:
        print(new_df.iloc[i[0]].title_movies)
  
recommend('Batman')