from src.python.modello.Posizione import Posizione, db
from sqlalchemy import func
from geoalchemy2.elements import WKTElement


class DAOPosizione(Posizione):

    def __init__(self):
        super().__init__()

    # - ricerca posizione nella locazione esatta
    def find_by_latlon(self, lat, lon) -> Posizione:
        try:
            pt = WKTElement('SRID=4326;POINT({1} {0})'.format(
                lat, lon), extended=True)
            risultati = db.session.query(Posizione).filter(
                func.ST_Contains(Posizione.geometria, pt))
            posizioni_trovate = risultati.all()
            if posizioni_trovate is not None and posizioni_trovate:
                return posizioni_trovate
            elif posizioni_trovate is None or not posizioni_trovate:
                return None
        except Exception as ex:
            raise Exception(f"Errore dal DAOPosizione: {ex}")

    # - ricerca posizione nella locazione di buffer
    def find_by_latlon_buffer(self, lat, lon) -> Posizione:
        try:
            pt = WKTElement('SRID=4326;POINT({1} {0})'.format(
                lat, lon), extended=True)
            risultati = db.session.query(Posizione).filter(
                func.ST_Contains(Posizione.geometria_validita, pt))
            posizioni_trovate = risultati.all()
            if posizioni_trovate is not None and posizioni_trovate:
                return posizioni_trovate
            elif posizioni_trovate is None or not posizioni_trovate:
                return None
        except Exception as ex:
            raise Exception(f"Errore dal DAOPosizione: {ex}")

    # - ricerca in base alla citta
    def find_by_citta(self, citta) -> Posizione:
        posizione = Posizione()
        try:
            risultato = posizione.query.filter_by(
                citta=citta)
            posizioni_trovate = risultato.all()
            if posizioni_trovate is not None and posizioni_trovate:
                return posizioni_trovate
            elif posizioni_trovate is None or not posizioni_trovate:
                return None
        except Exception as ex:
            raise Exception(f"Errore dal DAOPosizione: {ex}")
