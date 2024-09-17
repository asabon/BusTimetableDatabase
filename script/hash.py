import os
import hashlib

def hash_file(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(4096), b''):
            sha256.update(block)
    return sha256.hexdigest()

def hash_directory(directory_path):
    """Calculate a combined hash for all text files in a directory."""
    sha256 = hashlib.sha256()
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                file_hash = hash_file(file_path)
                sha256.update(file_hash.encode())
    return sha256.hexdigest()
