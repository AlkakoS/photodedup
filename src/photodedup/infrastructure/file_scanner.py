from pathlib import Path

from photodedup.domain.models import ImageFile, is_image_extension

IGNORED_FOLDERS = frozenset({"_", ".", "node_modules"})


def is_ignored_dirname(name: str) -> bool:
    return name.startswith(tuple(IGNORED_FOLDERS))


def should_scan_file(file: Path) -> bool:
    if file.is_dir() or file.is_symlink():
        return False

    return is_image_extension(file)


def format_scan_error(error: OSError, source: str) -> str:
    location = error.filename or "inconnu"

    if isinstance(error, PermissionError):
        return f"{source} - Permission refusée : {location}"
    elif isinstance(error, FileNotFoundError):
        return f"{source} introuvable : {location}"
    elif isinstance(error, NotADirectoryError):
        return f"{location} n'est pas un dossier."
    else:
        return f"{source} - Erreur d'accès : {location} ({error.strerror})"


def scan_directory(path: Path):
    if is_ignored_dirname(path.name):
        raise ValueError(f"Le dossier {path.name} ne peut pas être scanné.")

    images, errors, skipped_folders, skipped_files = [], [], [], []

    def handle_error(e: OSError) -> None:
        errors.append(format_scan_error(e, source="Dossier"))

    try:
        for dirpath, dirnames, filenames in path.walk(on_error=handle_error):
            skipped_folders.extend(dirpath / d for d in dirnames if is_ignored_dirname(d))
            dirnames[:] = [d for d in dirnames if not is_ignored_dirname(d)]

            for filename in filenames:
                file_path = dirpath / filename

                if not should_scan_file(file_path):
                    skipped_files.append(file_path)
                    continue

                try:
                    images.append(ImageFile.from_path(file_path))
                except OSError as e:
                    errors.append(format_scan_error(e, source="Fichier"))
    except OSError as e:
        errors.append(format_scan_error(e, source="Dossier"))

    return images, errors, skipped_folders, skipped_files
