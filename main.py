
import ast

import numpy as np
import pandas as pd
from rich import print



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
        if counter <= 3:
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
print(movies.head())
