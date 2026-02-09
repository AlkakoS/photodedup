from pathlib import Path

from photodedup.domain.models import ImageFile, is_image_extension

IGNORED_FOLDERS = frozenset({"_", ".", "node_modules"})


def validate_scan_root(path: Path) -> None:
    """
    Valide le dossier racine à scanner.

    Vérifie que le chemin existe, qu'il pointe vers un dossier, et qu'il n'est
    pas explicitement listé comme dossier à ignorer.

    Args:
        path: Chemin du dossier racine à scanner.

    Raises:
        FileNotFoundError: Si le chemin n'existe pas.
        NotADirectoryError: Si le chemin n'est pas un dossier.
        ValueError: Si le dossier racine fait partie des dossiers ignorés.
    """
    if not path.exists():
        raise FileNotFoundError(f"Le chemin '{path}' n'existe pas.")

    if not path.is_dir():
        raise NotADirectoryError(f"'{path.name}' n'est pas un dossier")

    if is_ignored_dirname(path.name):
        raise ValueError(f"Dossier ignoré: {path}")


def is_ignored_dirname(name: str) -> bool:
    """
    Indique si un nom de dossier doit être ignoré.

    Règle:
        Le dossier est ignoré si son nom commence par l'un des préfixes définis
        dans IGNORED_FOLDERS.

    Args:
        name: Nom du dossier (ex: "photos", "node_modules", ".git", "__pycache__").

    Returns:
        True si le dossier doit être ignoré, sinon False.
    """
    return name.startswith(tuple(IGNORED_FOLDERS))


def should_scan_file(root: Path, file: Path) -> bool:
    """
    Détermine si un chemin trouvé pendant le scan doit être traité comme une image.

    Le fichier est rejeté si :
      - un segment de son chemin relatif (par rapport à root) correspond à un dossier ignoré,
      - c'est un dossier,
      - c'est un lien symbolique,
      - son extension ne correspond pas à une image.

    Args:
        root: Dossier racine du scan (celui passé à scan_directory).
        file: Chemin candidat renvoyé par rglob.

    Returns:
        True si le fichier doit être scanné, sinon False.
    """
    rel_parts = file.relative_to(root).parts
    if any(is_ignored_dirname(part) for part in rel_parts):
        return False

    if file.is_dir() or file.is_symlink():
        return False

    return is_image_extension(file)


def scan_directory(path: Path):
    """
    Scanne récursivement un dossier et construit une liste d'ImageFile valides.

    Cette fonction :
      1) valide le dossier racine,
      2) parcourt tous les chemins via rglob("*"),
      3) filtre les chemins non pertinents (dossiers ignorés, dossiers, symlinks, non-images),
      4) crée des ImageFile avec ImageFile.from_path,
      5) collecte les erreurs d'accès (PermissionError/OSError) sous forme de messages.

    Args:
        path: Dossier racine à scanner.

    Returns:
        Un tuple (images, errors) où :
          - images : liste d'ImageFile créés avec succès,
          - errors : liste de messages d'erreur (str) pour les fichiers non lisibles.
    """
    validate_scan_root(path)

    images, errors = [], []
    for file in path.rglob("*"):
        if not should_scan_file(path, file):
            continue

        try:
            images.append(ImageFile.from_path(file))
        except (PermissionError, OSError) as e:
            errors.append(f"{file}: {e}")

    return images, errors
