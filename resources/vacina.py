from flask_restful import Resource, reqparse, marshal
from model.vacina import *
from model.message import Message, message_fields
from helpers.database import db
from helpers.base_logger import logger

from model.animal import Animal, animal_fields

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema no nome', required=False)
parser.add_argument('animal_id', type=int, help='id do animal não informado', required=False)
parser.add_argument('vacina_id', type=int, help='id da vacina não informada', required=False)

class Vacinas(Resource):
    def get(self):
        logger.info("Vacinas listadas com sucesso!")
        vacinas = Vacina.query.all()
        return marshal(vacinas, vacina_fields), 200

    def post(self):
        args = parser.parse_args()

        try:
            if args["nome"] is None:
                logger.error("Nome nao informado")
                codigo = Message("Nome não informado", 1)
                return marshal(codigo, message_fields), 400

            nome = args["nome"]
            animal_id = args["animal_id"]

            if not nome or len(nome) < 3:
                return {"message": "O campo 'nome' não pode ser nulo e deve ter no mínimo três caracteres."}, 400

            vacina = Vacina(nome=nome, animal_id=animal_id)


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
            return marshal(message, message_fields), 404

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

class AnimalVacina(Resource):
    def post(self):
        args = parser.parse_args()
        # try:

        animal = Animal.query.get(args["animal_id"])
        if animal is None:
            logger.error(f"Animal de id: {args['animal_id']} nao encontrado")

            codigo = Message(f"Animal de id: {args['animal_id']} não encontrado", 1)
            return marshal(codigo, message_fields), 404
    
        vacina = Vacina.query.get(args["vacina_id"])
        if vacina is None:
            logger.error(f"Vacina de id: {args['vacina_id']} nao encontrada")

            codigo = Message(f"Vacina de id: {args['vacina_id']} não encontrada", 1)
            return marshal(codigo, message_fields), 404
        
        animal.vacinas.append(vacina)
        db.session.add(animal)
        db.session.commit()

        logger.info(f"Vacina de id: {args['vacina_id']} foi associada ao animal de id: {args['animal_id']}")
        return marshal(animal, animal_fields), 201
        # except Exception as e:
        #     logger.error(f"Erro ao criar a vacina: {str(e)}")
        #     codigo = Message(f"Erro ao criar a vacina: {str(e)}", 2)
        #     return marshal(codigo, message_fields), 400
