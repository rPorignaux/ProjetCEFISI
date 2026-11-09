# CEFISI — Note de cadrage (V1, à valider)

**Projet :** refonte du site public `www.cefisi.com` avec administration du contenu et espace documentaire étudiant.  
**Équipe :** Mattéo, Romain, Tim, Cal-Sebastien — répartition des responsabilités **à compléter collectivement**.

**Interlocutrice côté client :** Manon Oubekkou (référente métier pour le recueil et la validation des besoins ; rôle formel à confirmer).  
**Statut :** document de travail ; les droits précis et les choix techniques ne sont pas arrêtés.

## Objectif

Moderniser le site d’information CEFISI sans reproduire à l’identique l’interface actuelle, tout en conservant sa charte graphique et ses contenus pertinents. Le site doit fonctionner sur ordinateur, tablette et téléphone. L’équipe côté client doit pouvoir créer et modifier des pages sans intervention dans le code. Un espace distinct doit permettre de déposer des PDF pédagogiques, puis de les consulter ou télécharger selon les droits accordés.

## Périmètre retenu pour la proposition

1. **Site public :** inventaire et reprise des informations du site actuel, nouvelle hiérarchie des pages, présentation des formations et accès visible à la candidature. Les textes, images, références graphiques et dates de formation seront relevés puis vérifiés avant réemploi.
2. **Administration :** tableau de bord pour créer et modifier des pages, gérer des utilisateurs et organiser le dépôt de documents pédagogiques. Les règles de publication et d’attribution des droits restent à valider.
3. **Intranet étudiant :** dossiers contenant des PDF de cours, TD et TP ; accès réservé aux étudiants autorisés pour consultation et téléchargement, sans modification ni suppression des documents par les étudiants.
4. **Candidatures :** conserver une redirection vers la plateforme existante `candidatures-cefisi.com`. Ne pas refaire la création de compte candidat, les dossiers ni leur traitement.

## Contraintes et hypothèses à vérifier

- **Graphisme :** conserver la charte, notamment le bleu ciel ; relever le logo et les couleurs exactes sur les supports officiels. La proposition graphique n’est pas une charte validée.
- **Accès :** quatre rôles sont envisagés : super-administrateur, administrateur, enseignant, étudiant. Le principe d’accès étudiant aux ressources sans droit de modification est retenu ; les permissions détaillées restent à valider dans une matrice.
- **Protection :** séparer les pages publiques des documents privés ; la faisabilité devra expliquer la vérification des droits côté serveur, y compris pour un lien direct vers un PDF. Ne déposer aucun vrai dossier de candidature ni document pédagogique privé dans un dépôt public.
- **Lien de candidature :** préserver le parcours vers la plateforme existante ; vérifier l’adresse finale et les liens propres aux formations dans l’inventaire du site.

## Points à préciser

Les responsabilités de l’équipe, les droits exacts par rôle, les contenus à reprendre et les contraintes d’hébergement restent à définir. Les observations et questions émergentes seront consignées dans le journal de projet, puis validées progressivement avec l’interlocutrice côté client.
