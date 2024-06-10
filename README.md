# Spotify Voting Application

This application allows users to vote for their favorite songs from a choice of two from a Spotify playlist, with the results displayed on a leaderboard.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- Fetches tracks from a specified Spotify playlist.
- Allows users to vote for their favorite tracks.
- Displays a leaderboard of the most voted tracks.
- Uses Flask for the backend.
- Stores song data and votes in a SQLite database.
- Handles Spotify authentication using Spotipy.

## Prerequisites

- Python 3.9
- Flask
- Spotipy
- SQLite
- Spotify Developer Account (for API credentials)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/tferracina/spotify_voting.git
    cd spotify_voting
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Spotify Developer Setup:**
    - Create a new application at the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
    - Note down the `Client ID` and `Client Secret`.

2. **Configuration File:**
    - Create a `config.py` file in the root directory of the project with the following content:

      ```python
      SPOTIPY_CLIENT_ID = 'your_spotify_client_id'
      SPOTIPY_CLIENT_SECRET = 'your_spotify_client_secret'
      PLAYLIST_ID = 'your_spotify_playlist_id'
      ```

3. **Database Initialization:**
    - Initialize the SQLite database by running:

      ```bash
      python
      >>> from app import init_db
      >>> init_db()
      >>> exit()
      ```

## Usage

1. **Run the Flask application:**

    ```bash
    flask run
    ```

2. **Access the application:**
    - Open your web browser and go to `http://127.0.0.1:5000`.

## Deployment

To deploy the application to a cloud service like Google Cloud Run:

1. **Containerize the Flask application using Docker:**

    Create a `Dockerfile`:

    ```dockerfile
    FROM python:3.9-slim

    WORKDIR /app

    COPY requirements.txt requirements.txt
    RUN pip install -r requirements.txt

    COPY . .

    CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
    ```

2. **Build and push the Docker image to a container registry:**

    ```bash
    gcloud builds submit --tag gcr.io/your-project-id/flask-app
    ```

3. **Deploy to Cloud Run:**

    ```bash
    gcloud run deploy flask-app --image gcr.io/your-project-id/flask-app --platform managed --region us-central1
    ```

## Contributing

We welcome contributions to the Spotify Voting Application! To contribute, please fork the repository, create a new branch, and submit a pull request. Make sure to follow the code style and include tests for new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
