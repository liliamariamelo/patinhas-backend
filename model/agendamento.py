from flask_restful import fields
from helpers.database import db
from model.animal import Animal
from model.parceiro import Parceiro

agendamento_fields = {
    'data_visita': fields.String,
    'hora_visita': fields.String,
    'id_animal': fields.Integer,
    'id_parceiro': fields.Integer,
}

class Agendamento(db.Model):
    __tablename__ = "agendamento"

    id = db.Column(db.Integer, primary_key=True)
    data_visita = db.Column(db.String, nullable=False)
    hora_visita = db.Column(db.String, nullable=False)
    id_animal = db.Column(db.Integer, db.ForeignKey("animal.id"), nullable=True)
    id_parceiro = db.Column(db.Integer, db.ForeignKey("parceiro_ong.id"), nullable=True)


    def __init__(self, data_visita, hora_visita, id_animal, id_parceiro):
        self.data_visita = data_visita
        self.hora_visita = hora_visita
        self.id_animal = id_animal
        self.id_parceiro = id_parceiro

    def __repr__(self):
        return f'<Agendamento>'
