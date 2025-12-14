# Conversation - Modification Script Acte d'Engagement PDF

**Date:** 2025-11-30
**Sujet:** Description et modification du script `complete_acte_engagement.py` pour retirer la signature PNG

---

## Utilisateur
Je veux que tu regardes le script complete_acte_engagement.py, et tu me le décris

---

## Assistant

Je vais lire le script pour vous le décrire.

*[Recherche et lecture du fichier `/Users/sebastien.morand/Downloads/complete_acte_engagement.py`]*

### Description du script `complete_acte_engagement.py`

Ce script Python automatise le remplissage d'un **acte d'engagement scolaire** (voyage scolaire à Dublin pour Balzac). Voici sa structure :

#### **Objectif**
Remplir automatiquement un PDF d'acte d'engagement avec les informations personnelles et y ajouter une signature numérique.

#### **Bibliothèque utilisée**
- **PyMuPDF (fitz)** : pour la manipulation de PDF

#### **Fichiers manipulés**
- **PDF source** : `/Users/sebastien.morand/Downloads/20251124 - Acte d'engagement VOY 11 2025-2026 DUBLIN BALZAC (002).pdf`
- **Signature** : `/Users/sebastien.morand/Downloads/Signature_Seb.png`
- **PDF de sortie** : même nom avec suffixe `_signed.pdf`

#### **Données renseignées**

**Informations parent** :
- Nom : Sébastien MORAND
- Adresse : 27 rue de Sebta, 14000 Kénitra
- Téléphone : 06 61 19 72 79
- Relation : Père

**Informations enfant** :
- Nom : Amira Rose MORAND
- Classe : 3.03
- Établissement : Honoré de Balzac Kénitra

**Signature** :
- Lieu : Kénitra
- Date : 26 12 2026

#### **Fonctions principales**

1. **`insert_bold_text()`** : Simule du texte en gras en dessinant le texte plusieurs fois avec de légers décalages
2. **`insert_text()`** : Insère du texte normal
3. **`draw_checkbox()`** : Dessine une case à cocher (avec ou sans croix)
4. **`strike_through_text()`** : Barre du texte en traçant une ligne

#### **Opérations effectuées**

**Page 1 (informations personnelles)** :
- Raye "Mme" et "Mlle" (garde "M.")
- Ajoute nom/adresse/téléphone du parent en gras
- Raye "mon fils" et "ma pupille" (garde "ma fille")
- Raye "Mère" et "tuteur légal" (garde "Père" et "Responsable légal")
- Ajoute nom/classe/établissement de l'enfant en gras

**Sur toutes les pages** :
- Coche la case "OUI" pour la caisse de solidarité
- Ajoute lieu et date après "Fait à"
- Insère la signature PNG (taille 315x105 pixels, soit +40% de l'original déjà agrandi de 50%)

#### **Particularités techniques**
- Positionnement précis avec décalages en pixels (x, y)
- Recherche de texte pour localiser les zones à remplir
- Gestion de multiples instances de texte (différencie premier/deuxième "Nom, prénom")
- Ajustements fins pour l'alignement (ex: "+12px", "-3px")

Le script affiche des messages de confirmation (✓) pour chaque opération réussie.

---

## Utilisateur
Ok je veux que tu supprimes la partie Signature PNG le reste tu touches à rien et tu me génére un fichier non signée. Puis tu l'ouvres que je puisse le regarder

---

## Assistant

Je vais modifier le script pour supprimer la partie signature PNG et générer le fichier non signé.

*[Lecture du fichier]*

**Modifications apportées** :

1. Suppression de la ligne `signature_path = Path("/Users/sebastien.morand/Downloads/Signature_Seb.png")`
2. Changement du nom de fichier de sortie : `output_path = pdf_path.parent / f"{pdf_path.stem}_unsigned.pdf"`
3. Suppression du bloc de code qui insère la signature (lignes 216-231) :
```python
# Chercher la zone de signature
signature_instances = page.search_for("Signature du responsable légal")
if signature_instances:
    for sig_inst in signature_instances:
        # Position de la signature (en dessous du texte)
        sig_x = sig_inst.x0
        sig_y = sig_inst.y1 + 20  # 20 points en dessous

        # Insérer l'image de signature
        # Taille originale: 150x50
        # +50% = 225x75
        # +40% supplémentaire de 225x75 = 315x105
        signature_rect = fitz.Rect(sig_x, sig_y, sig_x + 315, sig_y + 105)

        page.insert_image(signature_rect, filename=str(signature_path), keep_proportion=True)
        print(f"✓ Signature ajoutée à ({sig_x}, {sig_y}) - Taille: 315x105")
```
4. Modification du message final : `print(f"\n✅ PDF complété (non signé) : {output_path}")`

**Exécution du script** :
```
✓ 'Mme' rayé
✓ 'Melle' rayé
✓ Nom parent ajouté (en gras): Sébastien MORAND
✓ Adresse ajoutée (en gras): 27 rue de Sebta, 14000 Kénitra
✓ Téléphone ajouté (en gras): 06 61 19 72 79
✓ 'mon fils' rayé
✓ 'ma pupille' rayé
✓ 'Mère' rayé
✓ 'tuteur légal' rayé
✓ Nom enfant ajouté (en gras): Amira Rose MORAND
✓ Classe ajoutée (en gras): 3.03
✓ Etablissement ajouté (en gras): Honoré de Balzac Kénitra
✓ Case 'OUI' cochée pour caisse de solidarité à (269.04998779296875, 298.2660217285156)
✓ Trouvé 'Fait à' à la page 2
✓ Lieu ajouté: Kénitra
✓ Date ajoutée: 26    12    2026

✅ PDF complété (non signé) : /Users/sebastien.morand/Downloads/20251124 - Acte d'engagement VOY 11 2025-2026 DUBLIN BALZAC (002)_unsigned.pdf
```

**Résultat** :
Le PDF a été généré avec toutes les informations remplies **sauf la signature PNG** :
- ✓ Civilité (M. sélectionné, Mme et Melle rayés)
- ✓ Informations parent (nom, adresse, téléphone)
- ✓ Relation (Père sélectionné, autres rayés)
- ✓ Genre enfant (ma fille sélectionné, mon fils et ma pupille rayés)
- ✓ Informations enfant (nom, classe, établissement)
- ✓ Case OUI cochée pour caisse de solidarité
- ✓ Lieu et date (Kénitra, 26 12 2026)
- ❌ Signature PNG (supprimée comme demandé)

Le fichier a été ouvert pour consultation :
`20251124 - Acte d'engagement VOY 11 2025-2026 DUBLIN BALZAC (002)_unsigned.pdf`

---

## Utilisateur
I want you to backup this conversation.

---

**FIN DE LA CONVERSATION**

---

## ANNEXE - Script Python Modifié

**Fichier:** `complete_acte_engagement.py` (version sans signature PNG)

```python
#!/usr/bin/env python3
"""
Script pour remplir complètement l'acte d'engagement avec toutes les informations
"""
import fitz  # PyMuPDF
from pathlib import Path

# Chemins des fichiers
pdf_path = Path(
    "/Users/sebastien.morand/Downloads/20251124 - Acte d'engagement VOY 11 2025-2026 DUBLIN BALZAC (002).pdf"
)
output_path = pdf_path.parent / f"{pdf_path.stem}_unsigned.pdf"

# Informations à remplir
parent_info = {
    "nom_prenom": "Sébastien MORAND",
    "adresse": "27 rue de Sebta, 14000 Kénitra",
    "telephone": "06 61 19 72 79",
    "relation": "Père",  # Rayer les autres
}

enfant_info = {
    "nom_prenom": "Amira Rose MORAND",
    "classe": "3.03",
    "etablissement": "Honoré de Balzac Kénitra",
}

fait_a_info = {
    "lieu": "Kénitra",
    "date": "26    12    2026",  # Avec 4 espaces entre jour/mois/année
}

# Ouvrir le PDF
doc = fitz.open(pdf_path)


def insert_bold_text(page, x, y, text, fontsize=11):
    """Insère du texte en gras en le dessinant plusieurs fois avec léger décalage"""
    font = fitz.Font("helv")
    # Dessiner le texte plusieurs fois avec très léger décalage pour simuler le gras
    for offset_x in [0, 0.3, 0.6]:
        for offset_y in [0, 0.3]:
            writer = fitz.TextWriter(page.rect)
            writer.append((x + offset_x, y + offset_y), text, fontsize=fontsize, font=font)
            writer.write_text(page, color=(0, 0, 0))


def insert_text(page, x, y, text, fontsize=11):
    """Insère du texte normal"""
    font = fitz.Font("helv")
    writer = fitz.TextWriter(page.rect)
    writer.append((x, y), text, fontsize=fontsize, font=font)
    writer.write_text(page, color=(0, 0, 0))


def draw_checkbox(page, x, y, size=10, checked=True):
    """Dessine une case à cocher"""
    # Dessiner le carré
    rect = fitz.Rect(x, y, x + size, y + size)
    page.draw_rect(rect, color=(0, 0, 0), width=1)

    # Si cochée, ajouter une croix
    if checked:
        page.draw_line((x, y), (x + size, y + size), color=(0, 0, 0), width=1.5)
        page.draw_line((x + size, y), (x, y + size), color=(0, 0, 0), width=1.5)


def strike_through_text(page, rect, color=(0, 0, 0)):
    """Barre du texte"""
    # Tracer une ligne au milieu du rectangle
    y_middle = (rect.y0 + rect.y1) / 2
    page.draw_line((rect.x0, y_middle), (rect.x1, y_middle), color=color, width=1)


# Parcourir les pages pour remplir les informations
for page_num in range(len(doc)):
    page = doc[page_num]

    # Page 1: Informations personnelles
    if page_num == 0:
        # Rayer "Mme" et "Mlle" pour garder "M."
        mme_instances = page.search_for("Mme")
        for inst in mme_instances:
            strike_through_text(page, inst)
            print("✓ 'Mme' rayé")

        melle_instances = page.search_for("Melle")
        for inst in melle_instances:
            strike_through_text(page, inst)
            print("✓ 'Melle' rayé")

        # Chercher "Nom, prénom :" pour le parent
        nom_instances = page.search_for("Nom, prénom")
        if nom_instances and len(nom_instances) > 0:
            # Premier "Nom, prénom" est pour le parent
            inst = nom_instances[0]
            x = inst.x1 + 10
            y = inst.y0 + 12  # Descendre d'une ligne - 3px plus haut que 15 (15-3=12)
            insert_bold_text(page, x, y, parent_info["nom_prenom"], fontsize=11)
            print(f"✓ Nom parent ajouté (en gras): {parent_info['nom_prenom']}")

        # Chercher "Adresse :" pour ajouter l'adresse
        adresse_instances = page.search_for("Adresse :")
        if adresse_instances:
            inst = adresse_instances[0]
            x = inst.x1 + 10
            y = inst.y0 + 11  # 16px - 5px = 11px plus bas
            insert_bold_text(page, x, y, parent_info["adresse"], fontsize=11)
            print(f"✓ Adresse ajoutée (en gras): {parent_info['adresse']}")

        # Chercher "Téléphone :"
        tel_instances = page.search_for("Téléphone")
        if tel_instances:
            inst = tel_instances[0]
            x = inst.x1 + 10
            y = inst.y0 + 11  # 15px - 4px = 11px plus bas
            insert_bold_text(page, x, y, parent_info["telephone"], fontsize=11)
            print(f"✓ Téléphone ajouté (en gras): {parent_info['telephone']}")

        # Chercher et rayer les mentions inutiles pour "mon fils, ma fille, ma pupille"
        # On garde "ma fille" et on raye "mon fils" et "ma pupille"
        fils_instances = page.search_for("mon fils")
        if fils_instances:
            for inst in fils_instances:
                strike_through_text(page, inst)
                print("✓ 'mon fils' rayé")

        pupille_instances = page.search_for("ma pupille")
        if pupille_instances:
            for inst in pupille_instances:
                strike_through_text(page, inst)
                print("✓ 'ma pupille' rayé")

        # Rayer "Mère" et "tuteur légal" pour garder "Père" et "Responsable légal"
        mere_instances = page.search_for("Mère")
        for inst in mere_instances:
            strike_through_text(page, inst)
            print("✓ 'Mère' rayé")

        # Rayer "tuteur légal" (mais pas "Responsable légal")
        tuteur_instances = page.search_for("tuteur légal")
        for inst in tuteur_instances:
            strike_through_text(page, inst)
            print("✓ 'tuteur légal' rayé")

        # Chercher le deuxième "Nom, prénom" pour l'enfant
        if len(nom_instances) > 1:
            inst = nom_instances[1]
            x = inst.x1 + 10
            y = inst.y0 + 12  # Même décalage que le parent
            insert_bold_text(page, x, y, enfant_info["nom_prenom"], fontsize=11)
            print(f"✓ Nom enfant ajouté (en gras): {enfant_info['nom_prenom']}")

        # Chercher "Classe :"
        classe_instances = page.search_for("Classe :")
        if classe_instances:
            inst = classe_instances[0]
            x = inst.x1 + 5
            y = inst.y0 + 12  # 12px plus bas
            insert_bold_text(page, x, y, enfant_info["classe"], fontsize=11)
            print(f"✓ Classe ajoutée (en gras): {enfant_info['classe']}")

        # Chercher "Etablissement :"
        etab_instances = page.search_for("Etablissement :")
        if etab_instances:
            inst = etab_instances[0]
            x = inst.x1 + 5
            y = inst.y0 + 12  # 12px plus bas
            insert_bold_text(page, x, y, enfant_info["etablissement"], fontsize=11)
            print(f"✓ Etablissement ajouté (en gras): {enfant_info['etablissement']}")

    # Chercher la case à cocher "OUI" pour la caisse de solidarité
    caisse_instances = page.search_for("caisse de solidarité")
    if caisse_instances:
        # Chercher "OUI" en majuscules (après caisse de solidarité)
        oui_instances = page.search_for("OUI")
        for oui_inst in oui_instances:
            # Vérifier que "OUI" est après "caisse de solidarité"
            if oui_inst.y0 > caisse_instances[0].y0:
                # La case est juste après "OUI", on cherche le caractère □
                # Position de la case : après "OUI "
                checkbox_x = oui_inst.x1 + 5  # Juste après "OUI"
                checkbox_y = oui_inst.y0 - 2  # Aligné avec le texte
                draw_checkbox(page, checkbox_x, checkbox_y, size=10, checked=True)
                print(f"✓ Case 'OUI' cochée pour caisse de solidarité à ({checkbox_x}, {checkbox_y})")
                break

    # Chercher "Fait à" pour ajouter lieu et date
    fait_instances = page.search_for("Fait à")
    if fait_instances:
        print(f"✓ Trouvé 'Fait à' à la page {page_num + 1}")

        for inst in fait_instances:
            # Obtenir la position du texte "Fait à"
            x = inst.x1 + 10
            y = inst.y0 + 8  # 8px plus bas

            # Ajouter "Kénitra" en gras
            insert_bold_text(page, x, y, fait_a_info["lieu"], fontsize=11)
            print(f"✓ Lieu ajouté: {fait_a_info['lieu']}")

            # Chercher ", le" après "Fait à" pour placer la date
            date_instances = page.search_for(", le")
            if date_instances:
                for date_inst in date_instances:
                    # Vérifier que c'est proche de "Fait à"
                    if abs(date_inst.y0 - inst.y0) < 5:  # Même ligne
                        date_x = date_inst.x1 + 16  # +5 initial + 6px + 5px = 16px vers la droite
                        date_y = date_inst.y0 + 8  # 8px plus bas

                        # Ajouter la date en gras (avec espaces: "26  12  2026")
                        insert_bold_text(page, date_x, date_y, fait_a_info["date"], fontsize=11)
                        print(f"✓ Date ajoutée: {fait_a_info['date']}")

# Sauvegarder le PDF modifié
doc.save(output_path)
doc.close()

print(f"\n✅ PDF complété (non signé) : {output_path}")
```
