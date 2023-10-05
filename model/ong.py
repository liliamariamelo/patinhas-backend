from flask_restful import fields
from helpers.database import db
from model.endereco import endereco_fields

ong_fields = {
  'id': fields.Integer,
  'nome': fields.String,
  'cnpj': fields.String,
  'email': fields.String,
  'senha': fields.String,
  'telefone': fields.String,
  'endereco': fields.Nested(endereco_fields),
}

class Ong(db.Model):
  __tablename__ = "ong"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  cnpj = db.Column(db.String, unique=True, nullable=False)
  email = db.Column(db.String, unique=True, nullable=False)
  senha = db.Column(db.String, nullable=False)
  telefone = db.Column(db.String, nullable=False)
  id_endereco = db.Column(db.Integer, db.ForeignKey('endereco.id'))

  def __init__(self, nome, cnpj, email, senha, telefone, id_endereco):
    super().__init__()
    self.nome = nome
    self.cnpj = cnpj
    self.email = email
    self.senha = senha
    self.telefone = telefone
    self.id_endereco = id_endereco

  def __repr__(self):
    return f'<Ong>'