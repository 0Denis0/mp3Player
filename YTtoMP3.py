import yt_dlp
from youtube_search import YoutubeSearch

def download_youtube_as_mp3(url, output_path="downloads", ffmpeg_location="C:/ffmpeg/bin/ffmpeg.exe"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'ffmpeg_location': ffmpeg_location,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    download_youtube_as_mp3("https://www.youtube.com/watch?v=M8j0v4L7qpU")
