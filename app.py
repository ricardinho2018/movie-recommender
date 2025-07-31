import streamlit as st
from recommender import load_data, build_user_movie_matrix, build_similarity_matrix, get_recommendations

st.title("🎬 Sistema de Recomendação de Filmes - MovieLens")

ratings, movies = load_data()
user_movie_matrix = build_user_movie_matrix(ratings)
similarity_matrix = build_similarity_matrix(user_movie_matrix)

movie_list = movies['title'].sort_values().tolist()
selected_movie = st.selectbox("Escolhe um filme que gostaste:", movie_list)

if st.button("Recomendar"):
    recs = get_recommendations(selected_movie, ratings, movies, similarity_matrix)
    if recs:
        st.subheader("Filmes recomendados:")
        for r in recs:
            st.write("•", r)
    else:
        st.warning("Filme não encontrado ou sem dados suficientes.")
