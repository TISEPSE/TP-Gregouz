from src import create_app

app = create_app()
app.secret_key = "une-cle-secrete-au-hasard"

if __name__ == '__main__':
    app.run(port=5001)