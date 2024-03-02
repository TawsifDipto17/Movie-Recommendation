import streamlit as st
import pandas as pd
import requests
movies_list = pd.read_pickle("movies.pkl")
similarity = pd.read_pickle("sim.pkl")

# movies_list = pickle.load(open('movies.pkl','rb'))
st.set_page_config(layout="wide")
st.title('Movie Recommender System')

selected = st.selectbox(
    'Select a movie to receive recommendations',
    movies_list['title'].values)

def get_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=3a77f72777ff8166666e61462488f8c0'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w400/" + data['poster_path']

def get_release(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=3a77f72777ff8166666e61462488f8c0'.format(movie_id))
    data = response.json()
    return "Release: " + data['release_date']


def recommend(movie):
 with st.spinner("Loading..."):
    idx = movies_list[movies_list['title']== movie].index[0]
    sim = similarity[idx]
    movies = sorted(list(enumerate(sim)),reverse=True,key=lambda x:x[1])[1:20]

    recommended_movies = []
    recommended_movies_poster = []
    release_dates=[]
    for i in movies:
        movie_id = movies_list.iloc[i[0]].id
        recommended_movies.append((movies_list.iloc[i[0]].title))
        recommended_movies_poster.append(get_poster(movie_id))
        release_dates.append(get_release(movie_id))
        
 return recommended_movies,recommended_movies_poster,release_dates

if st.button('Recommend'):
     names,posters,release = recommend(selected)
     st.write('Selected Movie: ', selected)
     i=0
     while i<19 :
        col1,col2,col3,col4 = st.columns(4)
        st.markdown("---")
        with col1:
             st.text(names[i])
             st.image(posters[i])
             st.text(release[i])
        with col2:
             st.text(names[i+1])
             st.image(posters[i+1])
             st.text(release[i+1])
        with col3:
             st.text(names[i+2])
             st.image(posters[i+2])
             st.text(release[i+2])
        if i+3 < 19:     
            with col4:
                st.text(names[i+3])
                st.image(posters[i+3])
                st.text(release[i+3])
        i+=4     
             

