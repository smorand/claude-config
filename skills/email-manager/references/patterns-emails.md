# Patterns de détection d'emails

Expressions et patterns pour identifier automatiquement les types d'emails.

## Patterns par type

### Commandes e-commerce
**Expéditeurs (regex):**
```
.*amazon.*
.*fnac.*
.*ebay.*
.*aliexpress.*
```

**Sujets (mots-clés):**
- confirmation
- reçu / receipt
- commande / order
- livraison / delivery
- expédition / shipped

### Uber Eats (commandes restauration)
**Expéditeurs (regex):**
```
.*uber\.com$
.*ubereats.*
```

**Sujets (mots-clés):**
- Uber Eats
- commande
- reçu
- livraison

**Distinction avec Uber transport:**
Vérifier présence "Uber Eats" dans sujet ou "restaurant" dans corps

### Voyage (compagnies aériennes et Uber transport)
**Expéditeurs (regex):**
```
.*airfrance.*
.*air-france.*
.*ryanair.*
.*easyjet.*
.*lufthansa.*
.*uber\.com$ (si transport, pas Uber Eats)
```

**Sujets (mots-clés):**
- réservation
- billet
- vol / flight
- confirmation
- itinéraire
- boarding

### Services maison (factures et abonnements)
**Expéditeurs (regex):**
```
.*free.*
.*netflix.*
.*sosh.*
.*disney.*
.*crunchyroll.*
```

**Sujets NON publicitaires (mots-clés):**
- facture
- échéance
- prélèvement
- abonnement
- compte
- modification confirmée

**Sujets publicitaires (à archiver sans label):**
- offre
- nouveau
- découvrez
- promotion
- avantage

### Banques et paiements
**Expéditeurs (regex):**
```
.*paypal\.(fr|com)$
.*societegenerale.*
.*americanexpress.*
.*amex.*
```

**Récapitulatifs de paiement (afficher résumé puis archiver):**
- reçu
- paiement effectué
- transaction
- récapitulatif
- vous avez autorisé

**Codes de paiement à SUPPRIMER:**
- SafeKey
- code d'authentification
- one-time
- à usage unique

**Publicités (archiver sans label):**
- offre
- nouveau service
- avantage
- carte premium

### Newsletters
**Expéditeurs (regex):**
```
.*@substack\.com$
.*newsletter.*
.*@marketing.*
```

**Sujets (mots-clés):**
- newsletter
- recommendations
- digest
- weekly / mensuel
- édition

### Notifications automatiques
**Expéditeurs (regex):**
```
^noreply@.*
^no-reply@.*
^donotreply@.*
.*@notif.*
```

**Sujets (mots-clés):**
- code d'authentification
- code de vérification
- notification
- alert / alerte
- rappel / reminder

### Emails scolaires
**Expéditeurs (regex):**
```
.*@lycee-descartes\.ma$
.*pronote.*
^secretariat.*
```

**Sujets (mots-clés):**
- passeport
- voyage
- sortie scolaire
- réunion parents
- bulletin
- absence
- convocation

### Promotions
**Expéditeurs (regex):**
```
.*@emails\..*
.*marketing.*
.*promo.*
```

**Sujets (patterns):**
```
\d+%\s*(off|réduction|remise)
offre\s+(spéciale|exclusive)
soldes?
black\s+friday
cyber\s+monday
```

## ⚠️ Patterns DOUBLE CONFIRMATION (demander confirmation avant action)

### Paiements à effectuer
**Sujets contenant:**
- paiement requis
- à payer
- échéance
- facture impayée
- solde dû
- relance
- montant restant

**Action:** Afficher détails complets + demander confirmation explicite

### Check-in / Enregistrement vol
**Sujets contenant:**
- check-in
- enregistrement
- boarding pass
- carte d'embarquement
- enregistrez-vous
- online check-in

**Action:** Afficher détails complets + demander confirmation explicite

### Modifications / Changements vol
**Sujets contenant:**
- modification
- changement de vol
- annulation
- retard
- nouvelle heure
- reprogrammé
- vol modifié

**Action:** Afficher détails complets + demander confirmation explicite

## Patterns de priorité

### Haute priorité (ne jamais archiver automatiquement)
**Sujets contenant:**
- urgent
- important
- action requise
- deadline
- répondre avant

**Expéditeurs:**
- Famille (à définir par utilisateur)
- Supérieurs hiérarchiques
- Administrations officielles

### Basse priorité (archiver rapidement)
**Sujets contenant:**
- FYI
- pour info
- newsletter
- digest
- récapitulatif

## Détection listes de distribution et spam

### Headers à vérifier
**Indicateurs de mailing list :**
```
List-Unsubscribe: <...>
List-Id: ...
Precedence: bulk
X-Campaign-Id: ...
X-Mailer-Recptid: ...
```

### Liens de désinscription
**Patterns dans le corps de l'email :**
```
unsubscribe
se désabonner
gérer (vos|mes) préférences
opt.?out
désactivation
ne plus recevoir
arrêter les emails
```

**URLs typiques :**
```
.*unsubscribe.*
.*optout.*
.*preferences.*
.*email-settings.*
```

### Emails à suggérer pour suppression

**Spam évident :**
- Expéditeur non reconnu + sujet commercial agressif
- Nombreux liens/images mais peu de texte
- Sujet avec CAPS LOCK excessif
- Promesses financières irréalistes

**Codes/notifications expirés :**
- Codes de vérification >7 jours
- Codes promo expirés
- Liens temporaires expirés

**Pattern détection :**
```
\d+ jours? restants?
expire? (le|dans)
valable jusqu'au
code.{0,10}expire?
```

**Marketing ancien sans interaction :**
- >90 jours sans ouverture
- Emails récurrents jamais ouverts (>5 fois)
- Même expéditeur marketing >10 emails non lus

### Action proposée

**Format de suggestion :**
```
🗑️ Email candidat à suppression
Expéditeur : [expéditeur]
Sujet : [sujet]
Date : [date]
Raison : [code expiré depuis 30 jours / newsletter jamais ouverte / spam]

Supprimer cet email ? (oui/non)
Créer règle pour expéditeur similaire ? (oui/non)
```

## Détection de langue

**Français :**
- Mots-clés : merci, cordialement, bonjour, madame, monsieur

**Anglais :**
- Mots-clés : thanks, regards, hello, dear

Adapter les règles selon la langue détectée.
