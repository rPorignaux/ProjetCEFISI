# Refonte du site CEFISI

Projet de refonte de `www.cefisi.com` : site public, administration des contenus et espace documentaire pour les étudiants et l'équipe pédagogique.

**Équipe :** Mattéo, Romain, Tim. **Interlocutrice côté client :** Manon Oubekkou.
**État :** conception. Aucun développement n'a commencé, aucune date n'est fixée.

La plateforme de candidatures `candidatures-cefisi.com` reste **hors périmètre** : le nouveau site y renvoie par un lien, sans reprendre la création de compte ni le traitement des dossiers.

---

## Documents du projet

Tous les documents publiés sont rangés dans `docs/` :

| Répertoire | Contenu | Formats |
|---|---|---|
| `docs/cadrage/` | Note de cadrage V1 | Markdown, Word, PDF |
| `docs/conception/` | Dossier de conception : périmètre, 39 fonctionnalités, 16 difficultés techniques, critères de recette, choix de stack et décisions à prendre | Markdown, Word, PDF |
| `docs/observations/` | Journal d'observations et relevés du site public | Markdown, Word, JSON |
| `docs/inventaire/` | Inventaire des pages, de leur utilité et de leurs médias | Word, Excel |
| `docs/maquettes/` | Dix écrans de référence exportés depuis Penpot et leur index | PNG, Markdown |
| `docs/matrice/` | Matrice de 52 droits par domaine et par rôle, rattachée au dossier de conception | Excel |
| `docs/medias/site-actuel/` | Manifeste et bilan des médias copiés du site actuel ; images conservées localement seulement | CSV, JSON, Markdown |
| `docs/pilotage/` | Notes initiales de suivi ; les tâches vivantes sont sur Trello | Markdown |

`docs/medias/medias-site-actuel-cefisi.zip` est une archive locale **non versionnée**. Les scripts `tools/` sont également conservés localement et **exclus de Git** : un clone du dépôt ne contient pas les générateurs.

## Ce que disent les chiffres

| Donnée | Valeur | Source |
|---|---|---|
| Pages relevées dans les sitemaps | 28 (25 pages, 2 articles, 1 catégorie) | `docs/observations/site-audit.json` |
| Pages publiques observées | 20, plus 4 derrière une connexion et 4 non visitées | idem |
| Références d'images dans les CSS | 65 | `docs/observations/site-css.json` |
| Médias | 102 références, 100 fichiers récupérés localement | `docs/medias/site-actuel/manifest.csv` |
| Droits décrits dans la matrice | 52, sur 5 domaines | `docs/matrice/` |
| Fonctionnalités, difficultés, exigences | 39, 16, 12 | `docs/conception/` |

Les fichiers Word et PDF sont des versions de lecture. Les sources Markdown du cadrage et de la conception sont à côté d'eux. Les scripts locaux qui ont servi à produire ces fichiers ne font pas partie du dépôt.

## Suivi

Le suivi des tâches est un tableau Trello privé : <https://trello.com/b/2o9z11DF/refonte-du-site-cefisi>.
« En attente » regroupe les tâches futures, « En cours — prochain sprint » celles à présenter au prochain point. Ce tableau ne remplace ni l'inventaire, qui est un catalogue, ni la matrice des droits, qui sert à arbitrer.

## Limites connues

- **L'espace privé du site actuel n'a pas été exploré** : les adresses réservées répondent par une redirection vers la connexion. L'inventaire ne couvre que le public.
- **Les droits de diffusion des images ne sont pas vérifiés.** Les copies locales servent au travail interne ; leur publication demande l'accord du client.
- Les contenus des maquettes sont **fictifs** et signalés comme tels dans chaque écran.
- Les signalements d'indisponibilité du site et de recherche défaillante viennent du groupe, sans diagnostic.

## Ce qui n'est pas versionné

Les copies d'images du site actuel (`docs/medias/site-actuel/pages/`, `communs/`, `css/`) et l'archive ZIP dans `docs/medias/` ne sont pas versionnées : contenus tiers dont les droits de rediffusion ne sont pas établis. Le manifeste CSV et le bilan JSON restent versionnés. `tools/` est ignoré et n'est pas envoyé sur GitHub. Ces fichiers sont conservés sur cette machine ; ils n'apparaîtront pas dans un clone du dépôt.
