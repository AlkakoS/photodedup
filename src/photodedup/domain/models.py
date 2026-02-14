"""Modèles du domaine PhotoDeup

Ce module contient les structures de données fondamentales de l'application.
Ces classes représentent les concepts métier et n'ont aucune dépendance externe.

Contenu:
    - SUPPORTED_EXTENSIONS: ensemble immuable des extensions d'images supportées.
    - ImageFile: représentation d'un fichier image sur le disque (path, size, modified_at).
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Extensions d'images supportés par PhotoDedup
SUPPORTED_EXTENSIONS = frozenset(
    {".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".tiff", ".tif", ".bmp", ".svg"}
)


@dataclass
class ImageFile:
    """Représente un fichier image sur le disque.

    Attributes:
        path: Chemin absolu vers le fichier image.
        size: Taille du fichier en octets.
        modified_at: Date de dernière modification.
    """

    path: Path
    size: int
    modified_at: datetime

    @property
    def filename(self) -> str:
        """Nom du fichier (ex: 'chat.jpg')."""
        return self.path.name

    @property
    def extension(self) -> str:
        """Extension en minuscule (ex: '.jpg')."""
        return self.path.suffix.lower()

    @property
    def size_human(self) -> str:
        """Taille lisible (ex: '2.4 Mo')."""
        if self.size < 1024:
            return f"{self.size} o"
        elif self.size < 1024**2:
            return f"{self.size / 1024:.1f} Ko"
        elif self.size < 1024**3:
            return f"{self.size / 1024**2:.1f} Mo"
        else:
            return f"{self.size / 1024**3:.1f} Go"

    def is_supported(self) -> bool:
        """Vérifie si l'extension est supporté."""
        return self.extension in SUPPORTED_EXTENSIONS

    @classmethod
    def from_path(cls, path: Path) -> "ImageFile":
        stat = path.stat()
        return cls(path=path, size=stat.st_size, modified_at=datetime.fromtimestamp(stat.st_mtime))


def is_image_extension(path: Path) -> bool:
    """Vérifie si un chemin pointe vers un fichier image supporté."""
    return path.suffix.lower() in SUPPORTED_EXTENSIONS


@dataclass
class DuplicateGroup:
    hash: str
    imagefiles: list
    detection: str

    @property
    def extra_files(self) -> int:
        return len(self.imagefiles) - 1

    @property
    def wasted_space(self) -> int:
        return self.imagefiles[0].size * len(self.imagefiles)
