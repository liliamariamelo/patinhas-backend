from resources.parceiro import Parceiro
from resources.gestor import Gestor
from resources.ong import Ong
from resources.animal import Animal
from resources.endereco import Endereco
from model.pessoa import *
from model.parceiro import *
from model.gestor import *
from model.ong import *
from model.animal import *
from model.message import *
from flask_restful import Resource, reqparse, marshal
from psycopg2 import IntegrityError
from helpers.base_logger import logger
from helpers.database import db
import re
from password_strength import PasswordPolicy


class AdicionarPessoa(Resource):
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
            cpf = args["cpf"]
            email = args["email"]
            senha = args["senha"]
            nascimento = args["nascimento"]
            telefone = args["telefone"]
            #pessoa = Pessoa.query.get(id)

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
            

            pessoa = Pessoa(nome, cpf, email, senha, nascimento, telefone)

            db.session.add(pessoa)
            db.session.commit()

            logger.info("Pessoa cadastrada com sucesso!")

            return marshal(pessoa, pessoa_fields), 201
        
        except IntegrityError as e:
            if 'cpf' in str(e.orig):
                message = Message("CPF já existe!", 2)
                return marshal(message, message_fields), 409
            
            elif 'email' in str(e.orig):
                message = Message("Email já existe!", 2)
                return marshal(message, message_fields), 409

        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao cadastrar pessoa", 2)
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
           
           # vacina = Vacina(
            #    args["vacina"]["nome"],
             #   animal
            #)

           # db.session.add(vacina)

            db.session.commit()

            logger.info("Animal cadastrado com sucesso!")

            return marshal(animal, animal_fields), 201
        except Exception as e:
            logger.error(f"Erro: {e}")

            message = Message("Erro ao cadastrar o animal", 2)
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
        parser.add_argument('id_ong', type=str)
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

'''class AdicionarOng(Resource):
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
        parser.add_argument('cnpj', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('senha', type=str)
        parser.add_argument('telefone', type=str)
        parser.add_argument('id_endereco', type=dict)
        args = parser.parse_args()
        args = parser.parse_args()
        try:
            nome = args["nome"]
            email = args["email"]
            senha = args["senha"]
            cnpj = args["cnpj"]
            telefone = args["telefone"]
            enderecoResponse = args["endereco"]
            #Criar endereço 
            endereco = Endereco(
                cep=enderecoResponse["cep"],
                numero=enderecoResponse["numero"],
                complemento=enderecoResponse["complemento"],
                bairro=enderecoResponse["bairro"],
                referencia=enderecoResponse["referencia"],
                logradouro=enderecoResponse["logradouro"],
                cidade=enderecoResponse["cidade"],
                estado=enderecoResponse["estado"]
            )

            if not nome or len(nome) < 3:
                logger.info("Nome não informado ou não tem no mínimo 3 caracteres")
                message = Message("Nome não informado ou não tem no mínimo 3 caracteres", 2)
                return marshal(message, message_fields), 400

            if not endereco:
                logger.info("Endereço não informado")
                message = Message("Endereço não informado", 2)
                return marshal(message, message_fields), 400
            
            if not email:
                logger.info("Email não informado")
                message = Message("Email não informado", 2)
                return marshal(message, message_fields), 400

            if re.match(padrao_email, email) == None:
                logger.info("Email informado incorretamente")
                message = Message("Email informado incorretamente", 2)
                return marshal(message, message_fields), 400
            
            if not cnpj:
                logger.info("CNPJ não informado")
                message = Message("CNPJ não informado", 2)
                return marshal(message, message_fields), 400
            
            if not re.match(r'^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$', cnpj):
                logger.info("CNPJ não informado")
                message = Message("CNPJ informado incorretamente", 2)
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

            db.session.add(endereco)
            db.session.commit()

            ong = Ong(nome, cnpj, email, senha, telefone, id_endereco=endereco.id)

            db.session.add(ong)
            db.session.commit()

            logger.info("ONG cadastrada com sucesso!")

            return marshal(ong, ong_fields), 201
        
        except IntegrityError as e:
            if 'cnpj' in str(e.orig):
                message = Message("CNPJ já existe!", 2)
                return marshal(message, message_fields), 409
            
            elif 'email' in str(e.orig):
                message = Message("Email já existe!", 2)
                return marshal(message, message_fields), 409
            

        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao cadastrar a ong", 2)
            return marshal(message, message_fields), 404'''