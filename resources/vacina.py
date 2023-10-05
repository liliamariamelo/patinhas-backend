from flask_restful import Resource, reqparse, marshal
from model.vacina import *
from model.message import Message
from helpers.database import db
from helpers.base_logger import logger

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema no nome', required=True)

class Vacinas(Resource):
    def get(self):
        logger.info("Vacinas listadas com sucesso!")
        vacinas = Vacina.query.all()
        return marshal(vacinas, vacina_fields), 200

    def post(self):
        args = parser.parse_args()

        try:
            nome = args["nome"]

            if not nome or len(nome) < 3:
                return {"message": "O campo 'nome' não pode ser nulo e deve ter no mínimo três caracteres."}, 400

            vacina = Vacina(nome=nome)

            db.session.add(vacina)
            db.session.commit()
            logger.info("Vacina cadastrada com sucesso!")

            return marshal(vacina, vacina_fields), 201
        except Exception as e:
            logger.error(f"Erro: {e}")

            message = Message("Erro ao cadastrar a vacina", 2)
            return marshal(message, message_fields), 404

class VacinasById(Resource):
    def get(self, id):
        vacina = Vacina.query.get(id)

        if vacina is None:
            logger.error(f"Vacina {id} não encontrada")

            message = Message(f"Vacina {id} não encontrada", 1)
            return marshal(message), 404

        logger.info(f"Vacina {id} encontrada com sucesso!")
        return marshal(vacina, vacina_fields)

    def put(self, id):
        args = parser.parse_args()

        try:
            vacina = Vacina.query.get(id)

            if vacina is None:
                logger.error(f"Vacina {id} não encontrada")
                message = Message(f"Vacina {id} não encontrada", 1)
                return marshal(message, message_fields)

            vacina.nome = args["nome"]

            db.session.add(vacina)
            db.session.commit()

            logger.info("Vacina atualizada com sucesso!")
            return marshal(vacina, vacina_fields), 200
        except Exception as e:
            logger.error(f"Erro: {e}")

            message = Message("Erro ao atualizar a vacina", 2)
            return marshal(message, message_fields), 404

    def delete(self, id):
        vacina = Vacina.query.get(id)

        if vacina is None:
            logger.error(f"Vacina {id} não encontrada")
            message = Message(f"Vacina {id} não encontrada", 1)
            return marshal(message, message_fields)

        db.session.delete(vacina)
        db.session.commit()

        message = Message("Vacina deletada com sucesso!", 3)
        return marshal(message, message_fields), 200
