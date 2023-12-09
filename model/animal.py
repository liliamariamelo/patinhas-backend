from flask_restful import fields
from helpers.database import db
from model.vacina import vacina_fields


animal_fields = {
  'id': fields.Integer,
  'nome': fields.String,
  'especie': fields.String,
  'raca': fields.String,
  'idade': fields.Integer,
  'vacina_em_dia': fields.Boolean,
}



class Animal(db.Model):
  __tablename__ = "animal"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  especie = db.Column(db.String, nullable=False)
  raca = db.Column(db.String, nullable=False)
  idade = db.Column(db.Integer, nullable=False)

  vacina_em_dia = db.Column(db.Boolean, nullable=False)

  def __init__(self, nome, especie, raca, idade, vacina_em_dia):
    self.nome = nome
    self.especie = especie
    self.raca = raca
    self.idade = idade
    self.vacina_em_dia = vacina_em_dia


  def __repr__(self):
    return f'<Animal {self.nome}>'

