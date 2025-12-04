from src.templates.core.scan import scan
from src.templates.core.scanner import valid_ipv4_address, valid_port
from flask import Flask, render_template, request, redirect

app = Flask(__name__,
            template_folder='src/templates',
            static_folder='src/static')

# Variable globale pour stocker le résultat
scan_result_global = ""


@app.route("/result")
def scan_result():
    global scan_result_global

    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Résultat du Scan</title>
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
        <div class="container">
            <h1>Résultat du Scan</h1>
            <div class="result-item">
                <span class="result-label">IP:</span>
                <span class="result-value">{scan_result_global["ip"]}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Port:</span>
                <span class="result-value">{scan_result_global["port"]}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Statut:</span>
                <span class="result-value">{scan_result_global["result"]["data"]} : {scan_result_global["result"]["type"]}</span>
            </div>
            <a href="/" class="back-link">← Retour</a>
        </div>
    </body>
    </html>
    """


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan_form():
    global scan_result_global

    # Récupère les données du formulaire
    ip = request.form.get("ip")
    port = request.form.get("port")

    # Convertir le port en entier sinon ça marche pas zbi
    port = int(port)

    # Vérif si port et ip sont valides
    try:
        valid_ipv4_address(ip)
        valid_port(port)

        # Si pas d'erreur, on continue avec le scan
        result = scan(ip, port)

        # Afficher les données dans le terminal
        print("------ Données du formulaire ------")
        print(f"IP: {ip}")
        print(f"Port: {port}")
        print("-----------------------------------")

        # Stocker le résultat dans la variable globale
        scan_result_global = {"ip": ip, "port": port, "result": result}

        # Rediriger vers /result
        return redirect("/result")

    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Erreur</title>
            <link rel="stylesheet" href="/static/css/style.css">
        </head>
        <body>
            <div class="container">
                <h1>Erreur de validation</h1>
                <div class="error-message">
                    <p>{str(e)}</p>
                </div>
                <a href="/" class="back-link">← Retour</a>
            </div>
        </body>
        </html>
        """
