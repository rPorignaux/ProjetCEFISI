# Maquettes de référence

Dix écrans exportés depuis le fichier Penpot « CEFISI · Parcours & interfaces ». Les contenus, noms de fichiers et coordonnées sont **fictifs** et servent à juger la structure, pas le contenu définitif.

| Fichier | Écran | Ce qu'il montre | Statut |
|---|---|---|---|
| `01-accueil-public-bureau.png` | Accueil public, bureau | Gabarit de page : barre latérale unique, hero de présentation, trois blocs, bande des formations, bloc « Espace privé » | Décidé |
| `02-accueil-public-mobile.png` | Accueil public, mobile | Même contenu, barre latérale repliée en tiroir | Décidé |
| `03-connexion.png` | Connexion | Volet de marque, formulaire, mot de passe oublié, retour au site public | Décidé |
| `04-administration-documents.png` | Administration, documents | Dossiers, dépôt de fichiers, panneau d'accès par rôle | Décidé, portée des droits à confirmer |
| `05-creer-une-page.png` | Créer une page | Titre, contenu, rattachement à un sous-groupe, accès par rôle, brouillon | Décidé, rôle autorisé à confirmer |
| `06-etudiant-documents.png` | Étudiant, documents | Recherche, filtre par dossier, cartes de dossiers, liste de fichiers | Décidé |
| `07-gestion-utilisateurs.png` | Administration, utilisateurs | Liste des comptes, invitation, rôle sélectionné, cartes de rôles | Décidé, règles à confirmer |
| `08-fiche-formation.png` | Fiche formation | Modèle de page générique appliqué à une formation, encart de candidature | Décidé |
| `09-etats-vides-et-messages.png` | États vides et messages | Aucun document, recherche sans résultat, accès refusé, dépôt impossible, messages système | À intégrer aux écrans |
| `10-etudiant-mobile.png` | Étudiant, mobile | Même coque sur téléphone : recherche, dossiers, fichiers récents | Décidé |

## Règles communes

- **Une seule barre latérale** sur tout le site. Après connexion, les accès de l'espace documentaire s'ajoutent dans cette même barre ; il n'y a pas de seconde mise en page.
- **Une seule coque** : marque, signature, rubriques publiques et fil d'Ariane identiques d'un écran à l'autre.
- **Les sous-groupes** regroupent les pages d'un même contenu, par exemple `Pages › Formations › MOA en SI`.
- Les écrans 09 et 10 complètent les huit premiers : les états vides sont les premiers écrans vus par un nouvel utilisateur, et l'espace étudiant doit rester utilisable sur téléphone.

## Régénérer un export

Les écrans vivent dans Penpot (connecteur MCP de l'agent). Chaque export est un PNG à l'échelle du cadre : 1440 × 900 pour les écrans de bureau, 390 × 844 pour le mobile.
