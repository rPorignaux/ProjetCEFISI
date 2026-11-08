# Journal d’observations — site CEFISI

Ce fichier distingue les faits constatés, les signalements du groupe et les hypothèses. Ajouter la date, l’URL ou le parcours, la source de l’observation, le résultat obtenu et ce qui reste à vérifier. Éviter les données personnelles et les captures de zones privées.

| ID | Date | Parcours / source | Constat | Statut et suite |
|---|---|---|---|---|
| OBS-001 | 8 novembre 2026 | Accueil public `https://www.cefisi.com/`, consultation sans connexion | L’accueil a pu être ouvert lors d’une première visite. Le bouton « Envoyer ma candidature » contient un lien vers `http://candidatures-cefisi.com/`. | Observé sur la page ; vérifier la redirection finale et la disponibilité du lien, sans créer de compte candidat. |
| OBS-002 | 8 novembre 2026 | Retour de Romain | Le site serait parfois inaccessible. | Signalé par le groupe, non diagnostiqué ; consigner lors du prochain incident l’heure, l’URL, le navigateur, le réseau et le message exact, sans multiplier les tentatives. |
| OBS-003 | 8 novembre 2026 | Retour de Romain, recherche sur le site | Une recherche conduirait à une page de connexion sans possibilité apparente de se connecter. | Signalé par le groupe, non reproduit ici ; relever le terme recherché, l’URL atteinte, les éléments affichés et le résultat sur une session non connectée. Ne pas tester de mots de passe ni forcer l’accès. |
| OBS-004 | 8 novembre 2026 | Nouvelle tentative de chargement de l’accueil dans l’outil de navigation | La navigation a expiré après 5 secondes en attendant la réponse du navigateur automatisé. | Échec de l’outil, **pas une preuve** d’indisponibilité du site ; ne pas confondre avec OBS-002. |
| OBS-005 | 8 novembre 2026 | Relecture de `site-audit.json` après remarque de Romain | Les 288 URL relevées contiennent 220 occurrences de onze mêmes suffixes (`/friends`, `/groups`, `/messages`, `/profile` et leurs sous-pages) répétés à la suite de vingt pages différentes : ce sont les onglets du compte utilisateur du thème, pas des fonctionnalités du site. Quatre adresses seulement existent comme pages — `wiki`, `offres-demploi`, `publier-une-offre-demploi`, `tableau-de-bord-des-offres-demploi` — et répondent toutes par une redirection 302 vers `/login/`. | Fonctionnalités sociales retirées du dossier de conception : aucune n’a été observée. Les quatre adresses restreintes ne sont pas décrites comme des fonctionnalités ; leur contenu reste non exploré (voir T-07). |

## À compléter au fil des visites

- **Pages et contenus :** URL, titre, sections utiles, médias, dernière vérification, droit de réutilisation à confirmer.
- **Charte :** logo, couleurs mesurées, polices, différences ordinateur/mobile/tablette.
- **Parcours :** accès aux formations, candidature, recherche, connexion, intranet public/privé.
- **Questions pour l’interlocutrice côté client :** ajouter une question seulement lorsqu’une observation ou une décision à prendre la motive ; indiquer la réponse et la date de validation.

### Modèle d’entrée

`OBS-XXX — Date et heure — URL/parcours — Contexte (appareil, navigateur, connecté ou non) — Résultat observé — Source/capture — Hypothèse éventuelle — Vérification suivante — Statut.`
