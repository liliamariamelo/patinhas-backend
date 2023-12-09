from flask_restful import fields
from helpers.database import db
from model.gestor import *

ong_fields = {
  'id': fields.Integer,
  'nome': fields.String,
  'cnpj': fields.String,
  'telefone': fields.String,
  'email': fields.String,
  'senha': fields.String,
  'logradouro': fields.String,
  'numero': fields.Integer,
  'bairro': fields.String,
  'cep': fields.String,
  'cidade': fields.String,
  'id_gestor' : fields.Integer,
}

class ONG(db.Model):
  __tablename__ = "ong"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  cnpj = db.Column(db.String, unique=True, nullable=False)
  telefone = db.Column(db.String, nullable=False)
  email = db.Column(db.String, unique=True, nullable=False)
  logradouro = db.Column(db.String, nullable=False)
  numero = db.Column(db.String, nullable=False)
  bairro = db.Column(db.String, nullable=False)
  cep = db.Column(db.String, nullable=False)
  cidade = db.Column(db.String, nullable=False)
  id_gestor = db.Column(db.Integer, db.ForeignKey("gestor_ong.pessoa_id"), nullable=True)

  gestor = db.relationship("Gestor", uselist=False)

  def __init__(self, nome, cnpj, telefone, email, logradouro, numero, bairro, cep, cidade, id_gestor):
    self.nome = nome
    self.cnpj = cnpj
    self.telefone = telefone
    self.email = email
    self.logradouro = logradouro
    self.numero = numero
    self.bairro = bairro
    self.cep = cep
    self.cidade = cidade
    self.id_gestor = id_gestor

  def __repr__(self):
    return f'<Ong>'