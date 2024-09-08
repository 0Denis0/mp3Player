import json

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, file_path):
    """Save JSON data to a file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
