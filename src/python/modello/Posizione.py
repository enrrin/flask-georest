from geoalchemy2.types import Geometry
from geoalchemy2.shape import to_shape
from src.python.modello.Accesso import accesso
from src.python.persistenza.sql_alchemy.db import db


class Posizione(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazione = db.Column(db.String(80), nullable=False)
    regione = db.Column(db.String(80), nullable=False)
    citta = db.Column(db.String(80), nullable=False)
    locazione = db.Column(db.String(120), nullable=False)

    geometria = db.Column(Geometry(geometry_type='POLYGON'),
                          nullable=False, unique=True)

    geometria_validita = db.Column(Geometry(geometry_type='POLYGON'),
                                   nullable=False, unique=False)

    documenti = db.relationship(
        "Documento", secondary=accesso, back_populates="posizioni", cascade="all,delete", lazy=True)

    def get_geometria(self):
        return self.__converti_geom_to_coords(self.geometria)

    def get_regione_validita(self):
        return self.__converti_geom_to_coords(self.geometria_validita)

    # - la creazione di get e set con decoratori crea problemi all'adattamento delle proprietà di psycopg2

    def __repr__(self):
        return '<Posizione %r>' % self.locazione

    def to_geojson(self, lista_documenti):
        coords = self.__converti_geom_to_coords()
        return {"type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords]
                },
                "properties": {
                    "citta": self.citta,
                    "locazione": self.locazione,
                    "documenti": lista_documenti,
                }
                }

    def __converti_geom_to_coords(self, geometria_da_convertire):
        shape = to_shape(geometria_da_convertire)
        coords = list(shape.exterior.coords)
        return coords
