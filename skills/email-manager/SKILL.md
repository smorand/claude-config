---
name: email-manager
description: Gestionnaire d'emails Gmail PERSONNELS en français pour scanner, trier et archiver automatiquement les emails de l'INBOX selon des règles prédéfinies. **Utiliser pour TOUS les emails personnels (envoyer, lire, trier).** Utiliser quand l'utilisateur demande de "scanner les emails", "trier mes emails", "gérer ma boîte mail", "envoyer un email", "envoyer un mail" (sans préciser "professionnel"), ou toute tâche de gestion d'emails. Scanne UNIQUEMENT l'INBOX et déplace les emails vers les labels appropriés (personal/ecole, personal/voyage, personal/commandes, personal/Maison, pro/L'Oréal). **Note: Pour les emails professionnels L'Oréal, utiliser o365-manager.**
---

# Email Manager

Skill de gestion automatisée des emails Gmail en français.

## Outils disponibles

### CLI Go - email-manager
Un outil en ligne de commande moderne en Go pour les opérations courantes :
- **Installation** : `cd ~/projects/new/email-manager && make install`
- **Binaire** : `email-manager` (installé dans `/usr/local/bin`)
- **Commandes disponibles** :
  - `send` - Envoyer des emails
  - `list` - Lister les messages
  - `get` - Obtenir un message par ID
  - `search` - Rechercher des messages
  - `read` / `unread` - Marquer comme lu/non lu
  - `archive` - Archiver un message
  - `delete` - Supprimer un message
  - `download-attachments` - Télécharger les pièces jointes
  - `labels list/create/apply` - Gérer les labels

**Utiliser `email-manager` pour les opérations de téléchargement de pièces jointes et autres opérations basiques.**

### Scripts Python (legacy)
Les scripts Python dans `~/.claude/skills/email-manager/scripts/` restent disponibles pour les opérations avancées (tri automatique, gestion des brouillons, etc.).

## Objectif

Permettre un tri rapide et efficace des emails en scannant **par défaut l'INBOX**, en appliquant des règles prédéfinies pour archiver, labelliser ou marquer comme lu les emails selon leur type. Fournir un bilan concis des actions effectuées.

**⚠️ RÈGLE PAR DÉFAUT : Lors d'une demande de tri automatique ("trie mes emails", "scan les emails"), scanner UNIQUEMENT l'INBOX, jamais les autres labels (personal/ecole, personal/voyage, personal/commandes, personal/Maison, pro/L'Oréal) car ils contiennent des emails déjà traités. SAUF si l'utilisateur demande explicitement un autre label.**

## Quand utiliser cette skill

Utiliser cette skill quand l'utilisateur demande :
- "On scan les emails"
- "Trie mes emails"
- "Gère ma boîte mail"
- "Archive les emails non importants"
- Toute demande de gestion d'emails par lot

## Label à scanner

⚠️ **IMPORTANT : Scanner l'INBOX par défaut**

**Comportement par défaut :**
Lors d'une demande générale de tri ("trie mes emails", "scan les emails"), scanner **UNIQUEMENT l'INBOX**. Les emails déjà classés dans d'autres labels (personal/ecole, personal/voyage, personal/commandes, etc.) ne doivent **PAS** être re-triés ou re-scannés lors du tri automatique. Une fois qu'un email quitte l'INBOX et est archivé dans un label spécifique, il n'est plus touché par le processus de tri automatique.

**Exception :**
Si l'utilisateur demande explicitement de scanner un autre label (ex: "regarde mes emails personal/voyage", "scan personal/ecole"), alors scanner ce label spécifique.

**Label scanné :**
- **INBOX** - Boîte de réception principale

**Labels de destination** (où seront déplacés les emails de l'INBOX) :
- **personal/ecole** - Emails scolaires (Lycée Descartes, etc.)
- **personal/voyage** - Confirmations de voyage, billets, etc.
- **personal/commandes** - Confirmations de commandes en ligne
- **personal/Maison** - Services maison (Free, Netflix, Sosh, Disney+, Crunchyroll)
- **pro/L'Oréal** - Emails professionnels L'Oréal

## Processus de scan

### 1. Scanner le label approprié

**Par défaut : Scanner l'INBOX**

Utiliser le script `search_email` pour récupérer les emails de l'INBOX :

```bash
cd ~/.claude/skills/email-manager/scripts
./run.sh search_email --query "label:INBOX newer_than:7d" --max-results 100 --full
```

**Requêtes pour l'INBOX :**
- `label:INBOX` - Tous les emails de l'INBOX
- `label:INBOX is:unread` - Emails non lus dans l'INBOX uniquement
- `label:INBOX newer_than:7d` - Emails récents de l'INBOX (derniers 7 jours)

**Scanner un autre label si demandé explicitement :**

Si l'utilisateur demande un label spécifique (ex: "regarde personal/voyage"), utiliser :
```bash
./run.sh search_email --query "label:personal/voyage newer_than:7d" --max-results 100 --full
```

**Pendant le tri automatique** - ne PAS scanner les autres labels, ils contiennent des emails déjà traités.

### 2. Appliquer les règles de tri
Consulter `references/regles-tri.md` pour les règles détaillées par type d'email.

### 3. Actions disponibles

**Utiliser le CLI Go `email-manager` pour les actions basiques :**

#### Marquer comme lu
```bash
email-manager read "MESSAGE_ID"
```

#### Marquer comme non lu
```bash
email-manager unread "MESSAGE_ID"
```

#### Archiver (retirer de INBOX)
```bash
email-manager archive "MESSAGE_ID"
```

#### Ajouter un label
```bash
# D'abord lister les labels pour obtenir les IDs
email-manager labels list

# Ensuite ajouter le label (utiliser l'ID du label)
email-manager labels apply "MESSAGE_ID" "LABEL_ID"
```

#### Télécharger les pièces jointes (dans ~/Downloads)
```bash
# Télécharger toutes les pièces jointes dans ~/Downloads (par défaut)
email-manager download-attachments "MESSAGE_ID"

# Télécharger dans un répertoire spécifique
email-manager download-attachments "MESSAGE_ID" --dir "/path/to/dir"

# Télécharger dans le répertoire courant
email-manager download-attachments "MESSAGE_ID" --dir .
```

**Important :** Les pièces jointes sont toujours téléchargées dans `~/Downloads` par défaut. Le nouveau CLI Go `email-manager` remplace le script Python `download_attachment.py`.

#### Supprimer un message (mettre à la corbeille)
```bash
email-manager delete "MESSAGE_ID"
```

**Note:** Pour suppression définitive ou gestion spam avancée, utiliser les scripts Python.

**⚠️ Actions nécessitant confirmation utilisateur :**
- **Paiements à effectuer** : TOUJOURS demander avant d'archiver
- **Check-in vols** : TOUJOURS demander avant d'archiver
- **Modifications vols** : TOUJOURS demander avant d'archiver

### 4. Détecter listes de distribution et spam

**Identifier automatiquement :**
- Emails avec headers mailing list (`List-Unsubscribe`, `List-Id`, etc.)
- Présence de liens "unsubscribe" / "se désabonner"
- Emails récurrents non ouverts du même expéditeur

**Action :**
Proposer à l'utilisateur d'ouvrir le lien de désinscription et créer un filtre permanent.

### 5. Suggérer suppressions

**Pour emails potentiellement inutiles :**
- Codes expirés (>7 jours)
- Marketing ancien (>90 jours sans interaction)
- Spam évident

**Processus :**
1. Présenter l'email avec raison de suppression suggérée
2. Demander confirmation utilisateur
3. Si accepté, créer règle pour emails similaires futurs

### 6. Générer un bilan
Créer un rapport concis :
```
📧 Scan des emails terminé

✅ Actions effectuées :
- 5 emails archivés (confirmations de commandes)
- 3 emails marqués lus (newsletters)
- 2 emails déplacés vers personal/ecole

📬 Listes de distribution détectées :
- Newsletter Marketing XYZ (lien unsubscribe disponible)

🗑️ Suggestions de suppression :
- 2 codes SafeKey expirés (>30 jours)
- 1 newsletter ancienne jamais ouverte

⚠️ Emails nécessitant attention :
- 1 email : "PASSEPORT" - secretariat.balzac@lycee-descartes.ma
- 1 email : Facture importante

📊 Total : 13 emails traités
```

## Workflow complet de scan

### Exemple : Scanner et traiter INBOX

```bash
# 1. Scanner INBOX pour emails non lus (utiliser script Python pour recherche)
cd ~/.claude/skills/email-manager/scripts
./run.sh search_email --query "label:INBOX is:unread" --max-results 50 --full

# 2. Analyser chaque email selon les règles dans references/regles-tri.md

# 3. Pour un email de confirmation de commande Amazon (exemple):
# - Marquer lu (CLI Go)
email-manager read "MESSAGE_ID"

# - Lister les labels pour trouver l'ID de "personal/commandes" (CLI Go)
email-manager labels list

# - Ajouter le label personal/commandes (CLI Go)
email-manager labels apply "MESSAGE_ID" "LABEL_ID"

# - Archiver (retirer de INBOX) (CLI Go)
email-manager archive "MESSAGE_ID"

# 4. Pour un code SafeKey expiré (CLI Go):
email-manager delete "MESSAGE_ID"

# 5. Répéter pour tous les emails trouvés
```

**Stratégie recommandée :**
- Utiliser les **scripts Python** pour recherche et analyse complexe
- Utiliser le **CLI Go `email-manager`** pour les actions (read, archive, delete, download-attachments, labels)

### ⚠️ Important : Ne scanner QUE l'INBOX

```bash
# Scanner UNIQUEMENT l'INBOX
./run.sh search_email --query "label:INBOX newer_than:7d" --full

# ❌ NE PAS scanner les autres labels lors du tri
# Les emails déjà classés ne doivent JAMAIS être re-triés
```

## Opérations complètes disponibles

### 📧 Envoyer des emails

#### Email simple
```bash
./run.sh send_email \
  --to "destinataire@example.com" \
  --subject "Sujet de l'email" \
  --body "Corps de l'email"
```

#### Email avec CC et BCC
```bash
./run.sh send_email \
  --to "destinataire@example.com" \
  --subject "Sujet" \
  --body "Corps" \
  --cc "copie@example.com" \
  --bcc "copie.cachee@example.com"
```

#### Email avec pièces jointes
```bash
./run.sh send_email \
  --to "destinataire@example.com" \
  --subject "Documents" \
  --body "Voici les documents demandés" \
  --attach "/path/to/file1.pdf" "/path/to/file2.jpg"
```

### 🔍 Rechercher et lire des emails

#### Recherche simple
```bash
./run.sh search_email --query "is:unread"
```

#### Recherche avec détails complets
```bash
./run.sh search_email --query "from:example@gmail.com" --full
```

#### Obtenir les détails d'un email spécifique
```bash
./run.sh gmail_client --action get --message-id "MESSAGE_ID"
```

#### Exemples de requêtes Gmail
- `is:unread` - Emails non lus
- `from:example@gmail.com` - Emails d'un expéditeur
- `has:attachment` - Emails avec pièces jointes
- `label:INBOX` - Emails dans un label spécifique
- `after:2024/01/01 before:2024/01/31` - Emails par date
- `from:example.com has:attachment -is:read` - Requête complexe

### 🏷️ Gestion des labels

#### Lister tous les labels
```bash
./run.sh manage_labels --action list
```

#### Créer un nouveau label
```bash
./run.sh manage_labels --action create --label-name "personal/nouveau"
```

#### Ajouter des labels à un email
```bash
./run.sh manage_labels --action add \
  --message-id "MESSAGE_ID" \
  --label-ids "Label_123" "Label_456"
```

#### Retirer des labels d'un email
```bash
./run.sh manage_labels --action remove \
  --message-id "MESSAGE_ID" \
  --label-ids "INBOX"
```

### 📝 Gestion des brouillons

#### Lister les brouillons
```bash
./run.sh manage_drafts --action list
```

#### Créer un brouillon simple
```bash
./run.sh manage_drafts --action create \
  --to "destinataire@example.com" \
  --subject "Sujet" \
  --body "Corps du brouillon"
```

#### Créer un brouillon avec pièces jointes
```bash
./run.sh manage_drafts --action create \
  --to "destinataire@example.com" \
  --subject "Documents" \
  --body "Voici les documents" \
  --attach "/path/to/file1.pdf" "/path/to/file2.jpg"
```

#### Supprimer un brouillon
```bash
./run.sh manage_drafts --action delete --draft-id "r1234567890"
```

### 🗑️ Suppression et gestion spam

#### Mettre dans la corbeille
```bash
./run.sh delete_email --action trash --message-id "MESSAGE_ID"
```

#### Restaurer de la corbeille
```bash
./run.sh delete_email --action untrash --message-id "MESSAGE_ID"
```

#### Supprimer définitivement (demande confirmation)
```bash
./run.sh delete_email --action delete --message-id "MESSAGE_ID"
```

#### Marquer comme spam
```bash
./run.sh delete_email --action spam --message-id "MESSAGE_ID"
```

#### Retirer du spam
```bash
./run.sh delete_email --action not-spam --message-id "MESSAGE_ID"
```

#### Suppression en lot (demande confirmation)
```bash
./run.sh delete_email --action batch-delete \
  --message-ids "MESSAGE_ID1" "MESSAGE_ID2" "MESSAGE_ID3"
```

### 📖 Opérations de lecture

#### Marquer comme lu
```bash
./run.sh gmail_client --action read --message-id "MESSAGE_ID"
```

#### Marquer comme non lu
```bash
./run.sh gmail_client --action unread --message-id "MESSAGE_ID"
```

#### Archiver (retirer de INBOX)
```bash
./run.sh gmail_client --action archive --message-id "MESSAGE_ID"
```

## Références

- [Règles de tri détaillées](references/regles-tri.md) - Règles par type d'email et expéditeur
- [Patterns d'emails](references/patterns-emails.md) - Expressions régulières pour identifier les types d'emails
- [Filtres évolutifs](references/filtres-evolutifs.md) - Liste des expéditeurs filtrés automatiquement (mise à jour dynamique)
- [Scripts Gmail](scripts/README.md) - Documentation complète des scripts disponibles

## Évolution des règles

### Mise à jour automatique des filtres

Quand l'utilisateur accepte de filtrer/supprimer un expéditeur :
1. Ajouter l'expéditeur dans `references/filtres-evolutifs.md`
2. Mettre à jour `references/regles-tri.md` si nécessaire
3. Appliquer le filtre aux emails existants de cet expéditeur
4. Documenter la modification avec date et raison

### Suggestions proactives

Suggérer des nouvelles règles basées sur :
- Emails récurrents jamais ouverts (même expéditeur >5 fois)
- Patterns de spam détectés
- Codes/notifications expirés fréquents
