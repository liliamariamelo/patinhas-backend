from psycopg2 import IntegrityError
from flask_restful import Resource, reqparse, marshal
from model.ong import *
from model.gestor import *
from model.message import *
from helpers.database import db
from helpers.base_logger import logger
from password_strength import PasswordPolicy
import re

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema no nome da ong', required=True)
parser.add_argument('cnpj', type=str, help='Problema no cnpj', required=True)
parser.add_argument('telefone', type=str, help='Problema no telefone', required=True)
parser.add_argument('email', type=str, help='Problema no email', required=True)
parser.add_argument('senha', type=str, help='Problema no senha', required=True)
parser.add_argument('logradouro', type=str, help='Problema no logradouro', required=True)
parser.add_argument('numero', type=int, help='Problema no numero', required=True)
parser.add_argument('bairro', type=str, help='Problema no bairro', required=True)
parser.add_argument('complemento', type=str, help='Problema na complemento', required=True)
parser.add_argument('referencia', type=str, help='Problema no referencia', required=True)
parser.add_argument('cep', type=str, help='Problema no cep', required=True)
parser.add_argument('cidade', type=str, help='Problema na cidade', required=True)
parser.add_argument('estado', type=str, help='Problema no estado', required=True)
parser.add_argument('id_gestor', type=int, help='Problema no id de gestor', required=True)

class AdicionarONG(Resource):
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
            cnpj = args["cnpj"]
            telefone = args["telefone"]
            email = args["email"]
            senha = args["senha"]
            logradouro = args["logradouro"],
            numero = args["numero"],
            bairro = args["bairro"],
            complemento = args["complemento"],
            referencia = args["referencia"],
            cep = args["cep"],
            cidade=args["cidade"],
            estado=args["estado"],
            id_gestor=args["id_gestor"]
            

            if not nome or len(nome) < 3:
                logger.info("Nome não informado ou não tem no mínimo 3 caracteres")
                message = Message("Nome não informado ou não tem no mínimo 3 caracteres", 2)
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
            
            if (
                not logradouro or len(logradouro) < 3 or
                not bairro or len(bairro) < 3 or
                not complemento or len(complemento) < 3 or
                not referencia or len(referencia) < 3 or
                not cidade or len(cidade) < 3 or 
                not estado or len(estado) < 3
            ):
                logger.info("O campo não informado ou não tem no mínimo 3 caracteres")
                message = Message("O campo não informado ou não tem no mínimo 3 caracteres", 2)
                return marshal(message, message_fields), 400

            db.session.add(ong)
            db.session.commit()

            ong = ONG(nome, cnpj, telefone, email, senha, logradouro, numero, bairro, complemento, referencia, cep, cidade, estado, id_gestor)

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
            return marshal(message, message_fields), 404


