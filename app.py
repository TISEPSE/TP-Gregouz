from src import create_app

app = create_app()
app.secret_key = "une-cle-secrete-au-hasard"