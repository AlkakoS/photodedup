from collections import defaultdict
from pathlib import Path
from typing import Callable

from photodedup.domain.models import DuplicateGroup, ImageFile


def group_by_size(imagefiles: list[ImageFile]) -> dict[int, list[ImageFile]]:
    images_grouped_by_size = defaultdict(list)

    for image in imagefiles:
        images_grouped_by_size[image.size].append(image)
    return remove_singletons(images_grouped_by_size)


def remove_singletons(grouped_images: dict) -> dict:
    return {k: v for k, v in grouped_images.items() if len(v) > 1}


def find_exact_duplicates(images, hasher: Callable[[Path], str]) -> list[DuplicateGroup]:
    result = []
    grouped_images_by_size = group_by_size(images)

    grouped_by_hash = defaultdict(list)
    for size, imagegroup in grouped_images_by_size.items():
        for image in imagegroup:
            try:
                h = hasher(image.path)
                grouped_by_hash[h].append(image)
            except OSError:
                continue

    for hash, group in grouped_by_hash.items():
        if len(group) >= 2:
            result.append(DuplicateGroup(hash, group, "exact"))

    return result
