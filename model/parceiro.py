from flask_restful import fields
from helpers.database import db
from model.pessoa import Pessoa

parceiro_fields = {
  'id': fields.Integer,
  'nome': fields.String,
  'cpf': fields.String,
  'nascimento': fields.String,
  'telefone': fields.String,
  'email': fields.String,
  'senha': fields.String
}

class Parceiro(Pessoa):
    __tablename__ = "parceiro_ong"

    pessoa_id = db.Column(db.Integer, db.ForeignKey("pessoa.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "parceiro"}

    def __init__(self, nome, cpf, nascimento, telefone,  email, senha):
      super().__init__(nome, cpf, nascimento, telefone,  email, senha)


    def __repr__(self):
        return f'<Parceiro da Ong>'