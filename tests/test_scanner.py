"""Tests pour le scanner de dossiers."""

import pytest

from photodedup.infrastructure.file_scanner import (
    is_ignored_dirname,
    scan_directory,
    validate_scan_root,
)


class TestScanDirectory:
    """Tests pour la fonction scan_diretory."""

    def test_scan_trouve_images_basiques(self, tmp_path):
        (tmp_path / "photo.jpg").write_bytes(b"fake jpg data")
        (tmp_path / "image.png").write_bytes(b"fake png data")

        sous_dossier = tmp_path / "sub"
        sous_dossier.mkdir()
        (sous_dossier / "deep.gif").write_bytes(b"fake gif data")

        images, errors = scan_directory(tmp_path)

        assert len(images) == 3
        assert len(errors) == 0

        noms_fichiers = {img.filename for img in images}
        assert noms_fichiers == {"photo.jpg", "image.png", "deep.gif"}

    def test_scan_ignore_non_images(self, tmp_path):
        """Le scanner doit ignorer les PDF, TXT, MP4, etc."""

        (tmp_path / "photo.jpg").write_bytes(b"fake jpg data")
        (tmp_path / "document.pdf").write_bytes(b"pdf content")
        (tmp_path / "notes.txt").write_bytes(b"text content")
        (tmp_path / "video.mp4").write_bytes(b"video content")

        images, errors = scan_directory(tmp_path)

        assert len(images) == 1
        assert images[0].filename == "photo.jpg"
        assert len(errors) == 0

    def test_scan_ignore_dossiers_caches(self, tmp_path):
        """Les dossiers cachés doivent être ignorés."""

        (tmp_path / "visible.jpg").write_bytes(b"fake jpg data")

        dossier_cache = tmp_path / ".hidden"
        dossier_cache.mkdir()
        (dossier_cache / "secret.jpg").write_bytes(b"secret image")

        images, errors = scan_directory(tmp_path)

        assert len(images) == 1
        assert images[0].filename == "visible.jpg"

        chemins = [img.path for img in images]
        assert not any(".hidden" in str(chemin) for chemin in chemins)

    def test_scan_ignore_dossiers_systeme(self, tmp_path):
        """Les dossiers systéme doivent être ignorés"""

        (tmp_path / "photo.jpg").write_bytes(b"normal image")

        pycache = tmp_path / "__pycache__"
        pycache.mkdir()
        (pycache / "cached.png").write_bytes(b"cached images")

        images, errors = scan_directory(tmp_path)

        assert len(images) == 1
        assert images[0].filename == "photo.jpg"

    def test_scan_dossier_inexistant(self, tmp_path):
        """Scanner un dossier inexistant doir lever FileNotFoundError."""

        dossier_faux = tmp_path / "nexiste_pas"

        with pytest.raises(FileNotFoundError) as err_info:
            scan_directory(dossier_faux)

        assert f"Le chemin '{dossier_faux}' n'existe pas." in str(err_info.value)

    def test_scan_fichier_pas_dossier(self, tmp_path):
        """Scanner un fichier doit lever NotADirectoryError."""

        fichier = tmp_path / "photo.jpg"
        fichier.write_bytes(b"images data")

        with pytest.raises(NotADirectoryError) as err_info:
            scan_directory(fichier)

        assert f"'{fichier.name}' n'est pas un dossier." in str(err_info.value)

    def test_scan_dossier_vide(self, tmp_path):
        """Un dossier vide ne doit pas causer d'erreur."""

        images, errors = scan_directory(tmp_path)

        assert len(images) == 0
        assert len(errors) == 0

    def test_scan_extensions_majuscules(self, tmp_path):
        """Les extensions en majuscules doivent être reconnues."""

        (tmp_path / "photo.JPG").write_bytes(b"jpg uppercase")
        (tmp_path / "image.Png").write_bytes(b"png mixed case")
        (tmp_path / "gif.GIF").write_bytes(b"gif uppercase")

        images, errors = scan_directory(tmp_path)

        assert len(images) == 3

        extensions = {img.extension for img in images}
        assert extensions == {".jpg", ".png", ".gif"}

    def test_scan_metadonnees_correctes(self, tmp_path):
        """Les ImageFile créés doivent avoir les métadonnées correctes."""

        fichier = tmp_path / "test.jpg"
        contenu = b"X" * 100
        fichier.write_bytes(contenu)

        images, errors = scan_directory(tmp_path)

        assert len(images) == 1

        img = images[0]

        assert img.path == fichier
        assert img.size == 100

        from datetime import datetime

        assert isinstance(img.modified_at, datetime)
        assert img.modified_at is not None

        now = datetime.now()
        age_seconds = (now - img.modified_at).total_seconds()
        assert age_seconds < 60

    def test_scan_ignored_dirname(self, tmp_path):
        """Scanner un dossier inclus dans IGNORED_FOLDERS doit lever ValueError."""

        dossier = tmp_path / "_dossier"
        dossier.mkdir()

        with pytest.raises(ValueError) as err_info:
            scan_directory(dossier)

        assert f"Dossier ignoré: {dossier}" in str(err_info.value)


class TestIsIgnoredDirname:
    """Tests pour is_ignored_dirname."""

    def test_dossier_cache(self):
        assert is_ignored_dirname(".git") is True
        assert is_ignored_dirname(".hidden") is True

    def test_dossier_underscore(self):
        assert is_ignored_dirname("__pycache__") is True
        assert is_ignored_dirname("_build") is True

    def test_node_modules(self):
        assert is_ignored_dirname("node_modules") is True

    def test_dossier_normal(self):
        assert is_ignored_dirname("photos") is False
        assert is_ignored_dirname("Images") is False


class TestValidateScanRoot:
    """Tests pour validate_scan_root."""

    def test_dossier_valide(self, tmp_path):
        validate_scan_root(tmp_path)

    def test_chemin_inexistant(self, tmp_path):
        faux = tmp_path / "nexiste_pas"
        with pytest.raises(FileNotFoundError):
            validate_scan_root(faux)

    def test_pas_un_dossier(self, tmp_path):
        fichier = tmp_path / "test.txt"
        fichier.write_text("test")
        with pytest.raises(NotADirectoryError):
            validate_scan_root(fichier)

    def test_dossier_ignore(self, tmp_path):
        cache = tmp_path / ".git"
        cache.mkdir()
        with pytest.raises(ValueError) as exc_info:
            validate_scan_root(cache)
        assert "ignoré" in str(exc_info.value)
