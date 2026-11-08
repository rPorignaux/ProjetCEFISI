# CEFISI — Dossier de conception (V1, document de travail)

**Projet :** refonte de `www.cefisi.com` — site public, administration des contenus et espace documentaire.
**Équipe :** Mattéo, Romain, Tim.
**Interlocutrice côté client :** Manon Oubekkou, référente métier pour le recueil et la validation.
**Statut :** V1 de travail. Aucune date engagée, aucun développement décidé ; les options techniques sont proposées, pas retenues.
**Sources :** note de cadrage V1, inventaire du site (28 pages relevées dans les sitemaps, 20 pages publiques observées, 65 références CSS), copies locales de 100 médias, dix maquettes Penpot, matrice des droits (52 entrées), journal d'observations.

## 1. Objet du document

Ce document décrit ce que la refonte doit permettre, les difficultés qu'elle soulève, les options techniques envisageables et les décisions qui restent à prendre.

**Pourquoi « dossier de conception » et non « cahier des charges » :** un cahier des charges engage un périmètre stabilisé, un calendrier et un prix. Ici, plusieurs règles de droits ne sont pas arbitrées, le choix de stack n'est pas fait, une partie des fonctions reste à confirmer et aucune date n'est fixée. Le document décrit donc un état de conception, avec ses options et ses inconnues, plutôt qu'un engagement contractuel.

**Le livrable attendu est le site lui-même**, mis en ligne, avec son administration et son espace documentaire. Aucune date n'est fixée : le calendrier dépend des décisions du chapitre 10 et du choix de stack du chapitre 8.

**Ce que ce document ne remplace pas :** les maquettes Penpot restent la référence visuelle ; la matrice des droits reste la référence des permissions, droit par droit.

## 2. Périmètre

### 2.1 Dans le périmètre

| Lot | Contenu | Référence |
|---|---|---|
| A — Site public | Reprise des contenus, nouvelle hiérarchie, gabarit unique, adaptation mobile | Maquettes 01 et 02 |
| B — Authentification | Connexion, déconnexion, réinitialisation du mot de passe | Maquette 03 |
| C — Espace documentaire | Dossiers, dépôt de fichiers, consultation contrôlée | Maquettes 04 et 06 |
| D — Administration des pages | Création de pages, sous-groupes, accès par rôle | Maquette 05 |
| E — Comptes et rôles | Liste des utilisateurs, attribution des rôles | Maquette 07 |
| F — Reprise de l'existant | Contenus, médias, redirections | Inventaire du site |
| G — Administration et exploitation | Profil, groupes, import de comptes, médiathèque, paramètres, journal des actions | Maquettes 07 et 08, compléments à produire |

### 2.2 Hors périmètre

- La plateforme de candidatures `candidatures-cefisi.com` : la refonte conserve un lien vers elle sans refaire la création de compte, les dossiers ni leur traitement.
- La production des textes définitifs et de la charte graphique : le projet fournit le cadre, pas les contenus validés.
- L'exploitation quotidienne : modération, support aux utilisateurs, mise à jour des contenus.

### 2.3 Décisions déjà prises

| Décision | Portée | Source |
|---|---|---|
| Une seule barre latérale pour tout le site | Les pages publiques restent affichées ; les accès de l'espace connecté s'ajoutent dans la même barre | Retour de Romain, maquettes 04 à 07 |
| Les documents sont séparés des pages | Entrée « Documents » visible seulement après connexion, selon le rôle | Maquettes 01, 04 et 06 |
| Les pages sont organisées en sous-groupes | Une page est rattachée ou non à un sous-groupe pour garder un contenu cohérent | Maquette 05 |
| La charte existante est conservée | Logo et bleu ciel relevés sur les supports officiels | Note de cadrage |
| Quatre rôles envisagés | Super-administrateur, administrateur, enseignant, étudiant | Note de cadrage et matrice des droits — à valider |
| Le site fonctionne sur ordinateur, tablette et téléphone | Gabarit responsive | Note de cadrage |
| Les droits sont décrits droit par droit | 52 entrées réparties en cinq domaines, avec une colonne « Décision client » à remplir | `CEFISI-matrice-des-droits.xlsx` |

## 3. Acteurs

| Acteur | Ce qu'il fait | Statut |
|---|---|---|
| Visiteur | Consulte les pages publiques, accède à la candidature externe | Décidé |
| Étudiant | Se connecte, consulte et télécharge les documents autorisés | Décidé, droits à préciser |
| Enseignant | Rôle envisagé ; aucun écran dédié, droits non définis | À confirmer |
| Administrateur | Gère les documents, les dossiers et leurs accès | Décidé |
| Super-administrateur | Crée et organise les pages, gère les comptes | À confirmer (maquette 05) |
| Interlocutrice client | Valide les besoins et les contenus | Hors applicatif |

## 4. Exigences fonctionnelles

### 4.1 Site public — lot A

| Réf | Fonctionnalité | Comportement attendu | Maquette | Statut |
|---|---|---|---|---|
| F-01 | Gabarit commun de page | Barre latérale, en-tête et pied de page identiques sur toutes les pages ; seul le contenu central change | 01 | Décidé |
| F-02 | Pages d'information | Accueil de présentation et pages génériques : formations, approche, équipe, contact | 01 | Décidé |
| F-03 | Affichage mobile | Même contenu et mêmes accès ; barre latérale repliée en tiroir, tableaux transformés en listes | 02 | Décidé |
| F-04 | Bloc « Espace privé » | Depuis la barre latérale, un bouton mène à la connexion ; après connexion, ce bloc devient le compte et la déconnexion | 01 | Décidé |
| F-05 | Accès à la candidature | Bouton vers la plateforme existante, sans ressaisie de compte candidat sur le site | 01 | Décidé, destination à vérifier |
| F-06 | Pied de page et mentions | Coordonnées, liens de confidentialité, logos partenaires et certification | 01 | À reprendre |

### 4.2 Authentification — lot B

| Réf | Fonctionnalité | Comportement attendu | Maquette | Statut |
|---|---|---|---|---|
| F-07 | Connexion | Authentification par courriel et mot de passe, message d'erreur sans indiquer si le compte existe | 03 | Décidé |
| F-08 | Session et déconnexion | Session limitée dans le temps, déconnexion explicite, retour à l'accueil public | 03 | Décidé |
| F-09 | Mot de passe oublié | Lien présent sur l'écran de connexion ; envoi d'un courriel de réinitialisation | 03 | Flux à définir |

### 4.3 Espace documentaire — lot C

| Réf | Fonctionnalité | Comportement attendu | Maquette | Statut |
|---|---|---|---|---|
| F-10 | Dossiers | Création, renommage et déplacement de dossiers et sous-dossiers | 04 | Décidé, règles à confirmer |
| F-11 | Dépôt de fichiers | Dépôt par bouton ou glisser-déposer, avec indication du dossier de destination | 04 | Décidé |
| F-12 | Consultation étudiant | Liste des documents autorisés, filtre par dossier, consultation ou téléchargement | 06 | Décidé |
| F-13 | Recherche et filtre | Recherche par nom de document et filtre par dossier | 06 | Décidé |
| F-14 | Droits par dossier | Choix des rôles autorisés, appliqué côté serveur et pas seulement masqué dans le menu | 04 | Décidé, portée à confirmer |
| F-15 | Actions sur un fichier | Remplacer, retirer ou renommer un document existant | 04 | À confirmer |

### 4.4 Administration des pages — lot D

| Réf | Fonctionnalité | Comportement attendu | Maquette | Statut |
|---|---|---|---|---|
| F-16 | Créer une page | Titre, contenu et enregistrement en brouillon | 05 | Décidé pour un super-utilisateur, rôle à confirmer |
| F-17 | Sous-groupes | Rattachement facultatif à un sous-groupe pour regrouper les pages d'un même contenu | 05 | Décidé |
| F-18 | Accès par rôle | Choix des rôles autorisés à voir la page | 05 | Décidé, règle à valider |
| F-19 | Brouillon et publication | Prévisualisation avant publication, page non publiée invisible du public | 05 | Décidé |
| F-20 | Édition du contenu | Mise en forme simple et insertion de médias | 05 | Modalités à définir |
| F-21 | Modifier ou retirer une page | Reprise d'une page existante, retrait ou archivage | 05 | À confirmer |

### 4.5 Comptes et rôles — lot E

| Réf | Fonctionnalité | Comportement attendu | Maquette | Statut |
|---|---|---|---|---|
| F-22 | Liste des utilisateurs | Entrée « Utilisateurs » dans la barre, liste avec rôle et état du compte | 07 | Maquetté |
| F-23 | Gestion des comptes | Création, désactivation et attribution d'un rôle | 07 | Maquetté, règles à confirmer |

### 4.6 Reprise de l'existant — lot F

| Réf | Fonctionnalité | Comportement attendu | Référence | Statut |
|---|---|---|---|---|
| F-24 | Reprise des contenus | Reprise des pages publiques inventoriées, réécriture si nécessaire, validation par le client | Inventaire des pages | À planifier |
| F-25 | Reprise des médias | Réutilisation des images inventoriées après vérification des droits, versions adaptées au web | 100 fichiers, manifeste | À planifier |
| F-26 | Redirections et référencement | Redirections des anciennes adresses vers les nouvelles, sitemap et métadonnées | Inventaire des URL | À planifier |
| F-27 | Lien vers les candidatures | Adresse de destination vérifiée, ouverture externe conservée | OBS-001 | Décidé |

### 4.7 Administration et exploitation — lot G

| Réf | Fonctionnalité | Comportement attendu | Maquette | Statut |
|---|---|---|---|---|
| F-28 | Profil de l'utilisateur | Consulter et modifier ses coordonnées ; champs modifiables à définir | 07 | À confirmer |
| F-29 | Groupes et promotions | Créer un groupe, y affecter des utilisateurs, effet sur les droits à définir | Aucune | À confirmer |
| F-30 | Import et export des comptes | Importer une liste au format CSV, exporter les comptes existants | Aucune | À confirmer |
| F-31 | Fiche formation | Modèle de page structuré : intitulé, durée, prérequis, programme, appel à candidature | 08 | Maquetté |
| F-32 | Corbeille et historique | Restauration d'une page ou d'un document supprimé, versions précédentes | Aucune | À confirmer |
| F-33 | Menu et navigation | Modifier les entrées de la barre latérale et leur ordre | Aucune | À confirmer |
| F-34 | Médiathèque | Ajouter, remplacer et supprimer les images du site public | Aucune | À confirmer |
| F-35 | Paramètres généraux | Coordonnées, identité visuelle et réglages du site | Aucune | À confirmer |
| F-36 | Rôles et permissions | Configurer les droits par rôle, au-delà des cases cochées par dossier | Aucune | À confirmer |
| F-37 | Journal des actions | Historique des dépôts, publications et changements de droits | Aucune | À confirmer |
| F-38 | Tableau de bord d'administration | Vue d'ensemble : comptes, documents, pages en attente | Aucune | À maquetter |
| F-39 | Suppression d'un compte | Suppression définitive et sort des contenus associés | 07 | À confirmer |

### 4.8 Correspondance avec la matrice des droits

| Domaine de la matrice | Droits | Fonctionnalités |
|---|---|---|
| Site public | 3 | F-02, F-05, F-31 |
| Comptes et accès | 19 | F-07, F-09, F-22, F-23, F-28 à F-30, F-38, F-39 |
| Pages et contenus | 12 | F-16 à F-19, F-21, F-31 à F-34 |
| Intranet et PDF | 14 | F-10 à F-15, F-32 |
| Paramètres et suivi | 4 | F-35 à F-37, NF-07 |
| **Total** | **52** | **Chaque droit est rattaché à une fonctionnalité ou à une exigence** |

La colonne « Réf. dossier » du classeur porte ce rattachement ligne par ligne, à côté de la colonne « Décision client ».

## 5. Exigences non fonctionnelles

Les valeurs chiffrées sont des propositions à valider, pas des engagements.

| Réf | Exigence | Critère vérifiable | Statut |
|---|---|---|---|
| NF-01 | Affichage adaptatif | Lisible et utilisable de 360 px à 1 440 px de large | Décidé |
| NF-02 | Accessibilité | Contrastes conformes, navigation au clavier, textes alternatifs ; niveau visé à définir | À confirmer |
| NF-03 | Performance | Page publique affichée en moins de 2,5 s sur mobile en 4G | Proposition |
| NF-04 | Sécurité des accès | Chaque requête vérifie les droits côté serveur, y compris un lien direct vers un fichier | Décidé |
| NF-05 | Mots de passe | Stockage par hachage fort, aucune trace en clair | Exigence |
| NF-06 | Données personnelles | Données minimales, hébergement et durées de conservation à préciser | À confirmer |
| NF-07 | Sauvegarde | Sauvegarde régulière des contenus, des fichiers et de la base, restauration testée | Proposition |
| NF-08 | Traçabilité | Journal des dépôts, publications et changements de droits | Proposition |
| NF-09 | Référencement | Titres et descriptions par page, sitemap à jour, anciennes adresses redirigées | Décidé |
| NF-10 | Langue et formats | Contenus en français, dates et unités au format français | Décidé |
| NF-11 | Compatibilité | Deux dernières versions de Chrome, Firefox, Safari et Edge | Proposition |
| NF-12 | Maintenabilité | Le client crée et modifie ses pages et ses documents sans intervention dans le code | Décidé |

## 6. Problèmes techniques et difficultés

| Réf | Difficulté | Pourquoi elle est réelle ici | Impact | Piste | État |
|---|---|---|---|---|---|
| T-01 | Reconstruction et reprise | Le site actuel est un WordPress avec un thème commercial et des extensions visibles dans les adresses ; la refonte est un redéveloppement intégral | Reprise des contenus, adresses et médias sans reconduire le thème ni les extensions | Préparer les exports et une table de correspondance entre anciennes et nouvelles pages | Décidé, reprise à planifier |
| T-02 | Droits réellement appliqués | Masquer un lien dans la barre ne protège rien : un fichier reste accessible par son adresse | Fuite de documents pédagogiques | Contrôle côté serveur sur chaque requête, liens signés pour les fichiers | Décidé, à vérifier en recette |
| T-03 | Stockage des fichiers | Volume et taille des PDF, types autorisés, quotas, analyse antivirus | Saturation, dépôt de fichier indésirable | Limites explicites et analyse à l'entrée | À définir |
| T-04 | Diffusion des documents | Un PDF déposé dans un répertoire public est lisible par tous | Contournement des droits | Diffusion contrôlée, sans répertoire public, cache maîtrisé | Décidé |
| T-05 | Contenus et médias | 100 fichiers récupérés pour 102 références, dont deux références CSS qui renvoient du HTML | Images manquantes ou de mauvaise qualité après reprise | Vérifier chaque média, produire les variantes utiles | Connu et chiffré |
| T-06 | Droits de réutilisation | Les copies locales ne prouvent pas le droit de rediffuser les images et logos | Risque juridique à la publication | Valider avec le client, remplacer ce qui n'est pas autorisé | À vérifier |
| T-07 | Pages privées non explorées | Une dizaine d'adresses renvoient vers la connexion sans session ouverte | Inventaire potentiellement incomplet : contenus et fonctions oubliés | Inventaire complété avec le client ou un compte de test | Connu |
| T-08 | Éditeur de pages | Le client doit créer des pages sans code, avec mise en forme et médias | Un éditeur trop pauvre ramène l'équipe au code | Choisir un éditeur, définir les blocs autorisés | À définir |
| T-09 | Arborescence et cohérence | Pages, sous-groupes et navigation doivent rester compréhensibles quand le nombre de pages augmente | Navigation incohérente, pages orphelines | Règles de nommage, aperçu de la structure avant publication | Maquetté |
| T-10 | Authentification et comptes | Politique de mot de passe, réinitialisation, session, éventuel lien avec les comptes de candidature | Comptes faibles ou support envahi par les demandes | Flux de réinitialisation clair, règles de mot de passe | À définir |
| T-11 | Reprise des comptes existants | On ne sait pas combien de comptes existent ni ce qu'ils contiennent | Perte d'accès pour des utilisateurs actuels | Inventaire des comptes avec le client | À vérifier |
| T-12 | Redirections | Changement de structure d'adresses sans redirection = pages perdues | Perte de référencement et de visiteurs | Table de redirections établie avant la mise en ligne | À planifier |
| T-13 | Disponibilité du site actuel | Des indisponibilités ont été signalées, sans diagnostic | Reprise de contenu et recette perturbées | Fenêtres de travail prévues, ne pas dépendre du site en direct | Signalé, non diagnostiqué |
| T-14 | Recherche interne | Une recherche mène aujourd'hui à une page de connexion sans possibilité apparente de se connecter | Confusion des visiteurs | Décider maintien, correction ou retrait | Signalé, à reproduire |
| T-15 | Environnements et recette | Sans environnement de test séparé, chaque essai se fait sur le site en ligne | Risque de casser la production | Prévoir un environnement de recette et un jeu de données | À définir |
| T-16 | Sauvegarde et restauration | Une refonte change la base et les fichiers ; sans sauvegarde testée, un incident est définitif | Perte de contenus | Sauvegarde avant bascule, restauration vérifiée | À définir |

## 7. Critères de recette

| Lot | Ce qui doit être vérifié |
|---|---|
| A — Site public | Parcours complet depuis l'accueil, barre latérale identique partout, pages génériques au même gabarit, affichage mobile, lien de candidature fonctionnel |
| B — Authentification | Connexion valide et invalide, message d'erreur neutre, déconnexion, réinitialisation reçue par courriel |
| C — Espace documentaire | Création de dossier, dépôt d'un fichier, visibilité par rôle, refus d'un lien direct non autorisé, téléchargement |
| D — Administration des pages | Création d'une page, rattachement à un sous-groupe, accès limité à un rôle, brouillon invisible avant publication |
| E — Comptes et rôles | Attribution d'un rôle, effet immédiat des droits, désactivation d'un compte |
| F — Reprise de l'existant | Aucune adresse inventoriée ne renvoie une erreur, médias affichés, métadonnées présentes |
| G — Administration | Modification des paramètres, ajout d'un média, import d'une liste de comptes, journal consultable |
| Transverse | Contrastes et navigation clavier, sauvegarde restaurée, journal des actions consultable |

## 8. Choix du langage, du framework et de la base de données

La refonte est une reconstruction complète : WordPress n'est pas conservé. Le choix porte donc sur quatre éléments — langage, framework front, framework back, base de données. Les options sont comparées problème par problème plutôt que par préférence de marque.

### 8.1 Les problèmes que chaque stack devra résoudre

| Réf | Problème | Ce qu'il implique concrètement |
|---|---|---|
| P1 | Authentification et sessions | Connexion, mot de passe oublié, session limitée dans le temps, protection des formulaires |
| P2 | Autorisations par rôle et par objet | Décider qui voit quel dossier, quel fichier, quelle page, et le vérifier à chaque requête |
| P3 | Diffusion contrôlée des fichiers | Servir un PDF sans adresse publique, avec contrôle du droit et cache maîtrisé |
| P4 | Dépôt de fichiers | Envoi de PDF de plusieurs mégaoctets, limites, reprise, contrôle du type réel |
| P5 | Éditeur de pages | Mise en forme, images, sans code, sans casser le gabarit |
| P6 | Arborescence et adresses | Pages, sous-groupes, adresses lisibles, redirections des anciennes URL |
| P7 | Recherche | Documents et pages, accents et fautes de frappe tolérées, réponse rapide |
| P8 | Modèle de données et types | Un seul modèle décrit côté base, serveur et interface, migrations suivies |
| P9 | Tests et recette | Tests automatisés, jeu de données, parcours complet rejouable |
| P10 | Déploiement et exploitation | Mise en ligne, migrations, journaux, sauvegardes, retour arrière |
| P11 | Performance et référencement | Pages rapides sur mobile, métadonnées, sitemap, contenu indexable |
| P12 | Écosystème et support | Documentation, bibliothèques maintenues, personnes capables de reprendre |

### 8.2 Les quatre candidats

| Option | Langage | Front | Back | Base |
|---|---|---|---|---|
| A | TypeScript | Next.js, App Router | même application, server actions | PostgreSQL |
| B | TypeScript | React + Vite | NestJS | PostgreSQL |
| C | PHP | Twig, ou Inertia + React | Symfony | PostgreSQL |
| D | Python | gabarits Django, ou React | Django | PostgreSQL |

Une cinquième famille, Java et Spring, n'est pas retenue : elle ajoute une chaîne d'outils et un temps de mise en route sans bénéfice pour un site de 28 pages et une bibliothèque documentaire.

### 8.3 Facilité de traitement, problème par problème

Légende : ●●● problème réglé par une bibliothèque mature, peu de code ; ●●○ solution existante mais qui demande du code ou de la configuration ; ●○○ à écrire soi-même, ou hors du cadre de l'outil.

| Réf | Problème | A — Next.js | B — React + NestJS | C — Symfony | D — Django |
|---|---|---|---|---|---|
| P1 | Authentification et sessions | ●●○ | ●●● | ●●● | ●●● |
| P2 | Autorisations par rôle et par objet | ●●○ | ●●● | ●●● | ●●○ |
| P3 | Diffusion contrôlée des fichiers | ●●● | ●●● | ●●● | ●●○ |
| P4 | Dépôt de fichiers volumineux | ●●○ | ●●● | ●●● | ●●○ |
| P5 | Éditeur de pages | ●●○ | ●●○ | ●●● | ●●● |
| P6 | Arborescence et adresses | ●●● | ●●○ | ●●● | ●●● |
| P7 | Recherche | ●●● | ●●● | ●●○ | ●●● |
| P8 | Modèle de données et types | ●●● | ●●● | ●○○ | ●○○ |
| P9 | Tests et recette | ●●○ | ●●● | ●●● | ●●● |
| P10 | Déploiement et exploitation | ●●● | ●●○ | ●●○ | ●●○ |
| P11 | Performance et référencement | ●●● | ●●○ | ●●● | ●●● |
| P12 | Écosystème et support | ●●● | ●●● | ●●○ | ●●○ |

Ces appréciations sont qualitatives et doivent être confrontées aux compétences réelles de l'équipe : elles disent ce que l'écosystème facilite, pas ce que trois personnes savent faire en trois mois.

### 8.4 Lecture par option

**A — TypeScript de bout en bout.** Un seul modèle de types traverse la base, le serveur et l'interface ; le routage par segments couvre l'arborescence et les adresses lisibles ; le déploiement tient en un service. En revanche, l'authentification et les autorisations par objet se composent à la main à partir de briques distinctes : c'est là que se concentrera l'essentiel du travail de rigueur.

**B — React et NestJS séparés.** Les guards, la validation et la structure par modules rendent les droits et les sessions plus directs à écrire. Le prix est double : deux bases de code, un contrat d'API à maintenir, deux déploiements à surveiller.

**C — Symfony.** Le framework fournit les formulaires, la sécurité, les voters et un éditeur riche éprouvé. Il souffre sur le partage de types avec l'interface et sur un écosystème front qui évolue moins vite.

**D — Django.** Authentification, permissions, administration et recherche plein texte sont fournies. Les types ne traversent pas jusqu'à l'interface, et la modernisation du front demande soit de composer avec les gabarits, soit d'ajouter une application séparée.

### 8.5 Base de données

**PostgreSQL, dans les quatre options.** Il apporte l'indexation plein texte en français avec suppression des accents, la recherche approximative par trigrammes pour les fautes de frappe, des colonnes JSON pour le contenu structuré des pages, et une sécurité au niveau des lignes qui peut servir de filet sous les contrôles applicatifs. MySQL reste acceptable si l'hébergeur l'impose, avec une recherche plein texte plus pauvre sur les accents. SQLite est écarté : écritures concurrentes et recherche insuffisante pour une bibliothèque partagée.

### 8.6 Classement

| Option | Points de facilité | Cohérence du code | Coût de mise en route | Verdict |
|---|---|---|---|---|
| A — Next.js + PostgreSQL | 31 sur 36 | Un seul langage, une seule base de code | Un seul service à déployer | Recommandé |
| B — React + NestJS | 32 sur 36 | Deux bases de code, un contrat d'API | Deux services, plus de structure à écrire | Alternative solide |
| C — Symfony | 31 sur 36 | Deux langages si le front est en React | Cadre complet, moins de décisions à prendre | Si l'équipe est PHP |
| D — Django | 29 sur 36 | Deux langages si le front est en React | Cadre complet, front à moderniser | Si l'équipe est Python |

B obtient un point de plus que A sur la facilité brute : ses guards et sa structure de modules règlent plus directement les droits et les sessions. A reste recommandé parce qu'un seul langage, un seul modèle de types et un seul déploiement comptent davantage sur un projet de cette taille. Si l'équipe préfère séparer nettement le front et le back, B est un choix légitime et non un pis-aller.

### 8.7 Recommandation

**Option A — Next.js, TypeScript et PostgreSQL**, pour quatre raisons : un seul langage et un seul modèle de types entre la bibliothèque documentaire, l'éditeur de pages et l'interface ; le routage par segments correspond directement à l'arborescence pages et sous-groupes ; le déploiement d'un seul service simplifie l'exploitation d'une petite équipe ; PostgreSQL couvre la recherche et le stockage structuré sans service supplémentaire.

Le choix se renverse si l'audit des compétences montre que personne n'est à l'aise avec TypeScript : dans ce cas C ou D sont préférables à une stack que l'équipe découvrirait en même temps que le projet.

### 8.8 Ce que ce chapitre ne tranche pas

- Les compétences réelles de l'équipe, qui départagent A, B, C et D autant que les critères techniques.
- L'hébergement disponible, son coût et la personne qui l'administre.
- Qui maintient le site après la livraison.
- Le détail de l'outillage : Prisma ou Drizzle pour l'ORM, Tailwind ou CSS classique, bibliothèque de composants.

## 9. Suivi du projet et outils

| Outil | Usage | État |
|---|---|---|
| Trello | Suivi des tâches : « En attente » pour les tâches futures, « En cours — prochain sprint » pour celles à présenter au prochain point | Tableau privé `https://trello.com/b/2o9z11DF/refonte-du-site-cefisi` |
| Penpot | Maquettes et gabarit commun ; dix écrans : accueil bureau et mobile, fiche formation, connexion, administration, création de page, gestion des utilisateurs, consultation étudiante et sa version mobile, états vides et messages | Exports PNG dans `docs/maquettes/` |
| Inventaire du site | Pages, utilité, médias par page, références CSS | Word et Excel dans `docs/inventaire/` |
| Médias | 100 fichiers copiés localement, manifeste avec adresse source et empreinte, archive ZIP non versionnée (droits de diffusion non établis) | Manifeste dans `docs/medias/site-actuel/` |
| Matrice des droits | 52 droits par domaine et par rôle, colonne « Décision client » à remplir | `docs/matrice/` ; à arbitrer avec le client |
| Versionnage du projet | Dépôt Git ouvert ; documents et maquettes versionnés, scripts locaux non versionnés | À utiliser pour les futurs développements |

Le tableau Trello ne remplace ni l'inventaire, qui est un catalogue de pages, ni la matrice des droits, qui est un tableau d'arbitrage. Chacun a un rôle distinct.

## 10. Décisions à prendre

### 10.1 Rôles

La matrice des droits sert de base : chaque ligne porte déjà une proposition pour les quatre rôles. Restent à trancher les points qu'elle signale explicitement.

- Qui crée les pages : super-administrateur, administrateur, ou les deux ?
- Un utilisateur peut-il cumuler plusieurs rôles ?
- Que voit un enseignant : quels dossiers, quelles pages ?
- Qui valide la publication d'une page ?
- Qui attribue les rôles et gère les comptes ?
- L'accès à l'intranet se confond-il avec l'existence du compte, ou s'agit-il de deux droits distincts ?

### 10.2 Fonctionnalités

- Maintien ou retrait de la recherche interne, dont le comportement signalé renvoie à la page de connexion.
- Une page publiée doit-elle être validée par une seconde personne ?
- Un document peut-il être remplacé par une nouvelle version, ou seulement déposé puis retiré ?
- Faut-il un aperçu intégré des PDF ou un simple téléchargement ?
- Le contact se fait-il par formulaire ou par coordonnées affichées ?
- La réinitialisation du mot de passe passe-t-elle par un envoi de courriel ?

### 10.3 Technique et exploitation

- Quelle option de stack retenir : A, B, C ou D (chapitre 8) ?
- Qui héberge, qui sauvegarde, qui met à jour ?
- Un environnement de recette séparé est-il prévu (T-15) ?
- Faut-il reprendre les comptes existants du site actuel (T-11) ?
- Quelle durée de conservation pour les journaux et les documents ?

Chaque décision sera reprise dans l'espace de décisions, avec les options, leurs conséquences et une recommandation.
