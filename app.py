import os
from flask import Flask, render_template, request, redirect, url_for
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import random
from models import db, Song, init_db
import config
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
        return f"An error occurred: {e}"

@app.route('/vote')
def vote():
    try:
        # Query all songs from the database
        tracks = Song.query.all()

        # Randomly select two songs from the list
        song1, song2 = random.sample(tracks, 2)

        # Debug statements to log the selected songs
        app.logger.debug(f"Song1: {song1}")
        app.logger.debug(f"Song2: {song2}")

        # Render the vote.html template with the selected songs
        return render_template('vote.html', song1=song1, song2=song2)

    except Exception as e:
        # Log the error message
        app.logger.error(f"An error occurred: {e}")
        return f"An error occurred: {e}", 500

@app.route('/vote/<int:song_id>')
def cast_vote(song_id):
    try:
        song = Song.query.get(song_id)
        if song:
            song.votes += 1
            db.session.commit()
        return redirect(url_for('vote'))
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)