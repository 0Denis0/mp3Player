import json
import os
import requests
import time
from bs4 import BeautifulSoup
from tqdm import tqdm  # Progress bar library

# Paths to the JSON files
library_file = "my_spotify_data/Spotify Account Data/YourLibrary.json"
playlist_file = "my_spotify_data/Spotify Account Data/Playlist1.json"

# Directory where lyrics will be saved
lyrics_base_dir = "lyrics/"

def lyrics_exist(artist, album, title, folder_path):
    file_name = f"{artist}_{album}_{title}.txt"
    file_path = os.path.join(folder_path, file_name)
    return os.path.isfile(file_path)

def save_lyrics(artist, album, title, lyrics, folder_path):
    file_name = f"{artist}_{album}_{title}.txt"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(lyrics)

def record_failed_song(artist, album, title, folder_path):
    file_path = os.path.join(folder_path, "failed_songs.txt")
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"{artist} - {album} - {title}\n")

def get_azlyrics_url(artist, title):
    query = f"{artist} {title} site:azlyrics.com"
    search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        first_result = soup.find('a', href=True)
        if first_result and 'azlyrics.com' in first_result['href']:
            return first_result['href']
    except Exception as e:
        print(f"Error fetching search results: {e}")
    return None

def scrape_lyrics(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        lyrics_div = soup.find('div', class_='col-xs-12 col-lg-8 text-center')
        if lyrics_div:
            lyrics = lyrics_div.get_text(separator='\n').strip()
            return lyrics
    except Exception as e:
        print(f"Error fetching lyrics from URL: {e}")
    return None

def process_songs(songs, folder_name):
    folder_path = os.path.join("lyrics", folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    # Create or clear failed_songs.txt
    failed_songs_path = os.path.join(folder_path, "failed_songs.txt")
    with open(failed_songs_path, 'w', encoding='utf-8') as file:
        file.write("Failed Songs:\n")

    for song in tqdm(songs, desc=f"Processing {folder_name}"):
        artist = song.get('artist')
        album = song.get('album')
        title = song.get('track')

        if not artist or not title:
            continue

        # Skip songs with lyrics already saved
        if lyrics_exist(artist, album, title, folder_path):
            continue

        # Get AZLyrics URL
        search_url = get_azlyrics_url(artist, title)
        if search_url:
            print(f"Found AZLyrics URL: {search_url}")
            lyrics = scrape_lyrics(search_url)
            if lyrics:
                save_lyrics(artist, album, title, lyrics, folder_path)
            else:
                print(f"Lyrics not found for {artist} - {title}.")
                record_failed_song(artist, album, title, folder_path)
        else:
            print(f"No AZLyrics URL found for {artist} - {title}.")
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