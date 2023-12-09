from flask_restful import Resource, reqparse, marshal
from model.animal import Animal, animal_fields
from model.vacina import *
from model.message import *
from helpers.base_logger import logger
from helpers.database import db


parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema no nome', required=True)
parser.add_argument('especie', type=str, help='Problema no especie', required=True)
parser.add_argument('raca', type=str, help='Problema no raca', required=True)
parser.add_argument('idade', type=int, help='Problema no idade', required=True)
parser.add_argument('vacina_em_dia', type=bool, help='Problema se as vacinas estão em dia', required=True)

class Animais(Resource):
    def get(self):
        logger.info("Animais listados com sucesso!")
        animais = Animal.query.all()
        return marshal(animais, animal_fields), 200

    def post(self):
        args = parser.parse_args()


        try:
            nome = args["nome"]
            especie = args["especie"]
            raca = args["raca"]
            idade = args["idade"]
            vacina_em_dia = args["vacina_em_dia"]



            if (
                not nome or len(nome) < 3 or
                not especie or len(especie) < 3 or
                not raca or len(raca) < 3 or
                idade <= 0
            ):
                return {"message": "Campos obrigatórios não podem ser nulos e devem ter no mínimo três caracteres, e a idade deve ser maior que zero"}, 400

            if vacina_em_dia not in [True, False]:
                return {"message": "O valor de 'vacina_em_dia' deve ser True ou False"}, 400


            animal = Animal(nome, especie, raca, idade, vacina_em_dia)


            db.session.add(animal)
            db.session.commit()

            logger.info("Animal cadastrado com sucesso!")

            return marshal(animal, animal_fields), 201
        except Exception as e:
            logger.error(f"Erro: {e}")

            message = Message("Erro ao cadastrar o animal", 2)
            return marshal(message, message_fields), 404

class AnimalById(Resource):
    def get(self, id):
        animal = Animal.query.get(id)

        if animal is None:
            logger.error(f"Animal {id} não encontrada")

            message = Message(f"Animal {id} não encontrada", 1)
            return marshal(message, message_fields), 404

        logger.info(f"Animal {id} encontrada com sucesso!")
        return marshal(animal, animal_fields)


    def put(self, id):
        args = parser.parse_args()

        try:
            animal = Animal.query.get(id)

            if animal is None:
                logger.error(f"Animal {id} não encontrada")
                message = Message(f"Animal {id} não encontrada", 1)
                return marshal(message, message_fields)

            animal.nome = args["nome"]
            animal.especie = args["especie"]
            animal.raca = args["raca"]
            animal.idade = args["idade"]
            animal.vacina_em_dia = args["vacina_em_dia"]

            db.session.add(animal)
            db.session.commit()

            logger.info("Animal cadastrada com sucesso!")
            return marshal(animal, animal_fields), 200
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao atualizar animal", 2)
            return marshal(message, message_fields), 404


    def delete(self, id):
        animal = Animal.query.get(id)

        if animal is None:
            logger.error(f"Animal {id} não encontrada")
            message = Message(f"Animal {id} não encontrada", 1)
            return marshal(message, message_fields)

        db.session.delete(animal)
        db.session.commit()

        message = Message("Animal deletada com sucesso!", 3)
        return marshal(message, message_fields), 200

class AnimalByNome(Resource):
    def get(self, nome):
        animal = Animal.query.filter_by(nome=nome).all()

        if animal is None:
            logger.error(f"Animal {id} não encontrado")

            message = Message(f"Animal {id} não encontrado", 1)
            return marshal(message, message_fields), 404

        logger.info(f"Animal {id} encontrado com sucesso!")
        return marshal(animal, animal_fields), 200

# class AnimalMe(Resource):
#     def get(self):
#         animal = Animal.query

#         if animal is None:
#             logger.error(f"Animal {id} não encontrada")

#             message = Message(f"Animal {id} não encontrada", 1)
#             return marshal(message, message_fields), 404

#         logger.info(f"Animal {id} encontrada com sucesso!")
#         return marshal(animal, animal_fields), 200

