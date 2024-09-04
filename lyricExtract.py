# Getting song lyrics for each song in playlist
# using downloaded spotify user data

import json
import os
import azapi
from tqdm import tqdm  # Progress bar library

# Paths to the JSON files
library_file = "my_spotify_data/Spotify Account Data/YourLibrary.json"
playlist_file = "my_spotify_data/Spotify Account Data/Playlist1.json"

# Directory where lyrics will be saved
lyrics_base_dir = "lyrics/"

# Initialize the AZlyrics API
API = azapi.AZlyrics('google', accuracy=0.5)

# Function to save lyrics to a file
def save_lyrics(artist, album, title, lyrics, folder):
    filename = f"{artist}_{album}_{title}.txt"
    file_path = os.path.join(folder, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(lyrics)

# Function to record songs with no lyrics found
def record_failed_song(artist, album, title, folder):
    no_lyrics_file = os.path.join(folder, "no_lyrics_found.txt")
    with open(no_lyrics_file, 'a', encoding='utf-8') as file:
        file.write(f"{artist} - {album} - {title}\n")

# Function to process songs
def process_songs(songs, folder_name):
    folder_path = os.path.join(lyrics_base_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    for song in tqdm(songs, desc=f"Processing {folder_name}"):
        artist = song.get('artist')
        album = song.get('album')
        title = song.get('track')

        if not artist or not title:
            continue

        # Set the artist and title for the API
        API.artist = artist
        API.title = title

        # Get the lyrics
        try:
            API.getLyrics(save=False)
        except IndexError:
            # Handle cases where metadata is missing
            print(f"Skipping {artist} - {title}: no metadata found.")
            record_failed_song(artist, album, title, folder_path)
            continue

        # Save or record failed songs
        if API.lyrics and "No lyrics found" not in API.lyrics:
            save_lyrics(API.artist, album, API.title, API.lyrics, folder_path)
        else:
            record_failed_song(artist, album, title, folder_path)

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


