from flask import Flask, send_from_directory
from flask_restful import Api
from src.python.modello.Accesso import db
from src.python.modello.Documento import db
from src.python.modello.Posizione import db
from config.flask_config import get_config
from src.python.controllo.ControlloPosizione import ControlloPosizione
from src.python.controllo.ControlloDocumento import ControlloDocumento

from werkzeug.middleware.proxy_fix import ProxyFix

from datetime import timedelta


app = Flask(__name__, static_folder='public', static_url_path='')
app.config.from_object(get_config('env'))
db.init_app(app)

app.permanent_session_lifetime = timedelta(days=1)


@app.route('/')
def index():
    return send_from_directory('public', 'index.html')


api = Api(app)
# # POST date lat/lon ritorna geojeson corrispondente, se presente
api.add_resource(ControlloDocumento, '/api/documenti',
                 '/api/documenti/<href_id>')
# # GET consenso alla posizione negato
api.add_resource(ControlloPosizione, '/api/posizione')

# ProxyFix per reverse proxy server
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

if __name__ == '__main__':
    app.run(debug=True)

# - https in localhost
# flask run --cert cert/cert.pem --key cert/key.pem --host="0.0.0.0"
