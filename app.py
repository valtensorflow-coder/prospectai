from flask import Flask, render_template, request, send_file
import os
from system.generator import EmailClient
from system.parser import parse_csv
from system.exporter import exporter_csv, exporter_pdf
from flask import jsonify

FRONTEND_DIR = os.path.join("system", "templates")

app = Flask(__name__, template_folder=FRONTEND_DIR)

resultats = []

@app.route("/")
def serve_frontend():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_email():
    global resultats
    fichier = request.files["csv"]
    tonalite = request.form["tonalite"]
    fichier.save("temp.csv")
    entreprises = parse_csv("temp.csv")
    client = EmailClient()
    resultat = client.generer_tous(entreprises, tonalite)
    resultats = resultat
    return jsonify(resultat)

@app.route("/download/csv", methods=["GET"])
def export_csv():
    global resultats
    chemin=exporter_csv(resultats)
    return send_file(chemin, as_attachment=True)

@app.route("/download/pdf", methods=["GET"])
def export_pdf():
    global resultats
    chemin=exporter_pdf(resultats)
    return send_file(chemin, as_attachment=True)

if __name__ == "__main__":
    PORT=int(os.getenv("PORT", 5000))
    print(f"🤓 Intégration IA démarré sur http://localhost:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)