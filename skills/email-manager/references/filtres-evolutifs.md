# Filtres évolutifs - Liste des expéditeurs filtrés

Ce fichier est automatiquement mis à jour lors des scans d'emails quand l'utilisateur accepte de filtrer un expéditeur.

## Format

```
- `expéditeur@domaine.com` - Raison du filtre - Action - Date d'ajout
```

## Expéditeurs à archiver automatiquement

- `tuifly@emails.tuifly.be` - Newsletter promotionnelle non souhaitée (utilisateur désinscrit) - Archiver - 2025-11-14
- `tommyhilfiger@e.tommy.com` - Newsletter promotionnelle non souhaitée (utilisateur désinscrit) - Archiver - 2025-11-14

<!-- Les nouveaux filtres seront ajoutés ci-dessous automatiquement -->

## Expéditeurs à supprimer automatiquement

*Aucun filtre de suppression pour le moment.*

<!-- Les nouveaux filtres de suppression seront ajoutés ci-dessous automatiquement -->

## Instructions pour mise à jour

Lors de l'ajout d'un nouveau filtre :

1. Déterminer la catégorie (archiver ou supprimer)
2. Ajouter une ligne avec le format :
   ```
   - `expéditeur@exemple.com` - [Raison] - [Archiver/Supprimer] - [Date YYYY-MM-DD]
   ```
3. Exemple :
   ```
   - `newsletter@marketing.com` - Newsletter jamais ouverte - Archiver - 2025-01-10
   - `spam@promo.com` - Spam récurrent - Supprimer - 2025-01-10
   ```

## Historique des modifications

### 2025-11-14
- Ajout de `tuifly@emails.tuifly.be` - Newsletter TUI fly (utilisateur désinscrit)
- Ajout de `tommyhilfiger@e.tommy.com` - Newsletter Tommy Hilfiger (utilisateur désinscrit)

---
