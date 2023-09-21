from flask_restful import fields
from helpers.database import db
from model.pessoa import Pessoa
from model.ong import *

gestor_fields = {
  'id': fields.Integer,
  'nome': fields.String,
  'nascimento': fields.String,
  'email': fields.String,
  'senha': fields.String,
  'telefone': fields.String,
  'id_ong': fields.Integer,
}

class Gestor(Pessoa):
    __tablename__ = "gestor_ong"

    id_pessoa = db.Column(db.Integer ,db.ForeignKey("pessoa.id"), primary_key=True)
    id_ong = db.Column(db.Integer, db.ForeignKey("ong.id"), nullable=True)

    __mapper_args__ = {"polymorphic_identity": "gestor_ong"}

    def __init__(self, nome, cpf, email, senha,  nascimento, telefone, id_ong):
        super().__init__(nome, cpf, email, senha, nascimento, telefone)
        self.id_ong = id_ong

    def __repr__(self):
        return f'<Gestor {self.nome}>'