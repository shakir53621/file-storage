import hashlib
from abc import ABC, abstractmethod


class AbstractHasher(ABC):
    @abstractmethod
    def hash_str(self, string: str) -> str:
        raise NotImplementedError


class MD5Hasher(AbstractHasher):
    def hash_str(self, string: str) -> str:
        return hashlib.md5(string.encode('utf-8')).hexdigest()


class SHA256Hasher(AbstractHasher):
    def hash_str(self, string: str) -> str:
        return hashlib.sha256(string.encode('utf-8')).hexdigest()


class SHA1Hasher(AbstractHasher):
    def hash_str(self, string: str) -> str:
        return hashlib.sha1(string.encode('utf-8')).hexdigest()
