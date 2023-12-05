from flask_restful import fields
from helpers.database import db

gestor_fields = {
  'id': fields.Integer,
  'nome': fields.String,
  'cpf' : fields.String,
  'nascimento': fields.String,
  'telefone': fields.String,
  'email': fields.String,
  'senha': fields.String,
}

class Gestor(db.Model):
    __tablename__ = "gestor_ong"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    cpf = db.Column(db.String, unique=True, nullable=False)
    nascimento = db.Column(db.Date, nullable=False)
    telefone = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String, nullable=False)

    def __init__(self, nome, cpf, nascimento, telefone,  email, senha):
      self.nome = nome
      self.cpf = cpf
      self.nascimento = nascimento
      self.telefone = telefone
      self.email = email
      self.senha = senha


    def __repr__(self):
        return f'<Gestor>'