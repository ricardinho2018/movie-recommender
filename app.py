import streamlit as st
from recommender import load_data, build_user_movie_matrix, get_recommendations

# --- Carregar dados ---
st.title("🎬 Sistema de Recomendação de Filmes")

st.write("Carregando dados...")
ratings, movies = load_data()
user_movie_matrix = build_user_movie_matrix(ratings, movies)

# --- Seleção de filme ---
selected_movie = st.selectbox(
    "Escolhe um filme para ver recomendações:",
    options=sorted(user_movie_matrix.columns)
)

# --- Botão para gerar recomendações ---
if st.button("Gerar Recomendações"):
    if selected_movie:
        recommendations = get_recommendations(
            selected_movie,
            user_movie_matrix,
            movies,
            ratings
        )

        if recommendations:
            st.subheader(f"Filmes parecidos com **{selected_movie}**:")
            for title, rating in recommendations:
                st.write(f"🎥 {title} — ⭐ {rating}")
        else:
            st.warning("Não foi possível encontrar recomendações para este filme.")
