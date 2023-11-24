import numpy as np
import pandas as pd
import ast
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle


movie = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

movies=movie.merge(credits,on ='title')

movies= movies[['genres' , 'id' , 'keywords' , 'title' , 'overview', 'cast' ,'crew']]
movies.dropna(inplace = True)

def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L
def name_convert(obj):
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter!=3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L
def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i['name'])
    return L

movies['genres']=movies['genres'].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)
movies['cast']=movies['cast'].apply(name_convert)
movies['crew']=movies['crew'].apply(fetch_director)

movies['overview']=movies['overview'].apply(lambda x:x.split())
movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","")for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","")for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","")for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","")for i in x])
movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']

new_df = movies[['id','title','tags']]
new_df['tags'] = new_df['tags'].apply(lambda x: ' '.join(x))
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())
ps = PorterStemmer()                       #to remove ..s,..ed 'similar but different verbs words'

def stem(text):
    y =[]
    for i in text.split():
        y.append(ps.stem(i))
        
    return " ".join(y)
new_df['tags']=new_df['tags'].apply(stem)
cv = CountVectorizer(max_features=5000,stop_words='english')
vectors=cv.fit_transform(new_df['tags']).toarray()
cv.get_feature_names_out()[:100]

similarity=cosine_similarity(vectors)
similarity.shape                    #distance between every movies

def recommend(movie):
    movie_index = new_df[new_df['title']==movie].index[0]
    distances = similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6] #gives most similar movies
    for i in movie_list:
        print(new_df.iloc[i[0]].title)
        
pickle.dump(new_df,open('movies.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))        
while True:
    movie_name = input('Enter the name of the movie you like : ').title()
    if movie_name == 'Stop' or movie_name== 'No' or movie_name=='N'or movie_name=='Exit':
        break
    print("The Movie recommendations are : \n",)

    recommend(movie_name)
