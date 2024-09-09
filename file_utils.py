import os

def sanitize_filename(filename):
    """Sanitize a string to be used as a valid file name."""
    return ''.join(c for c in filename if c not in r'<>:"/\|?*').strip()

def file_exists(folder_path, artist, album, title, extension):
    """Check if the sanitized song file exists in the folder."""
    sanitized_filename = f"{sanitize_filename(artist)}_{sanitize_filename(album)}_{sanitize_filename(title)}.{extension}"
    return os.path.exists(os.path.join(folder_path, sanitized_filename))