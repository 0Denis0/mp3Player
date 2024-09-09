import json
import time

import json_utils
from mp3_processing import process_songs_audio
from lyrics_processing import check_missing_songs

if __name__ == "__main__":
    # Path to the JSON files
    liked_songs_json = "my_spotify_data/Spotify Account Data/YourLibrary.json"
    get_it_playlist_json = "my_spotify_data/Spotify Account Data/Playlist1.json"

    # # Check for missing songs in liked songs
    # check_missing_songs(liked_songs_json, 'liked_songs')

    # # Check for missing songs in the get it playlist
    # check_missing_songs(get_it_playlist_json, 'get_it_playlist')

    while True:
        try:
            # Load liked songs and process them
            with open(liked_songs_json, 'r', encoding='utf-8') as f:
                library_data = json.load(f)
                liked_songs = library_data.get('tracks', [])
            
            liked_path = "audio/liked_songs"
            liked_songs = json_utils.filter_missing_files(liked_songs,  liked_path, extension='mp3')
            process_songs_audio(liked_songs, output_path=liked_path)

            with open(get_it_playlist_json, 'r', encoding='utf-8') as f:
                playlist_data = json.load(f)
                get_it_playlist = next((p for p in playlist_data.get('playlists', []) if p.get('name') == "get it"), None)
                if get_it_playlist:
                    get_it_songs = get_it_playlist.get('items', [])
                    
            get_it_path = "audio/get_it"
            get_it_songs = json_utils.filter_missing_files(get_it_songs, get_it_path, extension='mp3')
            process_songs_audio(get_it_songs, output_path=get_it_path)

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Waiting for 30 minutes before retrying...")
            time.sleep(1800)  # Wait for 30 minutes (1800 seconds)
