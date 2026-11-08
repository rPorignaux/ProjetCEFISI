# Copies locales des médias du site actuel

Les liens et la provenance figurent dans `livrables/inventaire-site-cefisi.xlsx` ; `manifest.csv` consigne les téléchargements réels et leurs échecs. Seules les lignes avec un chemin `fichier_local` et un état « téléchargé », « copié » ou « déjà présent » correspondent à un fichier présent.

Collecte du 8 novembre 2026 : 100 fichiers image rangés pour 102 références de l'inventaire, provenant de 93 URL distinctes téléchargées. Deux références d'icônes CSS (`owl.video.play.png` et `mCSB_buttons.png`) ont répondu avec une page HTML plutôt qu'une image ; elles sont conservées comme échecs dans le manifeste, sans faux fichiers image.

Le script `tools/telecharger_medias_site.py` répartit les médias publics dans `pages/<page>/`, `communs/<zone>/` et `css/<composant>/`. Les images seulement référencées par le CSS ne sont pas nécessairement visibles sur le site. Les espaces réservés ne sont pas téléchargés par ce script.

Pour reprendre lorsque le site répond à nouveau, lancer depuis la racine du dossier :

```text
python tools/telecharger_medias_site.py
```

Les droits de reproduction ou de diffusion des médias doivent être vérifiés avant toute publication des copies dans un dépôt partagé ou public.
