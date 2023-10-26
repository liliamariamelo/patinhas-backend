from flask_restful import Resource, reqparse, marshal
from model.gestor import *
from model.ong import *
from model.message import *
from helpers.database import db
from helpers.base_logger import logger
import re
from password_strength import PasswordPolicy

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
            email = args["email"]
            senha = args["senha"]
            nascimento = args["nascimento"]
            telefone = args["telefone"]
            id_ong = args["id_ong"]

            if not nome or len(nome) < 3:
                logger.info("Nome não informado ou não tem no mínimo 3 caracteres")
                message = Message("Nome não informado ou não tem no mínimo 3 caracteres", 2)
                return marshal(message, message_fields), 400
            
            if not nascimento:
                logger.info("nascimento não informado")
                message = Message("nascimento não informado", 2)
                return marshal(message, message_fields), 400
            
            if not email:
                logger.info("Email não informado")
                message = Message("Email não informado", 2)
                return marshal(message, message_fields), 400

            if re.match(padrao_email, email) == None:
                logger.info("Email informado incorretamente")
                message = Message("Email informado incorretamente", 2)
                return marshal(message, message_fields), 400
            
            if not cpf:
                logger.info("CPF não informado")
                message = Message("CPF não informado", 2)
                return marshal(message, message_fields), 400
            
            if not re.match(r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$', cpf):
                logger.info("CPF não informado")
                message = Message("CPF informado incorretamente", 2)
                return marshal(message, message_fields), 400
            
            if not telefone:
                logger.info("Telefone não informado")
                message = Message("Telefone não informado", 2)
                return marshal(message, message_fields), 400
            
            if not re.match(r'^\d{11}$', telefone):
                logger.info("Telefone não informado")
                message = Message("Telefone informado incorretamente", 2)
                return marshal(message, message_fields), 400
            
            if not senha:
                logger.info("Senha não informada")
                message = Message("Senha não informada", 2)
                return marshal(message, message_fields), 400
            
            verifySenha = padrao_senha.test(senha)
            if len(verifySenha) != 0:
                message = Message("Senha informada incorretamente", 2)
                return marshal(message, message_fields), 400
            
            gestor = Gestor(nome, cpf, email, senha, nascimento, telefone, id_ong )

            db.session.add(gestor)
            db.session.commit()

            logger.info("Gestor cadastrada com sucesso!")

            return marshal(gestor, gestor_fields), 201
        except IntegrityError as e:
            if 'cpf' in str(e.orig):
                message = Message("CPF já existe!", 2)
                return marshal(message, message_fields), 409
            
            elif 'email' in str(e.orig):
                message = Message("Email já existe!", 2)
                return marshal(message, message_fields), 409
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