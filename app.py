import streamlit as st
import pandas as pd
from recommender import load_data, build_user_movie_matrix, build_similarity_matrix, get_recommendations

st.title("🎬 Sistema de Recomendação de Filmes")

# Funções para o contador
def ler_contador(filename="contador.txt"):
    try:
        with open(filename, "r") as f:
            valor = int(f.read())
    except (FileNotFoundError, ValueError):
        valor = 0
    return valor

def escrever_contador(valor, filename="contador.txt"):
    with open(filename, "w") as f:
        f.write(str(valor))

def incrementar_contador(filename="contador.txt"):
    valor = ler_contador(filename)
    valor += 1
    escrever_contador(valor, filename)
    return valor

# Carregar dados
ratings, movies = load_data()

# Criar matriz e similaridade
user_movie_matrix = build_user_movie_matrix(ratings)
similarity_matrix = build_similarity_matrix(user_movie_matrix)

# Mapear movieId <-> título
movie_ids = user_movie_matrix.columns.tolist()
movie_titles = movies[movies['movieId'].isin(movie_ids)][['movieId', 'title']].drop_duplicates()
id_to_title = dict(zip(movie_titles['movieId'], movie_titles['title']))
title_to_id = {v: k for k, v in id_to_title.items()}

# Seleção do filme pelo título
selected_title = st.selectbox("Escolhe um filme:", list(title_to_id.keys()))

if st.button("Recomendar"):
    # Incrementar contador
    contador = incrementar_contador()
    
    selected_movie_id = title_to_id[selected_title]
    recomendacoes_ids = get_recommendations(selected_movie_id, similarity_matrix, user_movie_matrix)
    recomendacoes_titulos = [id_to_title[mid] for mid in recomendacoes_ids]

    st.write("### Filmes recomendados:")
    for rec in recomendacoes_titulos:
        st.write("✅", rec)
        
    st.write(f"🔢 Número de vezes que o botão 'Recomendar' foi clicado: **{contador}**")
