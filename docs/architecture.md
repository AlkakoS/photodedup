## Couches

### Domain (`src/photoclean/domain/`)
- Logique métier pure
- Zéro dépendance externe
- Modèles : ImageFile, DuplicateGroup, SimilarGroup

### Application (`src/photoclean/application/`)
- Cas d'usage (orchestration)
- Connecte le domain et l'infrastructure

### Infrastructure (`src/photoclean/infrastructure/`)
- Implémentations concrètes : scanner, hasher, BDD, corbeille
- Peut être remplacé sans toucher au domain

### UI (`src/photoclean/ui/`)
- Interface PySide6 (Qt 6)
- Pages, widgets, workers (threads)
- Styles QSS (thème clair/sombre)

## Principe clé

Le domain ne dépend de RIEN d'autre. Les flèches de dépendance pointent
toujours vers le domain, jamais dans l'autre sens.