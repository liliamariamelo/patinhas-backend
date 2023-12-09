from flask_restful import fields
from helpers.database import db
from model.pessoa import Pessoa

class DateFormat(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d')

gestor_fields = {
  'id': fields.Integer,
  'nome': fields.String,
  'cpf' : fields.String,
  'nascimento': DateFormat,
  'telefone': fields.String,
  'email': fields.String,
  'senha': fields.String,
}

class Gestor(Pessoa):
    __tablename__ = "gestor_ong"

    pessoa_id = db.Column(db.Integer, db.ForeignKey("pessoa.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "gestor"}

    def __init__(self, nome, cpf, nascimento, telefone,  email, senha):
      super().__init__(nome, cpf, nascimento, telefone,  email, senha)

    def __repr__(self):
        return f'<Gestor>'