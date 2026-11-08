# Copies locales des médias du site actuel

Les liens et la provenance figurent dans `docs/inventaire/inventaire-site-cefisi.xlsx` ; `manifest.csv` consigne les téléchargements réels et leurs échecs. Seules les lignes avec un chemin `fichier_local` et un état « téléchargé », « copié » ou « déjà présent » correspondent à un fichier présent **sur la machine de collecte**. Les images elles-mêmes ne sont pas versionnées.

Collecte du 8 novembre 2026 : 100 fichiers image rangés pour 102 références de l'inventaire, provenant de 93 URL distinctes téléchargées. Deux références d'icônes CSS (`owl.video.play.png` et `mCSB_buttons.png`) ont répondu avec une page HTML plutôt qu'une image ; elles sont conservées comme échecs dans le manifeste, sans faux fichiers image.

Un script local non versionné répartit les médias publics dans `pages/<page>/`, `communs/<zone>/` et `css/<composant>/`. Les images seulement référencées par le CSS ne sont pas nécessairement visibles sur le site. Les espaces réservés n'ont pas été téléchargés.

Un clone du dépôt ne contient ni ce script, ni les fichiers image locaux, ni l'archive ZIP ; le manifeste reste disponible pour la traçabilité.

Les droits de reproduction ou de diffusion des médias doivent être vérifiés avant toute publication des copies dans un dépôt partagé ou public.
