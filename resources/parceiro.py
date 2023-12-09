from sqlalchemy.exc import IntegrityError
from flask_restful import Resource, reqparse, marshal
from model.parceiro import *
from model.message import *
from helpers.base_logger import logger
from helpers.database import db
import re
from password_strength import PasswordPolicy

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema no nome', required=True)
parser.add_argument('cpf', type=str, help='Problema no cpf', required=True)
parser.add_argument('nascimento', type=str, help='Problema no nascimento', required=True)
parser.add_argument('telefone', type=str, help='Problema no telefone', required=True)
parser.add_argument('email', type=str, help='Problema no email', required=True)
parser.add_argument('senha', type=str, help='Problema no senha', required=True)


class Parceiros(Resource):
    def get(self):
        logger.info("Parceiros listadas com sucesso!")
        parceiros = Parceiro.query.all()
        return marshal(parceiros, parceiro_fields), 200

    def post(self):
        padrao_email =  r'^[\w\.-]+@[\w\.-]+\.\w+$'
        padrao_senha = PasswordPolicy.from_names(
            length = 8,
            uppercase = 1,
            numbers = 1,
            special = 1
        )
        args = parser.parse_args()
        try:
            nome = args["nome"]
            cpf = args["cpf"]
            nascimento = args["nascimento"]
            telefone = args["telefone"]
            email = args["email"]
            senha = args["senha"]

            if not nome or len(nome) < 3:
                logger.info("Nome não informado ou não tem no mínimo 3 caracteres")
                message = Message("Nome não informado ou não tem no mínimo 3 caracteres", 2)
                return marshal(message, message_fields), 400

            if not cpf:
                logger.info("CPF não informado")
                message = Message("CPF não informado", 2)
                return marshal(message, message_fields), 400

            if not re.match(r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$', cpf):
                logger.info("CPF não informado")
                message = Message("CPF informado incorretamente", 2)
                return marshal(message, message_fields), 400


            if not nascimento:
                logger.info("nascimento não informado")
                message = Message("nascimento não informado", 2)
                return marshal(message, message_fields), 400

            if not telefone:
                logger.info("Telefone não informado")
                message = Message("Telefone não informado", 2)
                return marshal(message, message_fields), 400

            if not re.match(r'^\d{11}$', telefone):
                logger.info("Telefone não informado")
                message = Message("Telefone informado incorretamente", 2)
                return marshal(message, message_fields), 400

            if not email:
                logger.info("Email não informado")
                message = Message("Email não informado", 2)
                return marshal(message, message_fields), 400

            if re.match(padrao_email, email) == None:
                logger.info("Email informado incorretamente")
                message = Message("Email informado incorretamente", 2)
                return marshal(message, message_fields), 400

            if not senha:
                logger.info("Senha não informada")
                message = Message("Senha não informada", 2)
                return marshal(message, message_fields), 400

            verifySenha = padrao_senha.test(senha)
            if len(verifySenha) != 0:
                message = Message("Senha informada incorretamente", 2)
                return marshal(message, message_fields), 400

            parceiro = Parceiro(nome, cpf, nascimento, telefone, email, senha)

            db.session.add(parceiro)
            db.session.commit()

            logger.info("Parceiro cadastrado com sucesso!")

            return marshal(parceiro, parceiro_fields), 201

        except IntegrityError as e:
            if 'cpf' in str(e.orig):
                message = Message("CPF já existe!", 2)
                return marshal(message, message_fields), 409

            elif 'email' in str(e.orig):
                message = Message("Email já existe!", 2)
                return marshal(message, message_fields), 409

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
            return marshal(message, message_fields), 404

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
            parceiro.nascimento = args["nascimento"]
            parceiro.telefone = args["telefone"]
            parceiro.email = args["email"]
            parceiro.senha = args["senha"]

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
            return marshal(message, message_fields), 404

        logger.info(f"Parceiro {id} encontrado com sucesso!")
        return marshal(parceiro, parceiro_fields), 200

class ParceiroMe(Resource):
    def get(self):
        parceiro = Parceiro.query

        if parceiro is None:
            logger.error(f"Parceiro {id} não encontrada")

            message = Message(f"Parceiro {id} não encontrada", 1)
            return marshal(message, message_fields), 404

        logger.info(f"Parceiro {id} encontrada com sucesso!")
        return marshal(parceiro, parceiro_fields), 200