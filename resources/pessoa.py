from flask_restful import Resource, reqparse, marshal
from model.pessoa import *
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


class Pessoas(Resource):
    def get(self):
        logger.info("Pessoas listadas com sucesso!")
        pessoas = Pessoa.query.all()
        return marshal(pessoas, pessoa_fields), 200

    def post(self):
        args = parser.parse_args()
        try:
            nome = args["nome"]
            cpf = args["cpf"]
            email = args["email"]
            senha = args["senha"]
            nascimento = args["nascimento"]
            telefone = args["telefone"]

            pessoa = Pessoa(nome, cpf, email, senha, nascimento, telefone)

            db.session.add(pessoa)
            db.session.commit()

            logger.info("Pessoa cadastrada com sucesso!")

            return marshal(pessoa, pessoa_fields), 201
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao cadastrar pessoa", 2)
            return marshal(message, message_fields), 404

class PessoaById(Resource):
    def get(self, id):
        pessoa = Pessoa.query.get(id)

        if pessoa is None:
            logger.error(f"Pessoa {id} não encontrada")

            message = Message(f"Pessoa {id} não encontrada", 1)
            return marshal(message), 404

        logger.info(f"Pessoa {id} encontrada com sucesso!")
        return marshal(pessoa, pessoa_fields)


    def put(self, id):
        args = parser.parse_args()

        try:
            pessoa = Pessoa.query.get(id)

            if pessoa is None:
                logger.error(f"Pessoa {id} não encontrada")
                message = Message(f"Pessoa {id} não encontrada", 1)
                return marshal(message, message_fields)

            pessoa.nome = args["nome"]
            pessoa.cpf = args["cpf"]
            pessoa.email = args["email"]
            pessoa.senha = args["senha"]
            pessoa.nascimento = args["nascimento"]
            pessoa.telefone = args["telefone"]
            
            db.session.add(pessoa)
            db.session.commit()

            logger.info("Pessoa cadastrada com sucesso!")
            return marshal(pessoa, pessoa_fields), 200
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao atualizar pessoa", 2)
            return marshal(message, message_fields), 404

   
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

class PessoaByNome(Resource):
    def get(self, nome):
        pessoa = Pessoa.query.filter_by(nome=nome).all()

        if pessoa is None:
            logger.error(f"Pessoa {id} não encontrado")

            message = Message(f"Pessoa {id} não encontrado", 1)
            return marshal(message), 404

        logger.info(f"Pessoa {id} encontrado com sucesso!")
        return marshal(pessoa, pessoa_fields), 200

class PessoaMe(Resource):
    def get(self):
        pessoa = Pessoa.query

        if pessoa is None:
            logger.error(f"Pessoa {id} não encontrada")

            message = Message(f"Pessoa {id} não encontrada", 1)
            return marshal(message), 404

        logger.info(f"Pessoa {id} encontrada com sucesso!")
        return marshal(pessoa, pessoa_fields), 200