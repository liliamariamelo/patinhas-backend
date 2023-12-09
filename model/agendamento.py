from flask_restful import fields
from helpers.database import db
from model.animal import Animal
from model.parceiro import Parceiro
from sqlalchemy import DateTime


class DateFormat(fields.Raw):
  def format(self, value):
      return value.strftime('%Y-%m-%d')

class TimeFormat(fields.Raw):
  def format(self, value):
      return value.strftime('%H:%M')

agendamento_fields = {
    'data_visita': DateFormat,
    'hora_visita': TimeFormat,
    'id_animal': fields.Integer,
    'id_parceiro': fields.Integer,
}

class Agendamento(db.Model):

    __tablename__ = "agendamento"

    id = db.Column(db.Integer, primary_key=True)
    data_visita = db.Column(db.Date, nullable=False)
    hora_visita = db.Column(db.DateTime, nullable=False)
    id_animal = db.Column(db.Integer, db.ForeignKey("animal.id"), nullable=True)
    id_parceiro = db.Column(db.Integer, db.ForeignKey("parceiro_ong.pessoa_id"), nullable=True)

    parceiro = db.relationship("Parceiro", uselist=False)
    animal = db.relationship("Animal", uselist=False)

    def __init__(self, data_visita, hora_visita, animal, parceiro):
        self.data_visita = data_visita
        self.hora_visita = hora_visita
        self.animal = animal
        self.parceiro = parceiro

    def hora_formatada(self):
        return self.hora_visita.strftime('%H:%M')

    def __repr__(self):
        return f'<Agendamento>'
