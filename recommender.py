import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")
    return ratings, movies

def build_user_movie_matrix(ratings, movies):
    data = pd.merge(ratings, movies, on="movieId")
    user_movie_matrix = data.pivot_table(index="userId", columns="title", values="rating")
    user_movie_matrix.fillna(0, inplace=True)
    return user_movie_matrix

def get_recommendations(selected_movie, user_movie_matrix, movies, ratings, top_n=5):
    if selected_movie not in user_movie_matrix.columns:
        return []

    # Vetor do filme selecionado
    movie_vector = user_movie_matrix[selected_movie].values.reshape(1, -1)

    # Calcular similaridade apenas para este filme
    similarity_scores = cosine_similarity(movie_vector, user_movie_matrix.T)[0]

    # Índices ordenados por similaridade
    similar_indices = similarity_scores.argsort()[::-1]

    # Ignorar o próprio filme e selecionar top_n
    top_indices = [i for i in similar_indices if i != user_movie_matrix.columns.get_loc(selected_movie)]
    top_indices = top_indices[:top_n]

    recommended_movies = user_movie_matrix.columns[top_indices]

    # Calcular rating médio
    avg_ratings = ratings.groupby('movieId')['rating'].mean().to_dict()
    title_to_id = dict(zip(movies['title'], movies['movieId']))

    recommendations = []
    for title in recommended_movies:
        movie_id = title_to_id.get(title)
        rating = round(avg_ratings.get(movie_id, 0), 2)
        recommendations.append((title, rating))

    return recommendations
