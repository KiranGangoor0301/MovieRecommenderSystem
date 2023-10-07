# -*- coding: utf-8 -*-
"""MovieRecommenderSystem.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OoRGO5e3KXLe88dBSEN7sRVVgETXcOsj
"""

import pandas as pd
import numpy as np

movies=pd.read_csv('/content/tmdb_5000_movies.csv')

credits=pd.read_csv('/content/tmdb_5000_credits.csv')

movies.head()

credits

movies=movies.merge(credits,on='title')

movies.head()

movies_data=movies[['genres','id','keywords','overview','title','cast','crew']]

movies_data.head()

movies_data.isnull().sum()

movies_data.dropna(inplace=True)

import ast
def convert(dict):
  list=[]
  for i in ast.literal_eval(dict):
    list.append(i['name'])
  return list

dict=movies_data['genres'][0]
dict

movies_data['genres']=movies_data['genres'].apply(convert)

movies_data['keywords']=movies_data['keywords'].apply(convert)

def overview(obj):
  for i in obj:
    obj=obj.split()
  return obj

movies_data['overview']=movies_data['overview'].apply(lambda x:x.split())

movies_data['cast'][0]

def fetch_cast(obj):
  cnt=0
  list=[]
  for i in ast.literal_eval(obj):
    if cnt!=3:
      list.append(i['name'])
      cnt=cnt+1
    else:
      break
  return list

movies_data['cast']=movies_data['cast'].apply(fetch_cast)

movies_data['crew'][0]

def fetch_director(obj):
  list=[]
  for i in ast.literal_eval(obj):
    if i['job']=='Director':
      list.append(i['name'])
  return list

movies_data['crew']=movies_data['crew'].apply(fetch_director)

movies_data.head()

movies_data['genres']=movies_data['genres'].apply(lambda x:[i.replace(" ",'') for i in x])
movies_data['keywords']=movies_data['keywords'].apply(lambda x:[i.replace(" ",'') for i in x])
movies_data['cast']=movies_data['cast'].apply(lambda x:[i.replace(" ",'') for i in x])
movies_data['crew']=movies_data['crew'].apply(lambda x:[i.replace(" ",'') for i in x])

movies_data.head()

movies_data['tags']=movies_data['overview'] + movies_data['genres']  + movies_data['keywords'] + movies_data['cast'] +movies_data['crew']

movie=movies_data[['id','title','tags']]

movie.head()

movie['tags']=movie['tags'].apply(lambda x:" ".join(x))

movie.head()

movie['tags']=movie['tags'].apply(lambda x:x.lower())

from sklearn.feature_extraction.text import CountVectorizer

cv=CountVectorizer(stop_words='english',max_features=5000)

vector=cv.fit_transform(movie['tags']).toarray()

vector[0]

import nltk

from nltk.stem.porter import PorterStemmer

ps=PorterStemmer()

def stem(x):
  list=[]
  for i in x.split():
    list.append(ps.stem(x))
  return " ".join(list)

movie['tags']=movie['tags'].apply(stem)

from sklearn.metrics.pairwise import cosine_similarity

similar=cosine_similarity(vector)

similar[0]

def recommend(movies):
  movie_index=movie[movie['title']==movies].index[0]
  distance=similar[movie_index]
  movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]

  for i in movie_list:
    print(movie.iloc[i[0]].title)

name=input("Enter your movie name to recommend:--")

recommend(name)
