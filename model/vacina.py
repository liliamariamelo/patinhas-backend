from flask_restful import fields
from helpers.database import db

vacina_fields = {
  'id': fields.Integer,
  'nome': fields.String,
}

class Vacina(db.Model):
  __tablename__ = "vacina"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  animal_id = db.Column(db.Integer, db.ForeignKey("animal.id"), nullable=True)
 # animal = db.relationship("Animal", backref="vacina")



  def __init__(self, nome):
    self.nome = nome
  
  
    
  def __repr__(self):
    return f'<Vacina>'