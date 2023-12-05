from flask_restful import fields
from helpers.database import db
from model.gestor import * 

ong_fields = {
  'id': fields.Integer,
  'nome': fields.String,
  'cnpj': fields.String,
  'email': fields.String,
  'senha': fields.String,
  'telefone': fields.String,
  'logradouro': fields.String,
  'numero': fields.Integer,
  'bairro': fields.String,
  'complemento': fields.String,
  'referencia': fields.String,
  'cep': fields.String,
  'cidade': fields.String,
  'estado': fields.String,
  'id_gestor' : fields.Integer,
}

class ONG(db.Model):
  __tablename__ = "ong"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  cnpj = db.Column(db.String, unique=True, nullable=False)
  email = db.Column(db.String, unique=True, nullable=False)
  senha = db.Column(db.String, nullable=False)
  telefone = db.Column(db.String, nullable=False)
  logradouro = db.Column(db.String, nullable=False)
  numero = db.Column(db.String, nullable=False)
  bairro = db.Column(db.String, nullable=False)
  complemento = db.Column(db.String, nullable=False)
  referencia = db.Column(db.String, nullable=False)
  cep = db.Column(db.String, nullable=False)
  cidade = db.Column(db.String, nullable=False)
  estado = db.Column(db.String, nullable=False) 
  id_gestor = db.Column(db.Integer, db.ForeignKey("gestor_ong.id"), nullable=True)

  def __init__(self, nome, cnpj, email, senha, telefone, logradouro, numero, bairro, complemento, referencia, cep, cidade, estado, id_gestor):
    self.nome = nome
    self.cnpj = cnpj
    self.email = email
    self.senha = senha
    self.telefone = telefone
    self.logradouro = logradouro
    self.numero = numero
    self.bairro = bairro
    self.referencia = referencia
    self.complemento = complemento
    self.cep = cep 
    self.cidade = cidade
    self.estado = estado
    self.id_gestor = id_gestor

  def __repr__(self):
    return f'<Ong>'