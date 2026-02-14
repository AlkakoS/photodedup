import re

from photodedup.infrastructure.hasher import compute_hash, compute_partial_hash


class TestComputeHash:
    def test_same_content(self, tmp_path):
        file1 = tmp_path / "photo.jpg"
        file1.write_bytes(b"fake jpg")
        file2 = tmp_path / "photo(1).jpg"
        file2.write_bytes(b"fake jpg")

        assert compute_hash(file1) == compute_hash(file2)

    def test_different_content(self, tmp_path):
        file1 = tmp_path / "photo.jpg"
        file1.write_bytes(b"fake jpg")
        file2 = tmp_path / "photo(1).jpg"
        file2.write_bytes(b"fake 2 jpg")

        assert compute_hash(file1) != compute_hash(file2)

    def test_calc_hash_size(self, tmp_path):
        file = tmp_path / "photo.jpg"
        file.write_bytes(b"fake jpg")

        regex = "^[a-fA-F0-9]+$"

        assert len(compute_hash(file)) == 64
        assert re.match(regex, compute_hash(file))

    def test_empty_folder(self, tmp_path):
        file = tmp_path / "photo.jpg"
        file.write_bytes(b"")
        file2 = tmp_path / "photo.jpg"
        file2.write_bytes(b"")

        assert len(compute_hash(file)) == 64
        assert compute_hash(file) == compute_hash(file2)


class TestPartialComputeHash:
    def test_partial_vs_complete_hash(self, tmp_path):
        file1 = tmp_path / "photo.jpg"
        file1.write_bytes(b"A" * 4096 + b"987")

        file2 = tmp_path / "photo2.jpg"
        file2.write_bytes(b"A" * 4096 + b"123")

        assert compute_partial_hash(file1) == compute_partial_hash(file2)
        assert compute_hash(file1) != compute_hash(file2)
