# Google Keep Note Manager Scripts

Scripts Python pour gérer les notes Google Keep via l'API `gkeepapi`.

## Authentication Setup

⚠️ **Important :** Google Keep n'a pas d'API officielle publique. Cette skill utilise `gkeepapi` (bibliothèque non officielle) qui nécessite un **master token** pour s'authentifier.

### Étape 1 : Obtenir un OAuth2 Token

Pour obtenir un master token, vous devez d'abord récupérer un **OAuth2 token** (authentication token).

**Instructions détaillées :**

1. **Allez sur** : https://accounts.google.com/EmbeddedSetup
2. **Connectez-vous** avec votre compte Google et acceptez les conditions
3. **Ouvrez les Developer Tools** de votre navigateur :
   - Chrome/Edge : F12 ou Clic droit > Inspecter
   - Firefox : F12 ou Clic droit > Inspecter l'élément
4. **Allez dans l'onglet "Application"** (Chrome) ou "Stockage" (Firefox)
5. **Dans le menu de gauche**, dépliez "Cookies" > `https://accounts.google.com`
6. **Trouvez le cookie `oauth_token`** et copiez sa valeur
   - Le token commence par `oauth2_4/`
   - Exemple : `oauth2_4/0Ab32j90fvQ6SVsc4Leu0SuKINhcAgqTzqQpn6MRIZIHSVUU_hmmLLfwcSR3tH8WwM-RdJw`

**Alternative (via le cadenas)** :
1. Allez sur https://accounts.google.com/EmbeddedSetup et connectez-vous
2. Cliquez sur le **cadenas** dans la barre d'adresse
3. Allez dans **Cookies** > `accounts.google.com` > **Cookies**
4. Trouvez `oauth_token` et copiez le contenu

### Étape 2 : Générer le Master Token

Une fois que vous avez l'OAuth2 token, utilisez ce script pour générer le master token :

```bash
cd ~/.claude/skills/note-manager/scripts
source .venv/bin/activate

python3 << 'EOF'
import gpsoauth
import gkeepapi
import json
import os
import secrets
from pathlib import Path

# REMPLACEZ CES VALEURS
email = 'votre-email@gmail.com'
oauth_token = 'oauth2_4/...'  # Le token que vous avez copié

# Générer un android_id aléatoire
android_id = secrets.token_hex(8)

print(f"Email: {email}")
print(f"Android ID: {android_id}")
print(f"OAuth Token: {oauth_token[:50]}...")

try:
    print("\nÉchange de l'OAuth token contre un master token...")
    master_response = gpsoauth.exchange_token(email, oauth_token, android_id)

    if 'Token' not in master_response:
        print(f"✗ Erreur: {master_response}")
        exit(1)

    master_token = master_response['Token']
    print(f"✓ Master token obtenu: {master_token[:50]}...")

    # Test d'authentification avec Keep
    print("\nTest d'authentification avec Google Keep...")
    keep = gkeepapi.Keep()
    keep.resume(email, master_token)
    keep.sync()
    print("✓ Authentification réussie!")

    # Sauvegarde des credentials
    credentials_path = os.path.expanduser("~/.claude/credentials/gkeep_credentials.json")
    Path(credentials_path).parent.mkdir(parents=True, exist_ok=True)

    with open(credentials_path, "w") as f:
        json.dump({
            "username": email,
            "token": master_token
        }, f)

    os.chmod(credentials_path, 0o600)

    print(f"\n✓ Credentials sauvegardés: {credentials_path}")
    print("\nVous pouvez maintenant utiliser les scripts Google Keep!")

except Exception as e:
    print(f"\n✗ Erreur: {e}")
    import traceback
    traceback.print_exc()
EOF
```

### Types de tokens

- **Authentication token / OAuth2 token** (commence par `oauth2_4/`)
  - Expire rapidement
  - Ne peut être utilisé qu'une seule fois
  - Utilisé pour obtenir le master token

- **Master token** (commence par `aas_et/`)
  - N'expire jamais
  - Utilisé pour s'authentifier avec Google Keep
  - Sauvegardé dans `~/.claude/credentials/gkeep_credentials.json`

- **Access token** (commence par `ya29.`)
  - Expire en 1 heure
  - Généré automatiquement par `gkeepapi`

### Référence

Instructions détaillées avec captures d'écran : https://github.com/rukins/gpsoauth-java#receiving-an-authentication-token

## Scripts disponibles

### `auth.py` - Authentification
Configure l'authentification Google Keep et sauvegarde les credentials.

**Usage :**
```bash
./run.sh auth
```

### `search_notes.py` - Recherche de notes
Recherche des notes avec tri automatique (épinglées en premier).

**Usage :**
```bash
# Recherche simple
./run.sh search_notes --query "mot clé"

# Recherche détaillée (JSON)
./run.sh search_notes --query "mot clé" --full

# Inclure notes archivées
./run.sh search_notes --include-archived

# Limiter résultats
./run.sh search_notes --max-results 10
```

### `manage_notes.py` - Gestion CRUD
Créer, lire, modifier, archiver, épingler, supprimer et dupliquer des notes.

**Usage :**
```bash
# Créer note texte
./run.sh manage_notes --action create-text --title "Titre" --text "Contenu"

# Créer liste
./run.sh manage_notes --action create-list --title "Liste" --items '["Item 1", "Item 2"]'

# Obtenir note
./run.sh manage_notes --action get --note-id "NOTE_ID"

# Modifier note
./run.sh manage_notes --action update --note-id "NOTE_ID" --title "Nouveau titre"

# Épingler
./run.sh manage_notes --action pin --note-id "NOTE_ID"

# Archiver
./run.sh manage_notes --action archive --note-id "NOTE_ID"

# Dupliquer
./run.sh manage_notes --action duplicate --note-id "NOTE_ID" --new-title "Copie"

# Supprimer
./run.sh manage_notes --action delete --note-id "NOTE_ID"
```

## Dépendances

- Python 3.11+
- gkeepapi

Les dépendances sont installées automatiquement par `run.sh` via `uv`.
