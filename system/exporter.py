import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


OUTPUT_DIR = "outputs"


def _ensure_output_dir():
    """Crée le dossier outputs/ s'il n'existe pas."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def exporter_csv(resultats):
    """
    Exporte la liste de résultats en fichier CSV.

    Paramètre:
        resultats (list[dict]) : liste de dicts enrichis avec email_genere

    Retourne:
        str : chemin vers le fichier CSV généré
    """
    _ensure_output_dir()
    chemin = os.path.join(OUTPUT_DIR, "resultats.csv")

    df = pd.DataFrame(resultats)

    # Réordonner les colonnes pour que email_genere soit en dernier
    colonnes = [col for col in df.columns if col != "email_genere"] + ["email_genere"]
    df = df[colonnes]

    df.to_csv(chemin, index=False, encoding="utf-8-sig")  # utf-8-sig pour Excel français
    return chemin


def exporter_pdf(resultats):
    """
    Exporte la liste de résultats en fichier PDF — une section par entreprise.

    Paramètre:
        resultats (list[dict]) : liste de dicts enrichis avec email_genere

    Retourne:
        str : chemin vers le fichier PDF généré
    """
    _ensure_output_dir()
    chemin = os.path.join(OUTPUT_DIR, "resultats.pdf")

    # Créer le document
    doc = SimpleDocTemplate(
        chemin,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    elements = []

    for i, entreprise in enumerate(resultats):
        nom = entreprise.get("nom_entreprise", "Entreprise inconnue")
        secteur = entreprise.get("secteur", "")
        site = entreprise.get("site_web", "")
        email = entreprise.get("email_genere", "Aucun email généré.")

        # Nom de l'entreprise — titre
        elements.append(Paragraph(nom, styles["Title"]))

        # Secteur + site en sous-titre
        sous_titre = f"Secteur : {secteur}"
        if site:
            sous_titre += f" — {site}"
        elements.append(Paragraph(sous_titre, styles["Italic"]))

        # Espace
        elements.append(Spacer(1, 0.4 * cm))

        # Email généré — on remplace les sauts de ligne par des balises HTML
        email_html = email.replace("\n", "<br/>")
        elements.append(Paragraph(email_html, styles["Normal"]))

        # Séparateur entre les entreprises (sauf la dernière)
        if i < len(resultats) - 1:
            elements.append(Spacer(1, 1.2 * cm))
            elements.append(Paragraph("<hr/>", styles["Normal"]))
            elements.append(Spacer(1, 0.8 * cm))

    doc.build(elements)
    return chemin