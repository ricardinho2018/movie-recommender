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

def build_similarity_matrix(user_movie_matrix):
    similarity = cosine_similarity(user_movie_matrix.T)
    return similarity

def get_recommendations(selected_movie, user_movie_matrix, similarity_matrix, movies, ratings, top_n=5):
    if selected_movie not in user_movie_matrix.columns:
        return []

    movie_idx = user_movie_matrix.columns.get_loc(selected_movie)
    similarity_scores = list(enumerate(similarity_matrix[movie_idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    top_similar_indices = [i for i, _ in similarity_scores[1:top_n+1]]
    recommended_movies = user_movie_matrix.columns[top_similar_indices]

    # Calcular rating médio
    avg_ratings = ratings.groupby('movieId')['rating'].mean()

    recommendations = []
    for title in recommended_movies:
        movie_id = movies[movies['title'] == title]['movieId'].values[0]
        rating = round(avg_ratings.get(movie_id, 0), 2)
        recommendations.append((title, rating))

    return recommendations
