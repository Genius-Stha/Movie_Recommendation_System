import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1MjQ3M2VlYTY3NDdkNjA5ZjYwMWRlODk1ZTM2YTkxYyIsInN1YiI6IjY1NjBlY2VhMzY3OWExMDk3N2UwMjFiYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.kvapx4x6P7UV72Tt9u0MO8OcYBiLkyvl1iBfhEbrDX8"
    }

    response = requests.get(url, headers=headers)
    data =response.json()
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']

movies_list = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommendation System')

def recommend(movie):
    movie_index = movies_list[movies_list['title']==movie].index[0]
    distances = similarity[movie_index]
    movies=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6] #gives most similar movies
    recommended_movies=[]
    recommended_movies_poster=[]
    
    for i in movies:
        recommended_movies.append(movies_list.iloc[i[0]].title)
        movie_id=movies_list.iloc[i[0]].id
        recommended_movies_poster.append(fetch_poster(movie_id))
        
    return recommended_movies,recommended_movies_poster

movie = st.selectbox(
    'Name of the movie you like',
    (movies_list['title'].values)
)

if st.button('Recommend'):
    names,poster = recommend(movie)
    cols1,cols2,cols3,cols4,cols5 = st.columns(5)
    with cols1:
        st.text(names[0])
        st.image(poster[0])
    with cols2:
        st.text(names[1])
        st.image(poster[1])
    with cols3:
        st.text(names[2])
        st.image(poster[2])
    with cols4:
        st.text(names[3])
        st.image(poster[3])
    with cols5:
        st.text(names[4])
        st.image(poster[4])