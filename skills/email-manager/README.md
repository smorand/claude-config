# Email Manager - Skill de gestion d'emails Gmail

Skill automatisée pour trier, classer et archiver vos emails Gmail en français.

## Installation

La skill est déjà installée dans `~/.claude/skills/email-manager/`

Elle sera automatiquement chargée lors de votre prochaine session Claude Code.

## Utilisation

Dites simplement :
- **"On scan les emails"**
- **"Trie mes emails"**
- **"Gère ma boîte mail"**

Claude analysera automatiquement vos emails et appliquera les règles configurées.

## Focus : INBOX uniquement

⚠️ **Important** : Lors du tri des emails, la skill scanne **UNIQUEMENT l'INBOX**.

Les emails déjà classés dans d'autres labels (personal/ecole, personal/voyage, etc.) ne sont **jamais re-triés**. Une fois qu'un email est archivé de l'INBOX et classé dans un label spécifique, il n'est plus touché.

**Labels de destination** (où les emails de l'INBOX seront déplacés) :
1. **personal/ecole** - Emails scolaires
2. **personal/voyage** - Voyages et billets
3. **personal/commandes** - Confirmations de commandes
4. **personal/Maison** - Services maison (Free, Netflix, etc.)
5. **pro/L'Oréal** - Emails professionnels

## Règles de tri configurées

### ✅ Classification automatique

| Type | Action | Label |
|------|--------|-------|
| Amazon, Fnac, Ebay | Archiver + Marquer lu | `personal/commandes` |
| Uber Eats | Archiver + Marquer lu | `personal/commandes` |
| Uber transport | Archiver + Marquer lu | `personal/voyage` |
| Compagnies aériennes | Archiver + Marquer lu | `personal/voyage` |
| Free, Netflix, Sosh, Disney+, Crunchyroll (factures) | Archiver + Marquer lu | `personal/Maison` |

### 🗑️ Archivage sans label

- Publicités Free, Netflix, Sosh, Disney+, Crunchyroll
- Publicités Société Générale, American Express
- Récapitulatifs de paiement (après résumé)

### ⚠️ Suppression

- Codes de paiement American Express SafeKey

### 🔔 Double confirmation requise

Claude vous demandera confirmation AVANT de classer :
1. **Paiements à effectuer** - factures impayées, échéances
2. **Check-in vol** - enregistrement requis
3. **Modifications vol** - changements, annulations

### 🛡️ Jamais archivés automatiquement

- Emails scolaires (Lycée Descartes)
- Emails professionnels L'Oréal
- Factures importantes
- Documents officiels

## Nouvelles fonctionnalités

### 📬 Détection listes de distribution

Claude détecte automatiquement les mailing lists et newsletters avec liens de désinscription.

**Proposition :**
```
📬 Liste de distribution détectée
Expéditeur : marketing@example.com
Sujet : Newsletter hebdomadaire

🔗 Lien de désinscription disponible
Voulez-vous :
1. Ouvrir le lien pour vous désabonner
2. Créer un filtre pour archiver automatiquement
3. Ignorer (garder comme maintenant)
```

### 🗑️ Suggestions de suppression

Claude propose de supprimer les emails inutiles :
- Codes expirés (>7 jours)
- Marketing ancien (>90 jours sans interaction)
- Spam évident

**Vous décidez :** Aucune suppression sans votre accord explicite.

### 📋 Filtres évolutifs

Après chaque désinscription ou suppression acceptée, Claude met à jour automatiquement les règles pour filtrer les futurs emails similaires.

## Exemple de bilan

Après un scan, vous recevrez un rapport comme :

```
📧 Scan des emails terminé

✅ Actions effectuées :
- 8 emails archivés (confirmations Amazon, Fnac)
- 3 emails archivés (publicités Netflix, Free)
- 2 codes SafeKey supprimés
- 1 récap PayPal archivé après résumé

📬 Listes de distribution détectées :
- Newsletter Tech Weekly (lien unsubscribe disponible)
- Marketing XYZ (lien de désinscription trouvé)

🗑️ Suggestions de suppression :
- 3 codes SafeKey expirés (>30 jours)
- 1 newsletter jamais ouverte (>90 jours)

⚠️ Nécessitent confirmation :
- Air France : Check-in vol Paris-Dublin (départ 15/05)

📊 Total : 18 emails traités
```

## Personnalisation

Pour modifier les règles, éditez :
- `references/regles-tri.md` - Règles détaillées
- `references/patterns-emails.md` - Patterns de détection

## Sécurité

- Aucune suppression sans confirmation
- Double validation pour actions critiques
- Emails importants jamais archivés automatiquement

## Scripts Gmail personnalisés

La skill utilise des scripts Python personnalisés pour les opérations avancées, notamment l'envoi d'emails avec pièces jointes.

**Scripts disponibles :**
- `send_email` - Envoyer des emails avec pièces jointes
- `search_email` - Rechercher des emails
- `manage_labels` - Créer, lister et gérer les labels
- `manage_drafts` - Créer des brouillons avec pièces jointes
- `delete_email` - Supprimer, archiver, gérer spam
- `gmail_client` - Opérations génériques (lire, marquer lu/non lu, archiver)

**Voir la documentation complète :** `scripts/README.md`

**Exemple d'utilisation :**
```bash
~/.claude/skills/email-manager/scripts/run.sh send_email \
  --to "destinataire@example.com" \
  --subject "Documents" \
  --body "Voici les documents demandés" \
  --attach "/path/to/file.pdf"
```
