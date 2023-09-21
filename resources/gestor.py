from flask_restful import Resource, reqparse, marshal
from model.gestor import *
from model.ong import *
from model.message import *
from helpers.database import db
from helpers.base_logger import logger

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema no nome', required=True)
parser.add_argument('cpf', type=str, help='Problema no cpf', required=True)
parser.add_argument('email', type=str, help='Problema no email', required=True)
parser.add_argument('senha', type=str, help='Problema no senha', required=True)
parser.add_argument('nascimento', type=str, help='Problema no nascimento', required=True)
parser.add_argument('telefone', type=str, help='Problema no telefone', required=True)
parser.add_argument('id_ong', type=int, help='Problema na ONG', required=False)


class Gestores(Resource):
    def get(self):
        logger.info("Gestores listados com sucesso!")
        gestores = Gestor.query.all()
        return marshal(gestores, gestor_fields), 200

    def post(self):
        args = parser.parse_args()
        try:
            nome = args["nome"]
            cpf = args["cpf"]
            email = args["email"]
            senha = args["senha"]
            nascimento = args["nascimento"]
            telefone = args["telefone"]
            id_ong = args["id_ong"]

            gestor = Gestor(nome, cpf, email, senha, nascimento, telefone, id_ong )

            db.session.add(gestor)
            db.session.commit()

            logger.info("Gestor cadastrada com sucesso!")

            return marshal(gestor, gestor_fields), 201
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao cadastrar gestor", 2)
            return marshal(message, message_fields), 404

class GestorById(Resource):
    def get(self, id):
        gestor = Gestor.query.get(id)

        if gestor is None:
            logger.error(f"Gestor {id} não encontrada")

            message = Message(f"Gestor {id} não encontrada", 1)
            return marshal(message), 404

        logger.info(f"Gestor {id} encontrada com sucesso!")
        return marshal(gestor, gestor_fields)


    def put(self, id):
        args = parser.parse_args()

        try:
            gestor = Gestor.query.get(id)

            if gestor is None:
                logger.error(f"Gestor {id} não encontrada")
                message = Message(f"Gestor {id} não encontrada", 1)
                return marshal(message, message_fields)

            gestor.nome = args["nome"]
            gestor.cpf = args["cpf"]
            gestor.email = args["email"]
            gestor.senha = args["senha"]
            gestor.nascimento = args["nascimento"]
            gestor.telefone = args["telefone"]
            gestor.id_ong = args["id_ong"]
            
            db.session.add(gestor)
            db.session.commit()

            logger.info("Gestor cadastrada com sucesso!")
            return marshal(gestor, gestor_fields), 200
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao atualizar gestor", 2)
            return marshal(message, message_fields), 404

   
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

class GestorByNome(Resource):
    def get(self, nome):
        gestor = Gestor.query.filter_by(nome=nome).all()

        if gestor is None:
            logger.error(f"Gestor {id} não encontrado")

            message = Message(f"Gestor {id} não encontrado", 1)
            return marshal(message), 404

        logger.info(f"Gestor {id} encontrado com sucesso!")
        return marshal(gestor, gestor_fields), 200

class GestorMe(Resource):
    def get(self):
        gestor = Gestor.query

        if gestor is None:
            logger.error(f"Gestor {id} não encontrada")

            message = Message(f"Gestor {id} não encontrada", 1)
            return marshal(message), 404

        logger.info(f"Gestor {id} encontrada com sucesso!")
        return marshal(gestor, gestor_fields), 200