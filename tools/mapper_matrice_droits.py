"""Rattacher chaque droit de la matrice CEFISI à une fonctionnalité du dossier.

Ouvre livrables/CEFISI-matrice-des-droits.xlsx, insère (ou met à jour) la
colonne « Réf. dossier » juste avant « Décision client », et vérifie que les
52 droits sont couverts par une fonctionnalité ou une exigence existante.

Le rattachement est déclaré ici, ligne par ligne, dans l'ordre du classeur :
chaque entrée porte le début du libellé du droit, ce qui fait échouer le
script si l'ordre du classeur change.
"""
from __future__ import annotations

import sys
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
MATRICE = ROOT / "livrables" / "CEFISI-matrice-des-droits.xlsx"
DOSSIER = ROOT / "docs" / "cadrage" / "dossier-de-conception-v1.md"

# (début du libellé du droit, référence du dossier)
RATTACHEMENTS = [
    ("Consulter les pages publiques", "F-02"),
    ("Consulter l’offre et les fiches de formation", "F-02, F-31"),
    ("Accéder au lien", "F-05"),
    ("Se connecter à son espace", "F-07"),
    ("Consulter son propre profil", "F-28"),
    ("Modifier ses coordonnées", "F-28"),
    ("Changer ou réinitialiser son mot de passe", "F-09"),
    ("Accéder au tableau de bord du site", "F-38"),
    ("Consulter la liste des utilisateurs", "F-22"),
    ("Consulter la fiche d’un autre utilisateur", "F-23"),
    ("Créer ou inviter un étudiant", "F-23"),
    ("Créer ou inviter un enseignant", "F-23"),
    ("Créer ou inviter un administrateur", "F-23"),
    ("Modifier la fiche d’un autre utilisateur", "F-23"),
    ("Attribuer ou modifier un rôle", "F-23"),
    ("Donner l’accès à l’intranet à un étudiant", "F-23"),
    ("Retirer l’accès à l’intranet à un étudiant", "F-23"),
    ("Désactiver ou réactiver un compte", "F-23"),
    ("Supprimer un compte", "F-39"),
    ("Créer ou modifier un groupe ou une promotion", "F-29"),
    ("Affecter un utilisateur à un groupe ou une formation", "F-29"),
    ("Importer ou exporter une liste d’utilisateurs", "F-30"),
    ("Créer une page", "F-16"),
    ("Modifier une page", "F-21"),
    ("Prévisualiser une page en brouillon", "F-19"),
    ("Publier ou dépublier une page", "F-19"),
    ("Archiver ou supprimer une page", "F-21"),
    ("Restaurer une version de page", "F-32"),
    ("Consulter une page privée hors bibliothèque de PDF", "F-18"),
    ("Définir la visibilité d’une page privée", "F-18"),
    ("Créer ou modifier une fiche formation", "F-31"),
    ("Modifier le menu et les liens de navigation", "F-33"),
    ("Ajouter ou remplacer un média du site public", "F-34"),
    ("Supprimer un média du site public", "F-34"),
    ("Accéder à la bibliothèque pédagogique", "F-14"),
    ("Parcourir les dossiers auxquels on a accès", "F-12"),
    ("Consulter un PDF pédagogique", "F-12"),
    ("Télécharger un PDF pédagogique", "F-12"),
    ("Créer un dossier de ressources", "F-10"),
    ("Renommer ou déplacer un dossier", "F-10"),
    ("Supprimer ou restaurer un dossier", "F-10, F-32"),
    ("Déposer un PDF de cours, TD ou TP", "F-11"),
    ("Renommer, déplacer ou reclasser un PDF", "F-15"),
    ("Remplacer le fichier PDF d’une ressource", "F-15"),
    ("Retirer ou supprimer un PDF", "F-15"),
    ("Restaurer un PDF supprimé ou une version précédente", "F-32"),
    ("Publier ou masquer un PDF pour les étudiants", "F-14"),
    ("Définir les droits sur un dossier ou un PDF", "F-14"),
    ("Modifier les paramètres généraux du site", "F-35"),
    ("Configurer les rôles et leurs permissions", "F-36"),
    ("Consulter l’historique des actions administratives", "F-37"),
    ("Gérer les sauvegardes et la restauration du site", "NF-07"),
]

ENTETE = "Réf. dossier"


def references_du_dossier() -> set[str]:
    """Identifiants F-xx et NF-xx déclarés dans le dossier de conception."""
    import re

    texte = DOSSIER.read_text(encoding="utf-8")
    return set(re.findall(r"^\| ((?:F|NF)-\d+) \|", texte, flags=re.MULTILINE))


def main() -> int:
    wb = load_workbook(MATRICE)
    ws = wb.active
    entetes = [ws.cell(row=7, column=c).value for c in range(1, ws.max_column + 1)]
    if "Droit ou action" not in entetes or "Décision client" not in entetes:
        print("En-têtes inattendus :", entetes)
        return 1
    col_decision = entetes.index("Décision client") + 1
    col_ref = col_decision
    if ENTETE in entetes:
        col_ref = entetes.index(ENTETE) + 1
    else:
        ws.insert_cols(col_decision)
        ws.cell(row=7, column=col_decision, value=ENTETE)
        ws.column_dimensions[get_column_letter(col_decision)].width = 14.0

    premiere = 8
    lignes = [r for r in range(premiere, ws.max_row + 1) if ws.cell(row=r, column=2).value]
    if len(lignes) != len(RATTACHEMENTS):
        print(f"{len(lignes)} droits dans le classeur, {len(RATTACHEMENTS)} rattachements déclarés")
        return 1

    connus = references_du_dossier()
    inconnues = set()
    for rang, (ligne, (debut, ref)) in enumerate(zip(lignes, RATTACHEMENTS), start=1):
        libelle = str(ws.cell(row=ligne, column=2).value or "")
        if not libelle.startswith(debut):
            print(f"Ligne {ligne} : attendu « {debut} », trouvé « {libelle} »")
            return 1
        connus_ligne = {r.strip() for r in ref.split(",")}
        inconnues |= {r for r in connus_ligne if r not in connus}
        cellule = ws.cell(row=ligne, column=col_ref, value=ref)
        cellule.font = Font(size=9)
        cellule.alignment = Alignment(horizontal="center", vertical="center")

    if inconnues:
        print("Références absentes du dossier :", sorted(inconnues))
        return 1

    entete = ws.cell(row=7, column=col_ref)
    entete.value = ENTETE
    entete.font = Font(bold=True, color="FFFFFF")
    entete.fill = PatternFill("solid", fgColor="12304A")
    entete.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    if ws.cell(row=3, column=1).value and "Réf. dossier" not in str(ws.cell(row=3, column=1).value):
        ws.cell(row=3, column=1).value = (
            str(ws.cell(row=3, column=1).value).rstrip()
            + " La colonne « Réf. dossier » rattache chaque droit à une fonctionnalité du dossier de conception."
        )

    wb.save(MATRICE)
    couverts = {r.strip() for _, ref in RATTACHEMENTS for r in ref.split(",")}
    print(f"{len(RATTACHEMENTS)} droits rattachés • {len(couverts)} références distinctes")
    print("références :", ", ".join(sorted(couverts)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
