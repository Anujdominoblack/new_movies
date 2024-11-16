import pickle
import pandas as pd
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Load the models and data
movies_dict = pickle.load(open('movies1.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    # Simulate fetching poster (replace with actual API call)
    return f"https://image.tmdb.org/t/p/w500/{movie_id}.jpg"  # Mock URL (for example)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        movie_id = i[0]
        # fetch poster from an API if needed
        poster = fetch_poster(movies.iloc[i[0]].movie_id)
        recommended_movies.append({
            'title': movies.iloc[i[0]].title,
            'poster': poster
        })
    return recommended_movies


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_movie_name = request.form.get('movie')
        recommendations = recommend(selected_movie_name)
        return render_template('index.html', movies=movies['title'].values, recommendations=recommendations)
    return render_template('index.html', movies=movies['title'].values)


if __name__ == '__main__':
    app.run(debug=True)
