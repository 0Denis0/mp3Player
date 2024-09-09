import json
import file_utils

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, file_path):
    """Save JSON data to a file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def filter_missing_files(json_list, folder_path, extension="txt"):
    """
    Filter out the elements in the json_list that already have a corresponding file in the folder.
    
    Args:
    - json_list: The loaded list of JSON elements (dictionaries with artist, album, and track).
    - folder_path: The path to the folder where files are stored.
    - extension: The file extension to check (default is 'txt').
    
    Returns:
    - A list of elements from the json_list that don't have a corresponding file in the folder.
    """
    missing_files = []

    for song in json_list:
        artist = song.get('artist')
        album = song.get('album')
        title = song.get('track')

        if not file_utils.file_exists(folder_path, artist, album, title, extension):
            missing_files.append(song)

    return missing_files

if __name__ == '__main__':
    liked_songs_json = "my_spotify_data/Spotify Account Data/YourLibrary.json"
    with open(liked_songs_json, 'r', encoding='utf-8') as f:
                library_data = json.load(f)
                liked_songs = library_data.get('tracks', [])

    missing_songs = filter_missing_files(liked_songs, "audio/liked_songs", extension='mp3')
    print(len(missing_songs))
