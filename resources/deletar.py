from resources.parceiro import Parceiro
from resources.gestor import Gestor
from resources.ong import Ong
from resources.animal import Animal
from model.pessoa import *
from model.parceiro import *
from model.gestor import *
from model.ong import *
from model.animal import *
from helpers.database import db
from helpers.base_logger import logger
from flask_restful import Resource, marshal
from model.message import *

class DeletarPessoa(Resource):
    def delete(self, id):
        pessoa = Pessoa.query.get(id)

        if pessoa is None:
            logger.error(f"Pessoa {id} não encontrada")
            message = Message(f"Pessoa {id} não encontrada", 1)
            return marshal(message, message_fields)

        db.session.delete(pessoa)
        db.session.commit()

        message = Message("Pessoa deletada com sucesso!", 3)
        return marshal(message, message_fields), 200

class DeletarParceiro(Resource):
    def delete(self, id):
        parceiro = Parceiro.query.get(id)

        if parceiro is None:
            logger.error(f"Parceiro {id} não encontrada")
            message = Message(f"Parceiro {id} não encontrada", 1)
            return marshal(message, message_fields)

        db.session.delete(parceiro)
        db.session.commit()

        message = Message("Parceiro deletado com sucesso!", 3)
        return marshal(message, message_fields), 200

class DeletarGestor(Resource):
    def delete(self, id):
        gestor = Gestor.query.get(id)

        if gestor is None:
            logger.error(f"Gestor {id} não encontrada")
            message = Message(f"Gestor {id} não encontrada", 1)
            return marshal(message, message_fields)

        db.session.delete(gestor)
        db.session.commit()

        message = Message("Gestor deletada com sucesso!", 3)
        return marshal(message, message_fields), 200
    
class DeletarOng(Resource):
    def delete(self, id):
        ong = Ong.query.get(id)

        if ong is None:
            logger.error(f"Ong {id} não encontrada")
            message = Message(f"Ong {id} não encontrada", 1)
            return marshal(message, message_fields)

        db.session.delete(ong)
        db.session.commit()

        message = Message("Ong deletado com sucesso!", 3)
        return marshal(message, message_fields), 200

class DeletarAnimal(Resource):
    def delete(self, id):
        animais = Animal.query.get(id)

        if animais is None:
            logger.error(f"Animal {id} não encontrada")
            message = Message(f"Animal {id} não encontrada", 1)
            return marshal(message, message_fields)

        db.session.delete(animais)
        db.session.commit()

        message = Message("Animal deletado com sucesso!", 3)
        return marshal(message, message_fields), 200


