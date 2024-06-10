import os
from flask import Flask, render_template, request, redirect, url_for
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import random
from models import db, Song, init_db
import config
import logging
import requests  # Make sure to import requests

app = Flask(__name__)

# Update this line to use PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up logging
logging.basicConfig(level=logging.DEBUG)

with app.app_context():
    init_db(app)  # Initialize the database and create tables

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.SPOTIPY_CLIENT_ID,
                                                           client_secret=config.SPOTIPY_CLIENT_SECRET))

@app.route('/')
def index():
    try:
        leaderboard = Song.query.order_by(Song.votes.desc()).limit(10).all()
        return render_template('index.html', leaderboard=leaderboard)
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return f"An error occurred: {e}"

@app.route('/vote')
def vote():
    try:
        tracks = Song.query.all()
        song1, song2 = random.sample(tracks, 2)
        app.logger.debug(f"Song1: {song1}")
        app.logger.debug(f"Song2: {song2}")
        return render_template('vote.html', song1=song1, song2=song2)
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return f"An error occurred: {e}", 500

@app.route('/vote/<int:song_id>')
def cast_vote(song_id):
    try:
        vercel_url = os.getenv("VERCEL_URL")
        if not vercel_url:
            raise ValueError("VERCEL_URL environment variable not set")

        response = requests.get(f'{vercel_url}/api/vote?song_id={song_id}')
        if response.status_code == 200:
            return redirect(url_for('vote'))
        else:
            raise Exception(response.text)
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
