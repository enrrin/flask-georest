# flask-georest

Sistema di gestione di documenti digitali basato sull’uso di informazioni georeferenziate
![git_app1](https://user-images.githubusercontent.com/76885412/162795897-24388f4e-24ab-4925-8ce4-ff118cd9732b.png)

---

## Setup

```bash
git clone https://github.com/enrrin/flask-georest
cd flask-georest/
```

### Installare le dipendenze:

```bash
sudo apt install python3 pip python3.10-venv postgresql postgis
```

### Installare i package necessari per l'ambiente virtuale:

```bash
python3 -m venv venv
pip3 install -r requirements.txt
```

### Download database [IP2LocationLITE](https://lite.ip2location.com/) (DB5LITEBIN e PX2LITEBIN):

```bash
wget -O database.zip https://www.ip2location.com/download?token=<token>\&file=DB5LITEBIN
unzip -o database.zip
```

### Creazione nuovo utente psql:

```bash
sudo -u postgres psql
```

```sql
create user pguser;
create database pguser;
alter user pguser with encrypted password '123456';
alter role pguser with createdb;
\du
```

### Creazione database con le estensioni necessarie:

```sql
create database progetto;
\c progetto
create extension postgis;
create extension hstore;
\q

```
> Per poter dare accesso al db è necessario modificare `/etc/postgresql/14/main/pg_hba.conf` con autenticazione *md5* anziché *peer*

```bash
sudo service postgresql reload
```

### Inserire le credenziali del database:

```bash
cp env_sample .env
vi .env
```

> Prima di creare lo schema, assicurarsi che il PYTHONPATH sia corretto: ``` export PYTHONPATH=$PYTHONPATH:"$HOME/src" ```

### Creare lo schema:

```python
python
from src.app import app
from src.python.modello.Documento import db
from src.python.modello.Accesso import db
from src.python.modello.Posizione import db
with app.app_context():
    db.drop_all()
    db.create_all() 
```

### Inserire dati nel database:

> Assicurarsi che il percorso per i PDF sia corretto

```sql
psql -U pguser -d proj -f src/risorse/insert_sample.sql
```
Inserire il token mapbox in `src/public/js/mappa.js` e il file in cui salvare i log in `config/logging.conf`

### Eseguire l'applicazione:
```bash
export FLASK_APP="$HOME/src/app.py"
export FLASK_ENV="development"
source venv/bin/activate
flask run --host=0000 --port=8080
```