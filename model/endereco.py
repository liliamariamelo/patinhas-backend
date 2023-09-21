from flask_restful import fields
from helpers.database import db

endereco_fields = {
  'id': fields.Integer,
  'logradouro': fields.String,
  'numero': fields.Integer,
  'bairro': fields.String,
  'complemento': fields.String,
  'referencia': fields.String,
  'cep': fields.String,
  'cidade': fields.String,
  'estado': fields.String,

}

class Endereco(db.Model):
  __tablename__ = "endereco"

  id = db.Column(db.Integer, primary_key=True)
  logradouro = db.Column(db.String, nullable=False)
  numero = db.Column(db.String, nullable=False)
  bairro = db.Column(db.String, nullable=False)
  complemento = db.Column(db.String, nullable=False)
  referencia = db.Column(db.String, nullable=False)
  cep = db.Column(db.String, nullable=False)
  cidade = db.Column(db.String, nullable=False)
  estado = db.Column(db.String, nullable=False)

  ong = db.relationship("Ong", uselist=False, backref="endereco")


  def __init__(self, logradouro, numero, bairro, complemento, referencia, cep, cidade, estado):
    self.logradouro = logradouro
    self.numero = numero
    self.bairro = bairro
    self.referencia = referencia
    self.complemento = complemento
    self.cep = cep 
    self.cidade = cidade
    self.estado = estado


  def __repr__(self):
    return f'<Endereço>'
