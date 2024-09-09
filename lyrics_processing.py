import os
from json_utils import save_json
from file_utils import file_exists

def collect_missing_songs(json_data, folder_path):
    """Collect songs from the JSON data that are not yet processed and save missing ones in a JSON file."""
    missing_songs = []

    # Iterate through each song in the JSON data
    for song in json_data:
        artist = song.get('artist')
        album = song.get('album')
        title = song.get('track')

        # Check if the file exists
        if not file_exists(folder_path, artist, album, title, 'txt'):
            missing_songs.append({
                'artist': artist,
                'album': album,
                'track': title
            })

    # Save missing songs to a JSON file
    save_json(missing_songs, os.path.join(folder_path, "missing_songs.json"))

    print(f"Missing songs saved to: {folder_path}/missing_songs.json")

def check_missing_songs(json_file_path, folder_name):
    """Main function to load JSON and check for missing songs."""
    folder_path = os.path.join("lyrics", folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Load the JSON data from the file
    from json_utils import load_json
    json_data = load_json(json_file_path)

    # Collect and save missing songs
    collect_missing_songs(json_data, folder_path)
