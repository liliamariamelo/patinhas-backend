from flask_restful import fields
from helpers.database import db
#from model.vacina import * 

animal_fields = {
  'id': fields.Integer,
  'nome': fields.String,
  'especie': fields.String,
  'raca': fields.String,
  'idade': fields.Integer,
  'origem' : fields.String, #resgatado ou doado
  'descricao_origem' : fields.String,
  'vacina_em_dia': fields.Boolean
}

class Animal(db.Model):
  __tablename__ = "animal"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  especie = db.Column(db.String, nullable=False)
  raca = db.Column(db.String, nullable=False)
  idade = db.Column(db.Integer, nullable=False)
  origem = db.Column(db.String, nullable=False)
  descricao_origem = db.Column(db.String, nullable=False)
  vacina_em_dia = db.Column(db.Boolean, nullable=False)

  def __init__(self, nome, especie, raca, idade, origem, descricao_origem, vacina_em_dia):
    self.nome = nome
    self.especie = especie
    self.raca = raca
    self.idade = idade
    self.origem = origem
    self.descricao_origem = descricao_origem
    self.vacina_em_dia = vacina_em_dia
    
  def __repr__(self):
    return f'<Animal {self.nome}>'