# Règles de tri des emails

Règles détaillées pour le tri automatique des emails par type et expéditeur.

## ⚠️ RÈGLES CRITIQUES

### Double confirmation obligatoire

**Demander TOUJOURS confirmation explicite de l'utilisateur avant classification pour :**
1. Emails avec paiement à effectuer
2. Check-in / Enregistrement vol requis
3. Modifications / Changements de vol
4. Toute action nécessitant une intervention de l'utilisateur

### Suggestions de suppression

**Si un email semble inutile/spam récurrent, PROPOSER à l'utilisateur :**
1. Type d'email et raison de la suppression suggérée
2. Confirmer si suppression souhaitée
3. Ne JAMAIS supprimer sans accord explicite

### Listes de distribution et newsletters indésirables

**Détecter emails de type mailing list/distribution :**
- Présence d'un lien "unsubscribe" / "se désabonner"
- Emails marketing récurrents
- Newsletters non pertinentes

**Action à prendre :**
1. Signaler à l'utilisateur : "Email de liste de distribution détecté"
2. Proposer d'ouvrir le lien de désinscription
3. Demander si filtre permanent souhaité
4. Mettre à jour les règles après désinscription

## Résumé actions par type

| Type | Action | Label |
|------|--------|-------|
| Amazon, Fnac, Ebay | Archiver + Marquer lu | `personal/commandes` |
| Uber Eats | Archiver + Marquer lu | `personal/commandes` |
| Uber transport | Archiver + Marquer lu | `personal/voyage` |
| Compagnies aériennes | Archiver + Marquer lu | `personal/voyage` |
| Free, Netflix, Sosh, Disney+, Crunchyroll (factures) | Archiver + Marquer lu | `personal/Maison` |
| Free, Netflix, etc. (publicités) | Archiver + Marquer lu | AUCUN |
| Société Générale, Amex (publicités) | Archiver + Marquer lu | AUCUN |
| PayPal, banques (récaps paiement) | Résumé + Archiver | AUCUN |
| Amex SafeKey (codes paiement) | SUPPRIMER | - |
| Emails scolaires | Garder | `personal/ecole` |
| L'Oréal | Garder | `pro/L'Oréal` |

## Règles générales

### Emails à archiver automatiquement (après vérification rapide)

**Confirmations de commandes e-commerce :**
- Expéditeurs : `*amazon*`, `*fnac*`, `*ebay*`, `*aliexpress*`
- Sujets contenant : "confirmation", "reçu", "commande", "order confirmation", "expédition"
- Action : Marquer lu + Archiver + Ajouter label `personal/commandes`

**Confirmations Uber Eats :**
- Expéditeurs : `*uber.com` (uniquement Uber Eats, pas Uber transport)
- Sujets contenant : "commande", "reçu", "Uber Eats"
- Action : Marquer lu + Archiver + Ajouter label `personal/commandes`

**Récapitulatifs de paiement (archivage automatique après résumé) :**
- PayPal, Société Générale, American Express
- Sujets contenant : "reçu", "paiement effectué", "transaction", "récapitulatif"
- Action : Afficher résumé à l'utilisateur + Marquer lu + Archiver

**Codes de paiement temporaires à SUPPRIMER :**
- American Express SafeKey
- Sujets contenant : "code d'authentification", "SafeKey", "one-time"
- Action : SUPPRIMER définitivement (ne pas archiver)

**Newsletters et promotions :**
- Expéditeurs : `*@substack.com`, `*newsletter*`, `*@marketing*`, `tuifly@emails.tuifly.be`, `tommyhilfiger@e.tommy.com`
- Sujets contenant : "newsletter", "recommendations", "digest"
- Action : Marquer lu + Archiver (garder label existant)

**Publicités bancaires et cartes :**
- Société Générale, American Express (sauf codes paiement et factures)
- Sujets contenant : "offre", "promo", "avantage", "nouveau service"
- Action : Marquer lu + Archiver SANS label

**Publicités services (Free, Netflix, Sosh, Disney+, Crunchyroll) :**
- Expéditeurs : `*free*`, `*netflix*`, `*sosh*`, `*disney*`, `*crunchyroll*`
- Sujets contenant : "offre", "nouveau", "découvrez", "promotion"
- Action : Marquer lu + Archiver SANS label

### Emails services maison NON publicitaires (classification automatique)

**Services maison (Free, Netflix, Sosh, Disney+, Crunchyroll) :**
- Expéditeurs : `*free*`, `*netflix*`, `*sosh*`, `*disney*`, `*crunchyroll*`
- Sujets contenant : "facture", "échéance", "prélèvement", "abonnement", "compte", "confirmation modification"
- EXCLURE : publicités (voir section publicités ci-dessus)
- Action : Marquer lu + Archiver + Ajouter label `personal/Maison`

### Emails de voyage (classification automatique)

**Compagnies aériennes et Uber transport :**
- Expéditeurs : `*airfrance*`, `*ryanair*`, `*easyjet*`, `*lufthansa*`, `*uber.com` (transport uniquement)
- Sujets contenant : "réservation", "billet", "confirmation vol", "itinéraire"
- Action : Marquer lu + Archiver + Ajouter label `personal/voyage`

### Emails Assurance Maladie (classification automatique)

**Notifications Ameli :**
- Expéditeurs : `*ameli.fr`, `*assurance-maladie*`
- Tous les emails de l'Assurance Maladie
- Action : Marquer lu + Archiver + Ajouter label `personal` + **Inclure dans le bilan**

### Emails nécessitant DOUBLE CONFIRMATION avant classification

**⚠️ ATTENTION : Demander confirmation explicite avant toute action**

**Emails scolaires PRONOTE :**
- Expéditeurs : `*@lycee-descartes.ma`, `*pronote*`, `secretariat*`
- TOUS les emails de ces expéditeurs, sans exception
- Action : Afficher détails + **DEMANDER confirmation utilisateur** avant archivage + Ajouter label `personal/ecole` seulement après confirmation

**Paiements à effectuer :**
- Sujets contenant : "paiement requis", "à payer", "échéance", "facture impayée", "solde dû"
- Action : Afficher détails + **DEMANDER confirmation utilisateur** avant classification

**Enregistrement vol / Check-in :**
- Sujets contenant : "check-in", "enregistrement", "boarding pass", "carte d'embarquement"
- Action : Afficher détails + **DEMANDER confirmation utilisateur** avant classification

**Changements de vol / Modifications :**
- Sujets contenant : "modification", "changement de vol", "annulation", "retard", "nouvelle heure"
- Action : Afficher détails + **DEMANDER confirmation utilisateur** avant classification

### Emails nécessitant attention (ne pas archiver automatiquement)

**Emails scolaires :**
- Expéditeurs : `*@lycee-descartes.ma`, `*pronote*`, `secretariat*`
- Sujets contenant : demandes de documents, réunions, convocations
- Action : Ajouter label `personal/ecole` + Garder non lu si important

**Emails professionnels L'Oréal :**
- Expéditeurs : `*@loreal.com`
- Tous les emails sauf notifications automatiques
- Action : Ajouter label `pro/L'Oréal` + Garder non lu

**Factures importantes et documents officiels :**
- Sujets contenant : "facture", "invoice", "document officiel", "attestation"
- SAUF récapitulatifs déjà payés (voir section récapitulatifs)
- Action : Signaler à l'utilisateur + Ne pas archiver

## ⚠️ IMPORTANT : Focus sur INBOX uniquement

**Lors du tri des emails, scanner UNIQUEMENT l'INBOX.**

Les emails déjà présents dans les autres labels (personal/ecole, personal/voyage, personal/commandes, personal/Maison, pro/L'Oréal) ne doivent **JAMAIS** être re-triés. Une fois qu'un email est archivé de l'INBOX et classé dans un label de destination, il n'est plus touché.

### INBOX - Label à scanner

Trier tous les emails de l'INBOX selon les règles générales ci-dessus :
- Classer les emails selon leur type (commandes, voyage, école, etc.)
- Ajouter le label approprié
- Marquer comme lu si nécessaire
- Archiver (retirer de l'INBOX)

### Labels de destination - NE PAS scanner lors du tri

Ces labels contiennent des emails déjà traités et ne doivent pas être re-scannés :
- **personal/ecole** - Emails scolaires déjà classés
- **personal/voyage** - Emails de voyage déjà classés
- **personal/commandes** - Confirmations de commandes déjà classées
- **personal/Maison** - Services maison déjà classés
- **pro/L'Oréal** - Emails professionnels déjà classés

## Exceptions

**Ne jamais archiver automatiquement :**
- Emails avec pièces jointes importantes (contrats, documents officiels)
- Emails marqués comme importants (étoile)
- Emails en conversation active (réponse dans les 48h)
- Emails de famille ou amis proches

## Gestion des emails indésirables

### Emails à suggérer pour suppression

**Critères pour suggérer une suppression :**
- Spam évident (sujet suspect, expéditeur inconnu)
- Emails marketing très anciens (>90 jours) sans interaction
- Notifications obsolètes (codes expirés depuis >7 jours)
- Emails de services désactivés/non utilisés

**Processus :**
1. Identifier l'email candidat à suppression
2. Présenter à l'utilisateur : expéditeur, sujet, date, raison
3. Demander : "Voulez-vous supprimer cet email ?"
4. Si oui, créer règle pour emails similaires futurs

### Listes de distribution (mailing lists)

**Détection automatique :**
- Headers : `List-Unsubscribe`, `List-Id`, `Precedence: bulk`
- Liens dans le corps : "unsubscribe", "se désabonner", "gérer vos préférences"
- Pattern : emails récurrents du même expéditeur marketing

**Action proposée :**
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

**Après désinscription :**
- Ajouter expéditeur aux règles d'archivage automatique
- Archiver emails existants de cet expéditeur
- Mettre à jour `references/regles-tri.md`

### Filtres évolutifs

**Liste des expéditeurs à filtrer automatiquement :**
(Cette section sera mise à jour au fur et à mesure)

- `example@marketing.com` - Newsletter non pertinente (ajouté 2025-01-10)

**Format d'ajout :**
```
- `expéditeur@domaine.com` - Raison du filtre (date d'ajout)
```
