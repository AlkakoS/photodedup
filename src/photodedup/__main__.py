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

    start = perf_counter()
    try:
        images, errors = scan_directory(path)
    except FileNotFoundError as e:
        print(f"\nErreur : {e}")
        return 1
    except NotADirectoryError as e:
        print(f"\nErreur : {e}")
        return 1
    except ValueError as e:
        print(f"\nErreur : {e}")
        return 1

    print("⏳ Scan en cours...\n")

    end = perf_counter()
    count_time = end - start

    print(f"✅ Scan terminé en {count_time:.2f}s\n")
    print(f"📊 Résumé:\n - Images trouvées : {len(images)}\n - Erreurs : {len(errors)}\n")
    print("📋 Images :")

    if len(images) <= 20:
        for count, img in enumerate(images, start=1):
            print(f" {count}. {img.path}, {img.size}, {img.modified_at}")
    else:
        for count, img in enumerate(images[:10], start=1):
            print(f" {count}. {img.path}, {img.size}, {img.modified_at}")
        print(f"... et {len(images) - 10} autres images")

    print("⚠️  Erreurs :")
    if len(errors) == 0:
        print("Aucune erreur")
    else:
        for count, err in enumerate(errors, start=1):
            print(f" {count}. {err}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
