# Getting song lyrics for each song in playlist
# using downloaded spotify user data

import json
import os
import azapi
import requests
import time
from duckduckgo_search import DDGS
from tqdm import tqdm  # Progress bar library

# Paths to the JSON files
library_file = "my_spotify_data/Spotify Account Data/YourLibrary.json"
playlist_file = "my_spotify_data/Spotify Account Data/Playlist1.json"

# Directory where lyrics will be saved
lyrics_base_dir = "lyrics/"

# Initialize the AZlyrics API
# API = azapi.AZlyrics('duckduckgo', accuracy=0.5)

# Function to sanitize filenames
def sanitize_filename(filename):
    return ''.join(c for c in filename if c not in r'<>:"/\|?*').strip()

# Function to save lyrics to a file
def save_lyrics(artist, album, title, lyrics, folder):
    filename = f"{sanitize_filename(artist)}_{sanitize_filename(album)}_{sanitize_filename(title)}.txt"
    file_path = os.path.join(folder, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(lyrics)

# Function to check if lyrics already exist
def lyrics_exist(artist, album, title, folder):
    filename = f"{sanitize_filename(artist)}_{sanitize_filename(album)}_{sanitize_filename(title)}.txt"
    return os.path.exists(os.path.join(folder, filename))

def record_failed_song(artist, album, title, folder_path):
    file_path = os.path.join(folder_path, "__failed_songs.txt")
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"{artist} - {album} - {title}\n")

def process_songs(songs, folder_name):
    folder_path = os.path.join("lyrics", folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    # Create or clear failed_songs.txt
    failed_songs_path = os.path.join(folder_path, "__failed_songs.txt")
    with open(failed_songs_path, 'w', encoding='utf-8') as file:
        file.write("Failed Songs:\n")

    # Initialize azapi with DuckDuckGo
    API = azapi.AZlyrics('duckduckgo')
    
    for song in tqdm(songs, desc=f"Processing {folder_name}"):
        artist = song.get('artist')
        album = song.get('album')
        title = song.get('track')

        if not artist or not title:
            continue

        # Skip songs with lyrics already saved
        if lyrics_exist(artist, album, title, folder_path):
            continue

        # Set the artist and title for the API
        API.artist = artist
        API.title = title

        retries = 1
        while retries > 0:
            try:
                searchUrl = DDGS().text(f'{title} by {artist} from {album} lyrics site:azlyrics.com', max_results=1)[0]['href']

                # Retrieve lyrics with rate limiting
                API.getLyrics(url=searchUrl, save=False)
                time.sleep(1)  # Limit to one request per second

                if API.lyrics.strip() and "No lyrics found" not in API.lyrics:
                    save_lyrics(API.artist, album, API.title, API.lyrics, folder_path)
                    break
                else:
                    record_failed_song(API.artist, album, API.title, folder_path)
                    break

            except (requests.exceptions.ConnectionError, IndexError) as e:
                print(f"Error retrieving lyrics for {artist} - {title}: {e}")
                retries -= 1
                time.sleep(5)
                if retries == 0:
                    record_failed_song(artist, album, title, folder_path)
                    API.artist = ""
                    API.title = ""
                    continue

        # Reset API attributes to avoid carrying over data
        API.artist = ""
        API.title = ""


# Load liked songs and process them
with open(library_file, 'r', encoding='utf-8') as f:
    library_data = json.load(f)
    liked_songs = library_data.get('tracks', [])
    process_songs(liked_songs, "liked_songs")

# Load the "get it" playlist and process it
with open(playlist_file, 'r', encoding='utf-8') as f:
    playlist_data = json.load(f)
    get_it_playlist = next((p for p in playlist_data.get('playlists', []) if p.get('name') == "get it"), None)
    if get_it_playlist:
        get_it_songs = get_it_playlist.get('items', [])
        process_songs(get_it_songs, "get_it_playlist")



