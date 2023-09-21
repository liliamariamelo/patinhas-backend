from flask_restful import Resource, reqparse, marshal
from model.parceiro import *
from model.message import *
from helpers.base_logger import logger
from helpers.database import db


parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema no nome', required=True)
parser.add_argument('cpf', type=str, help='Problema no cpf', required=True)
parser.add_argument('email', type=str, help='Problema no email', required=True)
parser.add_argument('senha', type=str, help='Problema no senha', required=True)
parser.add_argument('nascimento', type=str, help='Problema no nascimento', required=True)
parser.add_argument('telefone', type=str, help='Problema no telefone', required=True)


class Parceiros(Resource):
    def get(self):
        logger.info("Parceiros listadas com sucesso!")
        parceiros = Parceiro.query.all()
        return marshal(parceiros, parceiro_fields), 200

    def post(self):
        args = parser.parse_args()
        try:
            nome = args["nome"]
            email = args["email"]
            senha = args["senha"]
            cpf = args["cpf"]
            nascimento = args["nascimento"]
            telefone = args["telefone"]


            parceiro = Parceiro(nome, cpf, email, senha, nascimento, telefone )

            db.session.add(parceiro)
            db.session.commit()

            logger.info("Parceiro cadastrada com sucesso!")

            return marshal(parceiro, parceiro_fields), 201
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao cadastrar parceiro", 2)
            return marshal(message, message_fields), 404

class ParceiroById(Resource):
    def get(self, id):
        parceiro = Parceiro.query.get(id)

        if parceiro is None:
            logger.error(f"Parceiro {id} não encontrada")

            message = Message(f"Parceiro {id} não encontrada", 1)
            return marshal(message), 404

        logger.info(f"Parceiro {id} encontrada com sucesso!")
        return marshal(parceiro, parceiro_fields)


    def put(self, id):
        args = parser.parse_args()

        try:
            parceiro = Parceiro.query.get(id)

            if parceiro is None:
                logger.error(f"Parceiro {id} não encontrada")
                message = Message(f"Parceiro {id} não encontrada", 1)
                return marshal(message, message_fields)

            parceiro.nome = args["nome"]
            parceiro.cpf = args["cpf"]
            parceiro.email = args["email"]
            parceiro.senha = args["senha"]
            parceiro.nascimento = args["nascimento"]
            parceiro.telefone = args["telefone"]
            
            db.session.add(parceiro)
            db.session.commit()

            logger.info("Parceiro cadastrada com sucesso!")
            return marshal(parceiro, parceiro_fields), 200
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao atualizar parceiro", 2)
            return marshal(message, message_fields), 404

   
    def delete(self, id):
        parceiro = Parceiro.query.get(id)

        if parceiro is None:
            logger.error(f"Parceiro {id} não encontrada")
            message = Message(f"Parceiro {id} não encontrada", 1)
            return marshal(message, message_fields)

        db.session.delete(parceiro)
        db.session.commit()

        message = Message("Parceiro deletada com sucesso!", 3)
        return marshal(message, message_fields), 200

class ParceiroByNome(Resource):
    def get(self, nome):
        parceiro = Parceiro.query.filter_by(nome=nome).all()

        if parceiro is None:
            logger.error(f"Parceiro {id} não encontrado")

            message = Message(f"Parceiro {id} não encontrado", 1)
            return marshal(message), 404

        logger.info(f"Parceiro {id} encontrado com sucesso!")
        return marshal(parceiro, parceiro_fields), 200

class ParceiroMe(Resource):
    def get(self):
        parceiro = Parceiro.query

        if parceiro is None:
            logger.error(f"Parceiro {id} não encontrada")

            message = Message(f"Parceiro {id} não encontrada", 1)
            return marshal(message), 404

        logger.info(f"Parceiro {id} encontrada com sucesso!")
        return marshal(parceiro, parceiro_fields), 200