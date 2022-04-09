from src.python.persistenza.sql_alchemy.db import db


# tabella ausiliaria tra Documento e Posizione
accesso = db.Table(
    "accesso",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("documento", db.Integer, db.ForeignKey("documento.id")),
    db.Column("posizione", db.Integer, db.ForeignKey("posizione.id")),
)
