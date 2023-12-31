from flask_restful import fields
from helpers.database import db
from datetime import datetime

relatoriodespesas_fields = {
  'categoria': fields.String,
  'valor': fields.Float,
  'data': fields.String,
  'observacoes': fields.String,
  'mes_Correspondente' : fields.Integer,

}

class RelatorioDespesas(db.Model):
  __tablename__ = "relatoriodespesas"

  id = db.Column(db.Integer, primary_key=True)
  categoria = db.Column(db.String, nullable=False)
  valor = db.Column(db.Float, nullable=False)
  data = db.Column(db.String, nullable=False)
  observacoes = db.Column(db.String)
  mes_Correspondente = db.Column(db.Integer, nullable=False)

  def __init__(self, categoria, valor, data, observacoes, mes_Correspondente):
    self.categoria = categoria
    self.valor = valor
    self.data = data
    self.observacoes = observacoes
    self.mes_Correspondente = mes_Correspondente


  def __repr__(self):
    return f'<RelatorioDespesas>'

