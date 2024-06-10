import os
from flask import Flask
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import config
from models import db, Song

app = Flask(__name__)

# Update this line to use PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.SPOTIPY_CLIENT_ID,
                                                           client_secret=config.SPOTIPY_CLIENT_SECRET))

PLAYLIST_ID = '5DoSNtB1JPoPcbBe7xJoOG'
LIMIT = 100  # Maximum value allowed by the API

def track_exists(spotify_id):
    return db.session.query(Song).filter_by(spotify_id=spotify_id).first() is not None

with app.app_context():
    db.create_all()  # Ensure tables are created
    
    offset = 0
    while True:
        results = sp.playlist_tracks(PLAYLIST_ID, limit=LIMIT, offset=offset)
        if not results['items']:
            break
        
        for index, item in enumerate(results['items']):
            track = item['track']
            if track and not track_exists(track['id']):
                print(track['name'])  # Print track name for debugging
                song = Song(
                    spotify_id=track['id'],
                    name=track['name'],
                    artist=', '.join(artist['name'] for artist in track['artists']),
                    votes=0  # Initializing votes to 0
                )
                db.session.add(song)
        
        offset += LIMIT

    db.session.commit()
    print("Database populated with data.")