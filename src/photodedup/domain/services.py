from collections import defaultdict

from photodedup.domain.models import DuplicateGroup


def group_by_size(imagefiles: list) -> dict:
    images_grouped_by_size = defaultdict(list)

    for image in imagefiles:
        images_grouped_by_size[image.size].append(image)
    return remove_singletons(images_grouped_by_size)


def remove_singletons(grouped_images: dict) -> dict:
    return {k: v for k, v in grouped_images.items() if len(v) > 1}


def find_exact_duplicates(images, hasher) -> list[DuplicateGroup]:
    result = []
    grouped_images_by_size = group_by_size(images)

    grouped_by_hash = defaultdict(list)
    for size, imagegroup in grouped_images_by_size.items():
        try:
            for image in imagegroup:
                hash = hasher(image.path)
                grouped_by_hash[hash].append(image)
        except OSError:
            continue

    for hash, group in grouped_by_hash.items():
        if len(group) >= 2:
            result.append(DuplicateGroup(hash, group, "exact"))

    return result
