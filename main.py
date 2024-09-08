from YTtoMP3 import get_top_youtube_link, download_youtube_as_mp3
from song_processing import check_missing_songs

if __name__ == "__main__":
    # Path to the JSON files
    liked_songs_json = 'path/to/YourLibrary.json'
    get_it_playlist_json = 'path/to/Playlist1.json'

    # Check for missing songs in liked songs
    check_missing_songs(liked_songs_json, 'liked_songs')

    # Check for missing songs in the get it playlist
    check_missing_songs(get_it_playlist_json, 'get_it_playlist')
