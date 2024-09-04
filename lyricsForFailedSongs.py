# lyrics for failed songs

import os
import json

# Sanitize function for filenames
def sanitize_filename(filename):
    return ''.join(c for c in filename if c not in r'<>:"/\|?*').strip()

# Load JSON data from a file
def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

# Get the saved songs from the folder
def get_saved_songs(folder_path):
    saved_songs = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):  # Lyrics files are .txt
            saved_songs.append(file_name)
    return saved_songs

# Extract songs from the JSON
def get_songs_from_json(json_data, key='tracks'):
    songs = []
    for song in json_data[key]:
        artist = song.get('artist')
        title = song.get('track')
        album = song.get('album')
        if artist and title and album:
            # Sanitize and format the filename
            sanitized_filename = f"{sanitize_filename(artist)}_{sanitize_filename(album)}_{sanitize_filename(title)}.txt"
            songs.append(sanitized_filename)
    return songs

# Compare JSON songs with saved files
def find_missing_songs(folder_path, json_filepath, key='tracks'):
    saved_songs = get_saved_songs(folder_path)
    json_data = load_json(json_filepath)
    json_songs = get_songs_from_json(json_data, key)
    
    # Find songs in JSON but not in the folder
    missing_songs = [song for song in json_songs if song not in saved_songs]
    return missing_songs

# Save missing songs to JSON file
def save_missing_songs(missing_songs, folder_path):
    missing_songs_filepath = os.path.join(folder_path, 'missingSongs.json')
    with open(missing_songs_filepath, 'w', encoding='utf-8') as file:
        json.dump(missing_songs, file, indent=4, ensure_ascii=False)

# Main function to process liked_songs and get_it_playlist folders
def process_folders_and_jsons():
    # Define paths to the folders and JSONs
    liked_songs_folder = "lyrics/liked_songs"
    get_it_playlist_folder = "lyrics/get_it_playlist"
    
    liked_songs_json = "my_spotify_data/Spotify Account Data/YourLibrary.json"
    get_it_playlist_json = "my_spotify_data/Spotify Account Data/Playlist1.json"
    
    # Find missing songs for liked_songs
    missing_liked_songs = find_missing_songs(liked_songs_folder, liked_songs_json, key='tracks')
    save_missing_songs(missing_liked_songs, liked_songs_folder)
    
    # Find missing songs for get_it_playlist
    missing_get_it_songs = find_missing_songs(get_it_playlist_folder, get_it_playlist_json, key='playlists')
    save_missing_songs(missing_get_it_songs, get_it_playlist_folder)

# Run the script
if __name__ == "__main__":
    process_folders_and_jsons()


