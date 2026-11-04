# Rapport final — Offre technique et méthodologique UNICEF Burundi

Reconstruction éditoriale du document à partir de deux sources : le PDF de l'offre
(contenu) et le modèle « Rapport de Stage Entreprise Minimaliste Moderne Noir et
Gris » (charte graphique uniquement).

## 1. Sources identifiées

| Rôle | Fichier | Caractéristiques | Usage |
|---|---|---|---|
| Modèle graphique | `Document Rapport de Stage Entreprise Minimaliste Moderne Noir et Gris (4).pdf` | 11 pages, A4 595,5 × 842,25 pt | Grille, marges, couleurs, hiérarchie typographique, couverture, sommaire, pied de page |
| Source de contenu | `OFFRE TECHNIQUE & MÉTHODOLOGIQUE UNICEF BURUNDI _Consultant International Dr Gullit.pdf` | 14 pages, US Letter | Totalité du texte, des données, tableaux, encadrés et mentions |

Les deux fichiers d'origine sont restés intacts (aucune écriture, aucun déplacement).

## 2. Caractéristiques graphiques reproduites

Relevé sur le modèle, mesuré au point (analyse des boîtes d'encre à 200 dpi) :

- **Format** A4 portrait, fond `#E8E8E7`, marges gauche/droite 59,5 pt, haut 42 pt,
  zone de texte 476,5 pt de large sur 710 pt de haut.
- **Polices** : Glacial Indifference (texte courant, 12 pt / interligne 16,63 pt) ;
  League Spartan Bold (titres de section 22 pt, titres d'encadré et d'intertitre 12 pt,
  sommaire 65 pt, couverture 47 pt) ; Distillery Script (grands numéros de section 31 pt,
  numéros du sommaire 27 pt, sous-titre du sommaire 22 pt).
- **Couleurs** : noir `#000000` pour le texte, brun-gris `#5E4032` pour les pastilles et
  les en-têtes de tableau, beige `#DACEC3` pour les cases marquées du calendrier,
  filets noirs 1,5 pt.
- **Repères de page** : pied de page « Offre technique et méthodologique » à x = 48,6,
  numéro de page cadré à droite (536 pt), filet noir de 0 à 204 pt à y = 782,6.
- **Couverture** : disque photographique de 286 pt centré à y = 42,7 ; titre sur trois
  lignes calées à droite (536 pt), lignes de base à 374,8 / 426,5 / 478,2 pt ;
  sous-titre centré sur trois lignes ; filet de 0 à 280,5 pt à y = 665 ; pastille
  « Novembre 2026 » de 175,8 × 40 pt centrée à y = 712.
- **Sommaire** : « Sommaire. » 65 pt, sous-titre en script, puis huit lignes de 53,3 pt
  (numéro script 27 pt, titre 20 pt, page à droite).

Contrôle d'alignement contre le modèle (boîtes d'encre, comparaison numérique) :
titre de section (113,3 · 39,8 · 298,0 · 59,2 contre 113,3 · 40,1 · 298,0 · 59,2),
numéro de page (61,5 · 39,4 · 89,2 · 61,0 contre 59,7 · 39,4 · 88,5 · 61,0),
lignes de texte à ± 0,4 pt, pastille de section 29,5 pt de haut sur 137,5 pt de large
(modèle : 29,5 × 137,4), barres d'en-tête de tableau 24 pt.

## 3. Sections intégrées

Aucune section, idée, donnée ou référence n'a été supprimée, résumée ni inventée.

| N° | Section | Page |
|---|---|---|
| 01 | Résumé exécutif | 3 |
| 02 | Compréhension de la mission | 3 |
| 03 | Objectifs de l'appui technique | 5 |
| 04 | Approche méthodologique | 6 |
| 05 | Assurance qualité | 13 |
| 06 | Gestion des risques | 14 |
| 07 | Calendrier indicatif | 15 |
| 08 | Expertise du consultant international : le Dr Gullit Lufiauluisu | 16 |

Volumétrie conservée : 8 sections, 69 paragraphes, 21 listes à puces ou numérotées,
8 pastilles de section, 19 intertitres, 4 encadrés « Produits attendus », 2 tableaux
(risques 4 × 2 avec en-tête répété, calendrier 5 phases × 6 semaines), 1 note de
calendrier, la couverture et l'illustration de couverture.

## 4. Difficultés liées aux polices

- **Glacial Indifference** : absente du dépôt ; fichier TTF officiel récupéré
  (`typeface-glacial-indifference`, upem 2048). Elle ne contient pas le point médian
  `·` (U+00B7) : tous les séparateurs de pastilles ont été convertis en tiret cadratin
  « — » ; les puces utilisent `•` (U+2022), présent dans la fonte.
- **League Spartan** : la version variable publiée par Fontsource (v2.002) est un
  redessin condensé, inutilisable ; la bonne version (v1.000, OTF 25 Ko) a été
  récupérée dans le dépôt `theleagueof/league-spartan`, puis convertie en TTF.
- **Distillery Script** : aucune version publique ni commerciale disponible ; la fonte
  a été reconstruite en courbes (31 pt pour les numéros, 27 pt au sommaire, 22 pt pour
  le sous-titre du sommaire) à partir des tracés du modèle. C'est la seule fonte qui
  n'est pas un original : elle reproduit les glyphes du modèle, sans garantie
  d'exhaustivité sur les caractères non utilisés.
- Les trois familles sont **incorporées** dans les deux livrables : sous-ensemble TrueType
  dans le PDF, parties `ObfuscatedFont` (ECMA-376 §17.8.1) dans le DOCX, avec
  `embedTrueTypeFonts` activé. Le rendu est donc identique sur un poste où les polices ne
  sont pas installées. Les fichiers TTF prêts à installer se trouvent dans
  `outils_offre_technique/fonts/` (dépôt) : il suffit de les installer pour éditer le
  DOCX avec les polices d'origine plutôt que celles incorporées.

## 5. Contrôles qualité effectués

1. **Présence des sections** : 132 blocs de contenu contrôlés automatiquement dans le
   PDF et dans le DOCX (titres, paragraphes, listes, pastilles, intertitres, encadrés,
   cellules des deux tableaux) — **0 manquant**.
2. **Chiffres, tableaux et références** : tableaux des risques et calendrier identiques
   à la source (libellés, semaines, marquages), note de calendrier conservée.
3. **Règles typographiques** : texte courant 12 pt, numéros de section 31 pt en script,
   titres de section 22 pt, titres encadrés/pastilles 12 pt blanc sur `#5E4032` —
   vérifié dans les deux fichiers (relevé des tailles et des couleurs).
4. **Cohérence des couleurs** : `#E8E8E7`, `#5E4032`, `#DACEC3`, noir — aucune autre
   teinte dans les deux documents.
5. **Contrôle visuel page par page** : 17 pages rendues et inspectées (couverture,
   sommaire, ouvertures de section, pages de pastilles, encadrés, tableaux, dernière
   page). Aucune page tronquée, aucun titre orphelin, aucun tableau coupé.
6. **Marges et sauts de page** : 0 débordement de marge détecté dans le PDF ; les sauts
   de page du DOCX reproduisent exactement ceux du PDF (mêmes 17 pages, mêmes
   ouvertures de section, y compris la coupure de liste à cheval sur les pages 5 et 6).
7. **Polices non substituées** : 4 fontes incorporées dans le PDF (aucune référence
   Helvetica résiduelle), 4 fontes incorporées dans le DOCX ; aucune substitution.
8. **Ouverture et éditabilité du DOCX** : structure OOXML validée (26 parties, ordre des
   éléments conforme au schéma, aucun XML invalide), 240 paragraphes et 15 tableaux
   natifs, styles de paragraphes et de caractères réglables, aucune protection.
9. **PDF = DOCX** : pagination du DOCX reconstituée avec les métriques réelles des
   polices (rendu de contrôle) puis comparée ligne à ligne au PDF — écart maximal
   observé 24 pt sur une page, 17 pages dans les deux fichiers, contenu identique.

## 6. Différences inévitables

- **Moteur de composition** : le PDF est composé avec ReportLab, le DOCX avec le moteur
  de Word. Les retours à la ligne, la justification et les hauteurs de ligne peuvent
  varier de quelques dixièmes de point ; les mêmes polices, la même largeur de colonne
  et les mêmes interlignes exacts produisent un résultat identique à la ligne près.
- **Interligne des paragraphes** : l'espace après paragraphe est fixé à 9 pt dans le
  DOCX (10,8 pt dans le PDF) pour absorber les arrondis de Word en twips et garantir
  qu'aucune page ne déborde.
- **Sommaire, entrée 08** : le titre se replie sur trois lignes ; Word place le numéro de
  page sur la dernière ligne (le PDF le place sur la première). Le numéro reste cadré à
  droite.
- **Distillery Script** est une reconstruction : les numéros sont fidèles au modèle mais
  ce n'est pas le fichier d'origine, qui n'existe pas dans le commerce.
- **Fond de page** : le DOCX porte son fond `#E8E8E7` par une image ancrée pleine page
  (visible à l'écran et à l'impression), le PDF par un aplat vectoriel.
- La page 14 reste partiellement remplie dans les deux fichiers (fin de la section 05
  puis ouverture de la section 06) : choix assumé pour ne pas couper le tableau des
  risques ni laisser un titre orphelin.

## 7. Livrables

- `LIVRABLES_OFFRE_TECHNIQUE/OFFRE_TECHNIQUE_VERSION_MODIFIABLE.docx`
  — 17 pages, 4 polices incorporées, tableaux et pastilles natifs, entièrement éditable.
  (238 Ko de texte et d'images + 140 Ko de polices incorporées.)
- `LIVRABLES_OFFRE_TECHNIQUE/OFFRE_TECHNIQUE_VERSION_FINALE.pdf`
  — 17 pages, A4, 4 polices vectorielles incorporées, aucune page tronquée.

Chaîne de production (dans `outils_offre_technique/`) : `content.py` (texte, source
unique), `design.py` (charte), `build_pdf.py`, `build_docx.py`, `embed_fonts.py`,
`qa.py` (contrôles), `docx_preview.py` (rendu de contrôle du DOCX).
