import hashlib
import os

# Compute the SHA256 hash of a file
def compute_sha256_from_apk(apk_file_path):
    hash_sha256 = hashlib.sha256()
    with open(apk_file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()




