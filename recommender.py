import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

def load_data():
    ratings = pd.read_csv("ml-latest-small/ratings.csv")
    movies = pd.read_csv("ml-latest-small/movies.csv")
    return ratings, movies

def build_user_movie_matrix(ratings):
    user_movie_matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)
    return user_movie_matrix

def build_similarity_matrix(user_movie_matrix):
    scaler = StandardScaler()
    normalized = scaler.fit_transform(user_movie_matrix.T)
    similarity = cosine_similarity(normalized)
    return pd.DataFrame(similarity, index=user_movie_matrix.columns, columns=user_movie_matrix.columns)

def get_recommendations(movie_title, ratings, movies, similarity_matrix, top_n=5):
    movie = movies[movies['title'].str.lower() == movie_title.lower()]
    if movie.empty:
        return []

    movie_id = movie.iloc[0]['movieId']
    if movie_id not in similarity_matrix.columns:
        return []

    similar_scores = similarity_matrix[movie_id].sort_values(ascending=False)
    top_movies = similar_scores.iloc[1:top_n+1].index
    recommended_titles = movies[movies['movieId'].isin(top_movies)]['title'].values.tolist()

    return recommended_titles
