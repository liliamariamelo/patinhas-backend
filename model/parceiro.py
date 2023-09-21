from flask_restful import fields
from helpers.database import db
from model.pessoa import Pessoa

parceiro_fields = {
  'id': fields.Integer,
  'nome': fields.String,
  'cpf': fields.String,
  'nascimento': fields.String,
  'email': fields.String,
  'senha': fields.String,
  'telefone': fields.String,
}

class Parceiro(Pessoa):
    __tablename__ = "parceiro_ong"

    id_pessoa = db.Column(db.Integer ,db.ForeignKey("pessoa.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "parceiro_ong"}

    def __init__(self, nome, cpf, email, senha, nascimento, telefone):
        super().__init__(nome, cpf, email, senha,  nascimento, telefone)

    def __repr__(self):
        return f'<Parceiro {self.nome}>'