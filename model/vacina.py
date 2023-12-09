from flask_restful import fields
from helpers.database import db

vacina_fields = {
  'id': fields.Integer,
  'nome': fields.String,
  'animal_id':fields.Integer
}



class Vacina(db.Model):
  __tablename__ = "vacina"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  animal_id = db.Column(db.Integer, db.ForeignKey("animal.id"), nullable=True)

  animal = db.relationship("Animal", uselist=False )

  def __init__(self, nome, animal_id):
    self.nome = nome
    self.animal_id = animal_id

  def __repr__(self):
    return f'<Vacina>'
