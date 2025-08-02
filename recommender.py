import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")
    return ratings, movies

def build_user_movie_matrix(ratings):
    # Criar matriz user x movie com ratings (NaN preenchidos com 0)
    user_movie_matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)
    return user_movie_matrix

def build_similarity_matrix(user_movie_matrix):
    # Transpor para movie x user para calcular similaridade entre filmes
    movie_user_matrix = user_movie_matrix.T
    similarity = cosine_similarity(movie_user_matrix)
    return similarity

def get_recommendations(selected_movie_id, similarity_matrix, user_movie_matrix, n=5):
    movie_ids = user_movie_matrix.columns.tolist()
    movie_id_to_index = {movie_id: idx for idx, movie_id in enumerate(movie_ids)}

    if selected_movie_id not in movie_id_to_index:
        return []

    idx = movie_id_to_index[selected_movie_id]
    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:n+1]
    recommended_indices = [i[0] for i in sim_scores]
    recommended_ids = [movie_ids[i] for i in recommended_indices]
    return recommended_ids
