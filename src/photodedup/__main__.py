import sys
from pathlib import Path
from time import perf_counter

from photodedup.infrastructure.file_scanner import scan_directory


def main() -> int:
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print("Erreur : Chemin du dossier manquant")
        print("Usage : python -m photodedup.main <chemin_dossier>")
        return 1

    args_str = sys.argv[1]
    path = Path(args_str)

    print(f"📂 Scan de : {path.name}")
    print("⏳ Scan en cours...\n")

    start = perf_counter()
    try:
        images, errors, skipped_folders, skipped_files = scan_directory(path)
    except FileNotFoundError as e:
        print(f"\nErreur : {e}")
        return 1
    except NotADirectoryError as e:
        print(f"\nErreur : {e}")
        return 1
    except ValueError as e:
        print(f"\nErreur : {e}")
        return 1

    end = perf_counter()
    count_time = end - start

    print(f"✅ Scan terminé en {count_time:.2f}s\n")
    print(f"📊 Résumé:\n - Images trouvées : {len(images)}\n - Erreurs : {len(errors)}\n")

    print_list_section("Images", images, "Aucune image.", "images")
    print()
    print_list_section("Erreurs", errors, "Aucune erreur.", "errors")
    print()
    print_list_section(
        "Dossiers ignorés", skipped_folders, "Aucun dossier ignoré.", "skipped_folders"
    )
    print()
    print_list_section("Fichiers ignorés", skipped_files, "Aucun fichier ignoré.", "skipped_files")

    return 0


def print_list_section(title, items, message, kind):
    if title == "Images":
        print(f"📋 {title} :")
    else:
        print(f"⚠️  {title} :")

    if len(items) == 0:
        print(message)
    else:
        limit_display(items, kind)


def limit_display(items, label):
    match label:
        case "images":
            display_setup(items, display_message_images, "images.")
        case "errors":
            display_setup(items, display_message_autres, "erreurs.")
        case "skipped_folders":
            display_setup(items, display_message_autres, "dossiers ignorés.")
        case _:
            display_setup(items, display_message_autres, "fichiers ignorés.")


def display_setup(items, display_messages, message):
    if len(items) >= 20:
        for count, item in enumerate(items[:10], start=1):
            display_messages(count, item)
        print(f"... et {len(items) - 10} autres {message}")
    else:
        for count, item in enumerate(items, start=1):
            display_messages(count, item)


def display_message_images(count, item):
    print(f" {count}. {item.path}, {item.size}, {item.modified_at}")


def display_message_autres(count, item):
    print(f" {count}. {item}")


if __name__ == "__main__":
    raise SystemExit(main())
