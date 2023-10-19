from flask_restful import fields
from helpers.database import db
#from model.animal import * 

vacina_fields = {
  'id': fields.Integer,
  'nome': fields.String,
 # 'animal' : fields.Nested(animal_fields),
}

class Vacina(db.Model):
  __tablename__ = "vacina"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  #id_animal= db.Column(db.Integer, db.ForeignKey("animal.id"), nullable=True)
  #animal = db.relationship("Animal", backref="vacina")

  def __init__(self, nome, animal):
    self.nome = nome
    self.animal = animal
  
    
  def __repr__(self):
    return f'<Vacina>'