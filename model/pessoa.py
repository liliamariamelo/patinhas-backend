from flask_restful import fields
from helpers.database import db

pessoa_fields = {
  'id': fields.Integer,
  'nome': fields.String,
  'cpf': fields.String,
  'nascimento': fields.String,
  'email': fields.String,
  'senha': fields.String,
  'telefone': fields.String,
  'tipo': fields.String,
}

class Pessoa(db.Model):
  __tablename__ = "pessoa"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  cpf = db.Column(db.String, unique=True, nullable=False)
  email = db.Column(db.String, unique=True, nullable=False)
  senha = db.Column(db.String, nullable=False)
  nascimento = db.Column(db.Date, nullable=False)
  telefone = db.Column(db.String, unique=True, nullable=False)
  tipo = db.Column(db.String, nullable=False)


  __mapper_args__ = {
    "polymorphic_identity": "pessoa",
    "polymorphic_on":tipo
  }

  def __init__(self, nome, cpf, email, senha, nascimento, telefone):
    self.nome = nome
    self.cpf = cpf
    self.email = email
    self.senha = senha
    self.telefone = telefone
    self.nascimento = nascimento

  def __repr__(self):
    return f'<Pessoa {self.nome}>'