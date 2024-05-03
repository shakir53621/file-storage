import hashlib


class FileHasher:
    def __init__(self, filename: str):
        self.filename = filename

    def create_hash(self):
        return hashlib.md5(self.filename.encode()).hexdigest()
