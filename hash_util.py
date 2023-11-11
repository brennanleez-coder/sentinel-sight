import hashlib

apk_directory = "../extractedApks/"
file_name = 'base.apk'

def compute_sha256(apk_name):
    file_path = apk_directory + file_name
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


# print(compute_sha256(file_path))