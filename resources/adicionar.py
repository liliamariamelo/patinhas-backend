from resources.parceiro import Parceiro
from resources.gestor import Gestor
from resources.animal import Animal
from model.parceiro import *
from model.gestor import *
from model.animal import *
from model.message import *
from flask_restful import Resource, reqparse, marshal
from psycopg2 import IntegrityError
from helpers.base_logger import logger
from helpers.database import db
import re
from password_strength import PasswordPolicy


class AdicionarParceiro(Resource):
    def post(self):
        padrao_email =  r'^[\w\.-]+@[\w\.-]+\.\w+$'
        padrao_senha = PasswordPolicy.from_names(
            length = 8,
            uppercase = 1,
            numbers = 1,
            special = 1
        )
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str)
        parser.add_argument('cpf', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('senha', type=str)
        parser.add_argument('nascimento', type=str)
        parser.add_argument('telefone', type=str)
        args = parser.parse_args()
        try:
            nome = args["nome"]
            email = args["email"]
            senha = args["senha"]
            cpf = args["cpf"]
            nascimento = args["nascimento"]
            telefone = args["telefone"]

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
            
            parceiro = Parceiro(nome, cpf, email, senha, nascimento, telefone )

            db.session.add(parceiro)
            db.session.commit()

            logger.info("Parceiro cadastrada com sucesso!")

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

class AdicionarGestor(Resource):
    def post(self):
        padrao_email =  r'^[\w\.-]+@[\w\.-]+\.\w+$'

        padrao_senha = PasswordPolicy.from_names(
            length = 8,
            uppercase = 1,
            numbers = 1,
            special = 1
        )
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str)
        parser.add_argument('cpf', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('senha', type=str)
        parser.add_argument('nascimento', type=str)
        parser.add_argument('telefone', type=str)
        #parser.add_argument('id_ong', type=str)
        args = parser.parse_args()

        try:
            nome = args["nome"]
            cpf = args["cpf"]
            email = args["email"]
            senha = args["senha"]
            nascimento = args["nascimento"]
            telefone = args["telefone"]
            #id_ong = args["id_ong"]

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
            
            gestor = Gestor(nome, cpf, email, senha, nascimento, telefone)

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

class AdicionarAnimal(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str)
        parser.add_argument('especie', type=str)
        parser.add_argument('raca', type=str)
        parser.add_argument('idade', type=int)
        parser.add_argument('origem', type=str)
        parser.add_argument('descricao_origem', type=str)
        parser.add_argument('vacina_em_dia', type=bool)
        args = parser.parse_args()

        try:
            nome = args["nome"]
            especie = args["especie"]
            raca = args["raca"]
            idade = args["idade"]
            origem = args["origem"]
            descricao_origem = args["descricao_origem"]
            vacina_em_dia = args["vacina_em_dia"]

            if (
                not nome or len(nome) < 3 or
                not especie or len(especie) < 3 or
                not raca or len(raca) < 3 or
                not origem or len(origem) < 3 or
                not descricao_origem or len(descricao_origem) < 3 or
                idade <= 0
            ):
                return {"message": "Campos obrigatórios não podem ser nulos e devem ter no mínimo três caracteres, e a idade deve ser maior que zero"}, 400

            if vacina_em_dia not in [True, False]:
                return {"message": "O valor de 'vacina_em_dia' deve ser True ou False"}, 400

        
            animal = Animal(nome, especie, raca, idade, origem, descricao_origem, vacina_em_dia)

            db.session.add(animal)
           
            db.session.commit()

            logger.info("Animal cadastrado com sucesso!")

            return marshal(animal, animal_fields), 201
        except Exception as e:
            logger.error(f"Erro: {e}")

            message = Message("Erro ao cadastrar o animal", 2)
            return marshal(message, message_fields), 404
