import streamlit as st
from recommender import load_data, build_user_movie_matrix, get_recommendations


st.title("🎬 Sistema de Recomendação de Filmes")

# Carregar dados e construir matrizes
ratings, movies = load_data()
user_movie_matrix = build_user_movie_matrix(ratings, movies)


# Interface
movie_list = movies['title'].sort_values().tolist()
selected_movie = st.selectbox("Escolhe um filme que gostaste:", movie_list)

if st.button("Recomendar"):
    recommendations = get_recommendations(
        selected_movie,
        user_movie_matrix,
        similarity_matrix,
        movies,
        ratings
    )
    
    if recommendations:
        st.subheader("🎯 Filmes recomendados:")
        for title, rating in recommendations:
            st.write(f"**{title}** — ⭐ {rating}/5")
    else:
        st.write("⚠️ Nenhuma recomendação encontrada.")


