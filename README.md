# Refonte du site CEFISI

Projet de refonte de `www.cefisi.com` : site public, administration des contenus et espace documentaire pour les étudiants et l'équipe pédagogique.

**Équipe :** Mattéo, Romain, Tim. **Interlocutrice côté client :** Manon Oubekkou.
**État :** conception. Aucun développement n'a commencé, aucune date n'est fixée.

La plateforme de candidatures `candidatures-cefisi.com` reste **hors périmètre** : le nouveau site y renvoie par un lien, sans reprendre la création de compte ni le traitement des dossiers.

---

## Documents du projet

| Répertoire | Contenu | Formats |
|---|---|---|
| `livrables/01-cadrage/` | Note de cadrage V1 et journal d'observations | Word, PDF |
| `livrables/02-conception/` | Dossier de conception : périmètre, 39 fonctionnalités, 16 difficultés techniques, critères de recette, choix de stack, décisions à prendre | Word, PDF |
| `livrables/03-inventaire/` | Inventaire des pages du site actuel, de leur utilité et de leurs médias | Word, Excel |
| `livrables/04-maquettes/` | Dix écrans de référence exportés depuis Penpot | PNG |
| `livrables/05-matrice/` | Matrice des droits : 52 droits par domaine et par rôle, avec le rattachement au dossier | Excel |
| `livrables/06-medias/` | Archive des images du site actuel récupérées localement | ZIP |

Les sources Markdown et les données d'observation sont dans `docs/`, les scripts de génération dans `tools/`.

## Structure du dépôt

```
docs/
  cadrage/        dossier-de-conception-v1.md, note-de-cadrage-v1.md
  observations/   journal.md, site-audit.json, site-rendered.json, site-css.json
  pilotage/       suivi.md (notes de suivi initiales)
livrables/        01 à 06, voir le tableau ci-dessus
medias/
  site-actuel/    manifest.csv et README.md de la collecte
tools/            scripts de collecte et de génération
```

## Ce que disent les chiffres

| Donnée | Valeur | Source |
|---|---|---|
| Pages relevées dans les sitemaps | 28 (25 pages, 2 articles, 1 catégorie) | `docs/observations/site-audit.json` |
| Pages publiques observées | 20, plus 4 derrière une connexion et 4 non visitées | idem |
| Références d'images dans les CSS | 65 | `docs/observations/site-css.json` |
| Médias | 102 références, 100 fichiers récupérés | `medias/site-actuel/manifest.csv` |
| Droits décrits dans la matrice | 52, sur 5 domaines | `livrables/05-matrice/` |
| Fonctionnalités, difficultés, exigences | 39, 16, 12 | `livrables/02-conception/` |

Le dossier de conception recalcule ces compteurs à chaque génération et échoue si un identifiant manque, se répète, ou si le classement des stacks ne correspond plus au tableau de points.

## Régénérer les documents

Le Markdown est la source ; les scripts produisent Word et PDF.

```bash
# Python avec python-docx, reportlab, openpyxl et pypdf
python tools/produire_dossier_conception.py      # dossier de conception
python tools/produire_documents.py               # note de cadrage et journal
python tools/produire_inventaire_site.py         # inventaire des pages
python tools/mapper_matrice_droits.py            # rattachement matrice ↔ dossier
```

## Suivi

Le suivi des tâches est un tableau Trello privé : <https://trello.com/b/2o9z11DF/refonte-du-site-cefisi>.
« En attente » regroupe les tâches futures, « En cours — prochain sprint » celles à présenter au prochain point. Ce tableau ne remplace ni l'inventaire, qui est un catalogue, ni la matrice des droits, qui sert à arbitrer.

## Limites connues

- **L'espace privé du site actuel n'a pas été exploré** : les adresses réservées répondent par une redirection vers la connexion. L'inventaire ne couvre que le public.
- **Les droits de diffusion des images ne sont pas vérifiés.** Les copies locales servent au travail interne ; leur publication demande l'accord du client.
- Les contenus des maquettes sont **fictifs** et signalés comme tels dans chaque écran.
- Les signalements d'indisponibilité du site et de recherche défaillante viennent du groupe, sans diagnostic.

## Ce qui n'est pas versionné

Les copies d'images du site actuel (`medias/site-actuel/pages/`, `communs/`, `css/`) et l'archive ZIP ne sont pas versionnées : contenus tiers dont les droits de rediffusion ne sont pas établis, et volume important. Le manifeste CSV qui les décrit reste versionné. Pour les ajouter malgré tout, retirer les lignes correspondantes de `.gitignore`.
