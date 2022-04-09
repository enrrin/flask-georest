from src.python.persistenza.sql_alchemy.db import db
from src.python.modello.Accesso import accesso
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.mutable import MutableDict


class Documento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    descrizione = db.Column(db.String(120), nullable=False)

    href = db.Column(MutableDict.as_mutable(HSTORE))

    posizioni = db.relationship(
        "Posizione", secondary=accesso, back_populates="documenti", cascade="all,delete", lazy=True)

    # - la creazione di get e set con decoratori crea problemi all'adattamento delle proprietà di psycopg2

    def __repr__(self):
        return 'Documento(nome=%s, descr=%s,)' % (self.nome, self.descrizione)

    def to_json(self):
        return {'nome': self.nome, 'descrizione': self.descrizione, 'href': list(self.href.keys())}
