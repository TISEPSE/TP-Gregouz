from scan import scan
from scanner import valid_ipv4_address, valid_port
from flask import Flask, request, redirect

app = Flask(__name__)

# Variable globale pour stocker le résultat
scan_result_global = ""

@app.route("/result")
def scan_result():
    global scan_result_global

    return f'''
    <h1>Résultat du Scan</h1>
    <p>IP: {scan_result_global["ip"]}</p>
    <p>Port: {scan_result_global["port"]}</p>
    <p>{scan_result_global["result"]["data"]} : {scan_result_global["result"]["type"]}</p>
    <br>
    <a href="/">← Retour</a>
    '''

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
    global scan_result_global

    #Récupère les données du formulaire
    ip = request.form.get("ip")
    port = request.form.get("port")

    #Convertir le port en entier sinon ça marche pas zbi
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
        scan_result_global = {
            "ip": ip,
            "port": port,
            "result": result
        }

        # Rediriger vers /result
        return redirect("/result")

    except Exception as e:
        return f'''
        <h1>Erreur de validation</h1>
        <p>{str(e)}</p>
        <br>
        <a href="/">← Retour</a>
        '''