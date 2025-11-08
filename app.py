from scan import scan
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route("/result")
def scan_result():
    return "Scan en cours..."

@app.route("/")
def hello_world():
    return '''
    <h1>Port Scanner</h1>
    <form action="/scan" method="POST">
        <label for="ip">Adresse IP :</label>
        <input type="text" id="ip" name="ip" placeholder="Ex: 192.168.1.1">
        <br><br>

        <label for="port">Port :</label>
        <input type="text" id="port" name="port" placeholder="Ex: 80">
        <br><br>

        <button type="submit">Scanner</button>
    </form>
    '''

@app.route("/scan", methods=["POST"])
def scan_form():
    #Récupère les données du formulaire
    ip = request.form.get("ip")
    port = request.form.get("port")

    #Convertir le port en entier sinon ça marche pas zbi
    port = int(port)

    scan(ip, port)

    # Afficher les données dans le terminal
    print("------ Données du formulaire ------")
    print(f"IP reçue: {ip}")
    print(f"Port reçu: {port}")
    print("-----------------------------------")

      # Rediriger vers la page d'accueil
    return redirect("/result")