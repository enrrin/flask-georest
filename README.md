# flask-georest
Sistema di gestione di documenti digitali basato sull’uso di informazioni georeferenziate
![git_app1](https://user-images.githubusercontent.com/76885412/162795897-24388f4e-24ab-4925-8ce4-ff118cd9732b.png)

## Setup
### Clonare il repo e l'ambiente virtuale
    git clone https://github.com/enrrin/flask-georest
    cd flask-georest/
    chmod +x setup.sh
    . setup.sh
### Installare le dipendenze
    pip install -r requirements.txt
### Impostare la cartella in cui salvare i log in
    vi config/logging.conf
### Inserire token mapbox
    vi src/public/js/mappa.js 

##  Setup del database
### Aggiornare le credenziali in
    cp env_sample .env
### Creazione database
    python
    from src.app import app
    from src.python.modello.Documento import db
    from src.python.modello.Accesso import db
    from src.python.modello.Posizione import db
    with app.app_context():
        db.drop_all()
        db.create_all() 
## Run
    flask run --host=0000 --port=8080
