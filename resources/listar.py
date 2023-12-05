from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.base_logger import logger
from resources.parceiro import Parceiro
from resources.gestor import Gestor
from resources.ong import ONG
from resources.animal import Animal
from model.parceiro import *
from model.gestor import *
from model.ong import *
from model.animal import *

class ListarTodos(Resource):
    def get(self):
        logger.info("Usuários listados com sucesso!")
        gestores = Gestor.query.all()
        parceiros = Parceiro.query.all()
        ongs = ONG.query.all()
        animais = Animal.query.all()

        
        gestores_serializados = marshal(gestores, gestor_fields)
        parceiros_serializados = marshal(parceiros, parceiro_fields)
        ongs_serializados = marshal(ongs, ong_fields),
        animais_serializados = marshal(animais, animal_fields)


    
        todos_os_dados = {
            'gestores': gestores_serializados,
            'parceiros': parceiros_serializados,
            'ongs': ongs_serializados,
            'animais' : animais_serializados
        }

        return todos_os_dados, 200
  