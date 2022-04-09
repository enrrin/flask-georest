from src.python.modello.Documento import Documento, db
import sqlalchemy.orm.exc as sqla


class DAODocumento(Documento):

    def __init__(self):
        super().__init__()

    # ricerca in base all'id della posizione
    def find_by_posizioneid(self, id) -> Documento:
        documento = Documento()
        try:
            documenti_trovati = documento.query.filter(
                Documento.posizioni.any(id=id))
            if documenti_trovati != None and documenti_trovati:
                return documenti_trovati.all()
            elif documenti_trovati == None or not documenti_trovati:
                return None
        except Exception as ex:
            raise Exception(f"Errore dal DAODocumento: {ex}")

    # ricerca in base all'id del tipo hstore
    def find_by_hrefid(self, href_id):
        try:
            documento = Documento.query.filter(
                Documento.href.has_key(href_id)).one()
            if documento != None and documento:
                return documento
            elif documento == None or not documento:
                return None
        except sqla.NoResultFound:
            raise FileNotFoundError("Nessun file trovato con questo codice")
        except Exception as ex:
            raise Exception(f"Errore dal DAODocumento: {ex}")

    # ricerca tutti i documenti
    def get_all(self):
        try:
            documenti_trovati = Documento.query.all()
            if documenti_trovati != None and documenti_trovati:
                return documenti_trovati
            elif documenti_trovati == None or not documenti_trovati:
                return None
        except Exception as ex:
            raise Exception(f"Errore dal DAODocumento: {ex}")
