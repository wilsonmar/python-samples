#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
"""
This is show-recommendations.py at 
https://github.com/wilsonmar/python-samples/blob/main/show-recommendations.py
   Not yet explained at https://wilsonmar.github.io/python-samples 
   Based on https://hackr.io/blog/python-projects

This program provides a GUI created (using tkinter) to select movies and TV shows as an example of data science machine learning. See https://hackr.io/blog/python-concepts-data-science

tkinter (which comes with Python) is used to create the GUI containing labels, buttons, and entry fields. The user enters a title they enjoyed and the app returns recommendations based on a database from the Kaggle competition.
The .csv file in the data folder combines csv files unzipped from Amazon Prime, Disney, Hulu, Netflix from https://www.kaggle.com/datasets/shivamb/hulu-movies-and-tv-shows

Each csv has the same header row: show_id,type,title,director,cast,country,date_added,release_year,rating,duration,listed_in,description
so can be combined into a 22,999 row file using command: 
cd into the data folder.
   csvstack orderline_123456.csv orderline_896524.csv > file_load.csv
   or
   head -n 1 file1.csv > merged.csv 
   tail -n+2 file2.csv >> merged.csv
   or
   awk -F, -v OFS=, '{$(NF+1)="Disney"; print}' disney_plus_titles.csv >> combined.csv
   awk -F, -v OFS=, '{$(NF+1)="Hulu"; print}' hulu_titles.csv >> combined.csv
   awk -F, -v OFS=, '{$(NF+1)="Netflix"; print}' netflix_titles.csv >> combined.csv
# Move combined.csv above the data folder.
# Open combined.csv in LibreOffice to change top row last column heading to "Platform".
# Search of "show_id," to remove extra headings.
TODO: Fix code to recognize column for Streaming platform.
   
The ‘cosine similarity’ algorithm is used to to find similar results based on user input. 

Although not scalable, pandas and numpy are used to clean the data and prepare it for processing.

A requirements.txt file accompanies this file to specify the version of each import specified below. It is generated from the requirements.in file using command "pip-compile requirements.in" after pip install pip-tools.
"""

# Thse are part of the Python standard library not need pip install:
import tkinter as tk
# These require pip install:
from nltk.tokenize import word_tokenize
import numpy as np
import pandas as pd
import re  # regular expressions
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

data = pd.read_csv('shows.csv')
data = data.dropna(subset=['Cast', 'Production Country', 'Rating'])
# FIXME: above: File "/Users/johndoe/github-wilsonmar/python-samples/show-recommendations/./show-recommendations.py", line 38, in <module>
movies = data[data['Content Type'] == 'Movie'].reset_index()
movies = movies.drop(['index', 'Show Id', 'Content Type', 'Date Added',
                    'Release Date', 'Duration', 'Description'], axis=1)
movies.head()
tv = data[data['Content Type'] == 'TV Show'].reset_index()
tv = tv.drop(['index', 'Show Id', 'Content Type', 'Date Added',
            'Release Date', 'Duration', 'Description'], axis=1)
tv.head()
actors = []
for i in movies['Cast']:
   actor = re.split(r', \s*', i)
   actors.append(actor)
flat_list = []

for sublist in actors:
   for item in sublist:
       flat_list.append(item)

actors_list = sorted(set(flat_list))
binary_actors = [[0] * 0 for i in range(len(set(flat_list)))]
for i in movies['Cast']:
   k = 0
   for j in actors_list:
       if j in i:
           binary_actors[k].append(1.0)
       else:
           binary_actors[k].append(0.0)
       k += 1

binary_actors = pd.DataFrame(binary_actors).transpose()
directors = []
for i in movies['Director']:
   if pd.notna(i):
       director = re.split(r', \s*', i)
       directors.append(director)

flat_list_2 = []
for sublist in directors:
   for item in sublist:
       flat_list_2.append(item)

directors_list = sorted(set(flat_list_2))
binary_directors = [[0] * 0 for i in range(len(set(flat_list_2)))]
for i in movies['Director']:
   k = 0
   for j in directors_list:
       if pd.isna(i):
           binary_directors[k].append(0.0)
       elif j in i:
           binary_directors[k].append(1.0)
       else:
           binary_directors[k].append(0.0)
       k += 1

binary_directors = pd.DataFrame(binary_directors).transpose()
countries = []
for i in movies['Production Country']:
   country = re.split(r', \s*', i)
   countries.append(country)

flat_list_3 = []
for sublist in countries:
   for item in sublist:
       flat_list_3.append(item)

countries_list = sorted(set(flat_list_3))
binary_countries = [[0] * 0 for i in range(len(set(flat_list_3)))]
for i in movies['Production Country']:
   k = 0
   for j in countries_list:
       if j in i:
           binary_countries[k].append(1.0)
       else:
           binary_countries[k].append(0.0)
       k += 1

binary_countries = pd.DataFrame(binary_countries).transpose()
genres = []
for i in movies['Genres']:
   genre = re.split(r', \s*', i)
   genres.append(genre)

flat_list_4 = []
for sublist in genres:
   for item in sublist:
       flat_list_4.append(item)

genres_list = sorted(set(flat_list_4))
binary_genres = [[0] * 0 for i in range(len(set(flat_list_4)))]
for i in movies['Genres']:
   k = 0
   for j in genres_list:
       if j in i:
           binary_genres[k].append(1.0)
       else:
           binary_genres[k].append(0.0)
       k += 1

binary_genres = pd.DataFrame(binary_genres).transpose()
ratings = []
for i in movies['Rating']:
   ratings.append(i)

ratings_list = sorted(set(ratings))
binary_ratings = [[0] * 0 for i in range(len(set(ratings_list)))]
for i in movies['Rating']:
   k = 0
   for j in ratings_list:
       if j in i:
           binary_ratings[k].append(1.0)
       else:
           binary_ratings[k].append(0.0)
       k += 1

binary_ratings = pd.DataFrame(binary_ratings).transpose()
binary = pd.concat([binary_actors, binary_directors,
                  binary_countries, binary_genres], axis=1, ignore_index=True)
actors_2 = []
for i in tv['Cast']:
  actor2 = re.split(r', \s*', i)
  actors_2.append(actor2)

flat_list_5 = []
for sublist in actors_2:
   for item in sublist:
       flat_list_5.append(item)

actors_list_2 = sorted(set(flat_list_5))
binary_actors_2 = [[0] * 0 for i in range(len(set(flat_list_5)))]
for i in tv['Cast']:
   k = 0
   for j in actors_list_2:
       if j in i:
           binary_actors_2[k].append(1.0)
       else:
           binary_actors_2[k].append(0.0)
       k += 1

binary_actors_2 = pd.DataFrame(binary_actors_2).transpose()
countries_2 = []
for i in tv['Production Country']:
   country2 = re.split(r', \s*', i)
   countries_2.append(country2)

flat_list_6 = []
for sublist in countries_2:
   for item in sublist:
       flat_list_6.append(item)

countries_list_2 = sorted(set(flat_list_6))
binary_countries_2 = [[0] * 0 for i in range(len(set(flat_list_6)))]
for i in tv['Production Country']:
   k = 0
   for j in countries_list_2:
       if j in i:
           binary_countries_2[k].append(1.0)
       else:
           binary_countries_2[k].append(0.0)
       k += 1

binary_countries_2 = pd.DataFrame(binary_countries_2).transpose()
genres_2 = []
for i in tv['Genres']:
   genre2 = re.split(r', \s*', i)
   genres_2.append(genre2)

flat_list_7 = []
for sublist in genres_2:
   for item in sublist:
       flat_list_7.append(item)

genres_list_2 = sorted(set(flat_list_7))
binary_genres_2 = [[0] * 0 for i in range(len(set(flat_list_7)))]
for i in tv['Genres']:
   k = 0
   for j in genres_list_2:
       if j in i:
           binary_genres_2[k].append(1.0)
       else:
           binary_genres_2[k].append(0.0)
       k += 1

binary_genres_2 = pd.DataFrame(binary_genres_2).transpose()
ratings_2 = []
for i in tv['Rating']:
   ratings_2.append(i)

ratings_list_2 = sorted(set(ratings_2))
binary_ratings_2 = [[0] * 0 for i in range(len(set(ratings_list_2)))]
for i in tv['Rating']:
   k = 0
   for j in ratings_list_2:
       if j in i:
           binary_ratings_2[k].append(1.0)
       else:
           binary_ratings_2[k].append(0.0)
       k += 1

binary_ratings_2 = pd.DataFrame(binary_ratings_2).transpose()
binary_2 = pd.concat([binary_actors_2, binary_countries_2,
                    binary_genres_2], axis=1, ignore_index=True)

window = tk.Tk()
window.geometry('600x600')
head = tk.Label(window, text='Enter Movie / TV Show on Netflix For Recommendations', font=('Calibri 15'))
head.pack(pady=20)


def netflix_recommender(search):
   cs_list = []
   binary_list = []

   if search in movies['Title'].values:
       idx = movies[movies['Title'] == search].index.item()
       for i in binary.iloc[idx]:
           binary_list.append(i)

       point_1 = np.array(binary_list).reshape(1, -1)
       point_1 = [val for sublist in point_1 for val in sublist]
       for j in range(len(movies)):
           binary_list_2 = []
           for k in binary.iloc[j]:
               binary_list_2.append(k)
           point_2 = np.array(binary_list_2).reshape(1, -1)
           point_2 = [val for sublist in point_2 for val in sublist]
           dot_product = np.dot(point_1, point_2)
           norm_1 = np.linalg.norm(point_1)
           norm_2 = np.linalg.norm(point_2)
           cos_sim = dot_product / (norm_1 * norm_2)
           cs_list.append(cos_sim)

       movies_copy = movies.copy()
       movies_copy['cos_sim'] = cs_list
       results = movies_copy.sort_values('cos_sim', ascending=False)
       results = results[results['title'] != search]
       top_results = results.head(5)
       return (top_results)

   elif search in tv['Title'].values:
       idx = tv[tv['Title'] == search].index.item()
       for i in binary_2.iloc[idx]:
           binary_list.append(i)

       point_1 = np.array(binary_list).reshape(1, -1)
       point_1 = [val for sublist in point_1 for val in sublist]
       for j in range(len(tv)):
           binary_list_2 = []
           for k in binary_2.iloc[j]:
               binary_list_2.append(k)

           point_2 = np.array(binary_list_2).reshape(1, -1)
           point_2 = [val for sublist in point_2 for val in sublist]
           dot_product = np.dot(point_1, point_2)
           norm_1 = np.linalg.norm(point_1)
           norm_2 = np.linalg.norm(point_2)
           cos_sim = dot_product / (norm_1 * norm_2)
           cs_list.append(cos_sim)

       tv_copy = tv.copy()
       tv_copy['cos_sim'] = cs_list
       results = tv_copy.sort_values('cos_sim', ascending=False)
       results = results[results['Title'] != search]
       top_results = results.head(5)
       return (top_results)

   else:
       return ('Title not in dataset. Please check spelling.')


def call_recommender():
  subject = text.get()
  recommendation = netflix_recommender(subject)
  txt = ''
  for i in recommendation.iterrows():
      txt += 'Title: ' + str(i[1][0]) + '\n'
  tk.Label(window, text=txt, font=('Calibri 15')).place(x=195, y=150)


text = tk.StringVar()
tk.Entry(window, textvariable=text).place(x=200, y=80, height=30, width=280)
tk.Button(window, text='Find Recommendations',
         command=call_recommender).place(x=285, y=150)
window.mainloop()
