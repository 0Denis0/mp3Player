import os
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

from file_utils import sanitize_filename, file_exists
from YTtoMP3 import get_top_youtube_link, download_youtube_as_mp3

# Wrapper function for multiprocessing
def process_single_song(song, output_path):
    artist = song.get('artist')
    album = song.get('album')
    track = song.get('track')

    if not artist or not track:
        print("Missing artist or track name.")
        return False

    # Skip songs with lyrics already saved
    if file_exists(output_path, artist, album, track, 'mp3'):
        print(f"MP3 file for {track} by {artist} already exists.")
        return False

    # Sanitize file name
    output_name = f"{sanitize_filename(artist)}_{sanitize_filename(album)}_{sanitize_filename(track)}"
    
    # Use the artist and track for search terms
    search_terms = f'{track} by {artist} lyrics'
    youtube_url = get_top_youtube_link(search_terms)
    
    if youtube_url:
        download_youtube_as_mp3(youtube_url, output_path=output_path, output_name=output_name)
        return True
    else:
        print(f"No YouTube link found for {track} by {artist}")
        return False

# Helper function to avoid using lambda
def process_song_wrapper(args):
    return process_single_song(*args)

def process_songs_audio(song_list, output_path="audio/liked_songs", use_multiprocessing=False):
    os.makedirs(output_path, exist_ok=True)

    # If multiprocessing is enabled, use Pool
    if use_multiprocessing:
        num_workers = cpu_count()
        with Pool(processes=num_workers) as pool:
            song_args = [(song, output_path) for song in song_list]
            
            # Use pool.imap_unordered with tqdm for parallel processing with a progress bar
            results = list(tqdm(pool.imap_unordered(process_song_wrapper, song_args),
                                total=len(song_list), desc="Downloading songs", unit="song"))
    else:
        # Process songs sequentially with tqdm progress bar
        for song in tqdm(song_list, total=len(song_list), desc="Downloading songs", unit="song"):
            process_song_wrapper((song, output_path))





