"""Tests pour les modèles du domaine."""

from datetime import datetime
from pathlib import Path

from photodedup.domain.models import ImageFile, is_image_extension


class TestImageFile:
    """Tests pour la classe ImageFile."""

    def _make_image(self, name: str = "photo.jpg", size: int = 1024) -> ImageFile:
        """Helper: créer une ImageFile de test rapidement."""
        return ImageFile(
            path=Path(f"/fake/path/{name}"), size=size, modified_at=datetime(2026, 1, 15, 10, 30, 0)
        )

    def test_filename(self):
        img = self._make_image("vacances.jpg")
        assert img.filename == "vacances.jpg"

    def test_extension_minuscule(self):
        img = self._make_image("photo.jpg")
        assert img.extension == ".jpg"

    def test_extension_majuscule_convertie(self):
        img = self._make_image("photo.JPG")
        assert img.extension == ".jpg"

    def test_size_human_octets(self):
        img = self._make_image(size=500)
        assert img.size_human == "500 o"

    def test_size_human_ko(self):
        img = self._make_image(size=2048)
        assert img.size_human == "2.0 Ko"

    def test_size_human_mo(self):
        img = self._make_image(size=5 * 1024**2)
        assert img.size_human == "5.0 Mo"

    def test_size_human_go(self):
        img = self._make_image(size=2 * 1024**3)
        assert img.size_human == "2.0 Go"

    def test_is_supported_jpg(self):
        img = self._make_image("screenshot.jpg")
        assert img.is_supported() is True

    def test_is_supported_pdf(self):
        img = self._make_image("document.pdf")
        assert img.is_supported() is False

    def test_is_supported_txt(self):
        img = self._make_image("notes.txt")
        assert img.is_supported() is False


class TestIsImageExtension:
    """Tests pour la fonction is_image_extension."""

    def test_jpg(self):
        assert is_image_extension(Path("photo.jpg")) is True

    def test_jpeg(self):
        assert is_image_extension(Path("photo.jpeg")) is True

    def test_png(self):
        assert is_image_extension(Path("photo.png")) is True

    def test_gif(self):
        assert is_image_extension(Path("anim.gif")) is True

    def test_webp(self):
        assert is_image_extension(Path("photo.webp")) is True

    def test_pdf_not_image(self):
        assert is_image_extension(Path("doc.pdf")) is False

    def test_mp4_not_image(self):
        assert is_image_extension(Path("video.mp4")) is False

    def test_no_extension(self):
        assert is_image_extension(Path("fichier_sans_extension")) is False

    def test_majuscule(self):
        """L'extension en majuscule doit être reconnue."""
        assert is_image_extension(Path("photo.PNG")) is True
