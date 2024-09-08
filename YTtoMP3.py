import yt_dlp
from youtube_search import YoutubeSearch

def download_youtube_as_mp3(url, output_path="downloads", output_name="default", ffmpeg_location="C:/ffmpeg/bin/ffmpeg.exe"):
    
    if output_name == "default":
        tmpl = f'{output_path}/%(title)s.%(ext)s'
    else:
        tmpl = f'{output_path}/{output_name}'

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': tmpl,
        'ffmpeg_location': ffmpeg_location,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def get_top_youtube_link(search_terms):
    try:
        # Perform the search
        results = YoutubeSearch(search_terms=search_terms, max_results=1).to_dict()
        
        if results:
            # Extract video ID of the top result
            video_id = results[0]['id']
            yt_prefix = 'https://www.youtube.com/watch?v='
            # Form the complete YouTube link
            return f'{yt_prefix}{video_id}'
        else:
            return "No results found."
    
    except Exception as e:
        return f"Error occurred: {str(e)}"


if __name__ == "__main__":
    search_terms = 'Closer by Big Baby Tape, Aarne lyrics'
    top_link = get_top_youtube_link(search_terms)
    download_youtube_as_mp3("https://www.youtube.com/watch?v=M8j0v4L7qpU")
