from photodedup.domain.models import ImageFile
from photodedup.domain.services import find_exact_duplicates, group_by_size
from photodedup.infrastructure.hasher import compute_hash


class TestGroupBySize:
    def test_simple_group(self, tmp_path):
        files_data = [
            ("photo1.jpg", 1000),
            ("photo2.jpg", 1000),
            ("photo3.jpg", 2000),
            ("photo4.jpg", 3000),
        ]

        grouped_images = group_by_size(create_imagefile_list(files_data, tmp_path))

        assert len(grouped_images) == 1

    def test_no_group(self, tmp_path):
        files_data = [("photo1.jpg", 1000), ("photo2.jpg", 2000), ("photo3.jpg", 3000)]

        grouped_images = group_by_size(create_imagefile_list(files_data, tmp_path))

        assert len(grouped_images) == 0

    def test_all_same_size(self, tmp_path):
        files_data = [("photo1.jpg", 5000), ("photo2.jpg", 5000), ("photo3.jpg", 5000)]

        grouped_images = group_by_size(create_imagefile_list(files_data, tmp_path))

        assert len(grouped_images) == 1
        assert len(grouped_images[5000]) == 3


class TestFindExactDuplicates:
    def test_detect_doubles(self, tmp_path):
        files_data = [
            ("photo1.jpg", 1000),
            ("photo2.jpg", 1000),
            ("photo3.jpg", 2000),
        ]

        images = create_imagefile_list(files_data, tmp_path)
        duplicates = find_exact_duplicates(images, compute_hash)

        assert len(duplicates) == 1
        assert len(duplicates[0].imagefiles) == 2

    def test_no_doubles(self, tmp_path):
        files_data = [("photo1.jpg", b"1234A"), ("photo2.jpg", b"1234B"), ("photo3.jpg", b"1234C")]

        images = []
        for name, fbytes in files_data:
            path = tmp_path / name
            path.write_bytes(fbytes)
            images.append(ImageFile.from_path(path))

        duplicates = find_exact_duplicates(images, compute_hash)

        assert len(duplicates) == 0

    def test_multiple_groups(self, tmp_path):
        files_data = [
            ("photo1.jpg", b"1234A"),
            ("photo2.jpg", b"1234A"),
            ("photo3.jpg", b"1234B"),
            ("photo4.jpg", b"1234B"),
            ("photo5.jpg", b"1234B"),
            ("photo6.jpg", b"1234C"),
        ]

        images = []
        for name, fbytes in files_data:
            path = tmp_path / name
            path.write_bytes(fbytes)
            images.append(ImageFile.from_path(path))

        duplicates = find_exact_duplicates(images, compute_hash)

        assert len(duplicates) == 2
        assert len(duplicates[0].imagefiles) == 2
        assert len(duplicates[1].imagefiles) == 3


class TestDuplicateGroup:
    def test_duplicate_group_proprieties(self, tmp_path):
        size_mo = 5242880

        files_data = [
            ("photo1.jpg", b"A" * size_mo),
            ("photo2.jpg", b"A" * size_mo),
            ("photo3.jpg", b"A" * size_mo),
        ]

        images = []
        for name, fbytes in files_data:
            path = tmp_path / name
            path.write_bytes(fbytes)
            images.append(ImageFile.from_path(path))

        duplicates = find_exact_duplicates(images, compute_hash)

        assert duplicates[0].extra_files == 2
        assert duplicates[0].wasted_space == 10485760


def create_imagefile_list(data, tmp_path):
    images = []
    for name, size in data:
        path = tmp_path / name
        path.write_bytes(b"A" * size)
        images.append(ImageFile.from_path(path))

    return images
