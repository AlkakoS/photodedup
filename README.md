# PhotoDedup

Détecteur intelligent de doublons photos et de photos indentiques (ex. rafales) - **desktop**, **local** et **privé**.

> Projet en cours de développement

## Description

PhotoDedup scanne une bibliothèque de photos (dossier choisi), détecte :
- les **doublons exacts** (copies identiques),
- les **images similaires** (recadrage, recompression, rafales),
puis vous permet de les **envoyer à la corbeille** (par défaut) ou de les **supprimer définitivement** (option avancée) pour libérer de l’espace disque.

## Tech Stack

- **python 3.12.3**
- **PySide6 (Qt 6)** - Interface desktop native
- **SQLite** - Base de données locale
- **CLIP + FAISS** - Détection par IA (optionnel selon capacités machine)

## Statut

- [ ] v0.1.0 — Scanner de fichiers
- [ ] v0.2.0 — Détection doublons exacts
- [ ] v0.3.0 — Base de données
- [ ] v0.4.0 — Interface desktop
- [ ] v0.5.0 — Affichage + suppression
- [ ] v0.6.0 — Hash perceptuel
- [ ] v0.7.0 — Détection IA (CLIP)
- [ ] v0.8.0 — Recherche vectorielle (FAISS)
- [ ] v1.0.0 — Release publique

## License

MIT