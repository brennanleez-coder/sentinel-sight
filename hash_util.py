import hashlib

apk_directory = "../extractedApks/"
file_name = 'base.apk'

def compute_sha256(apk_file_path):
    hash_sha256 = hashlib.sha256()
    with open(apk_file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


# print(compute_sha256(file_path))