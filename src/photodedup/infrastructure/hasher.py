import hashlib
from pathlib import Path


def compute_partial_hash(path: Path, chunk_size: int = 4096) -> str:
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        sha256.update(f.read(chunk_size))
    return sha256.hexdigest()


def compute_hash(path: Path, chunk_size: int = 8192) -> str:
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            sha256.update(chunk)
    return sha256.hexdigest()
