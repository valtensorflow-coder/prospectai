import pandas as pd

COLONNES_OBLIGATOIRES = ["nom_entreprise", "secteur"]
COLONNES_OPTIONNELLES = ["site_web"]

def parse_csv(filepath):
    """
    Lit un fichier CSV et retourne une liste de dicts propres.

    Paramètre:
        filepath (str) : chemin vers le fichier CSV

    Retourne:
        list[dict] : liste d'entreprises, ex:
            [{"nom_entreprise": "Acme", "secteur": "e-commerce", "site_web": "acme.fr"}, ...]

    Lève:
        ValueError : si le fichier est vide ou qu'une colonne obligatoire manque
    """

    # --- 1. Lecture du fichier ---
    try:
        df = pd.read_csv(filepath, encoding="utf-8")
    except UnicodeDecodeError:
        # Fallback si le fichier n'est pas en UTF-8 (ex: export Excel français)
        df = pd.read_csv(filepath, encoding="latin-1")
    except pd.errors.EmptyDataError:
        raise ValueError("Le fichier CSV est vide.")

    # Tentative avec séparateur point-virgule si le CSV semble mal parsé
    if len(df.columns) == 1:
        try:
            df = pd.read_csv(filepath, sep=";", encoding="utf-8")
        except Exception:
            pass

    # --- 2. Vérification des colonnes obligatoires ---
    colonnes_manquantes = [col for col in COLONNES_OBLIGATOIRES if col not in df.columns]
    if colonnes_manquantes:
        raise ValueError(
            f"Colonnes manquantes dans le CSV : {', '.join(colonnes_manquantes)}. "
            f"Colonnes attendues : {', '.join(COLONNES_OBLIGATOIRES)}"
        )

    # --- 3. Nettoyage ---
    # Supprimer les lignes où nom_entreprise ou secteur est vide
    df = df.dropna(subset=COLONNES_OBLIGATOIRES)

    # Supprimer les espaces en début/fin pour les colonnes texte
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.strip()

    # Supprimer les doublons sur nom_entreprise
    df = df.drop_duplicates(subset=["nom_entreprise"])

    # Vérifier qu'il reste des lignes après nettoyage
    if df.empty:
        raise ValueError("Le fichier CSV ne contient aucune ligne valide après nettoyage.")

    # --- 4. Ajouter site_web vide si colonne absente ---
    if "site_web" not in df.columns:
        df["site_web"] = ""

    # Remplacer les NaN de site_web par une chaîne vide
    df["site_web"] = df["site_web"].fillna("")

    # --- 5. Retourner uniquement les colonnes utiles sous forme de liste de dicts ---
    colonnes_finales = COLONNES_OBLIGATOIRES + COLONNES_OPTIONNELLES
    return df[colonnes_finales].to_dict("records")

# --- Test rapide en standalone ---
if __name__ == "__main__":
    import sys

    fichier = sys.argv[1] if len(sys.argv) > 1 else "prospector/input_example.csv"

    try:
        entreprises = parse_csv(fichier)
        print(f"✅ {len(entreprises)} entreprise(s) chargée(s) :\n")
        for e in entreprises:
            print(f"  - {e['nom_entreprise']} ({e['secteur']}) — {e['site_web'] or 'pas de site'}")
    except ValueError as e:
        print(f"❌ Erreur : {e}")