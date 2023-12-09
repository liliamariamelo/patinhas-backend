from resources.parceiro import Parceiro
from resources.gestor import Gestor
from resources.ong import *
from resources.animal import Animal
from model.parceiro import *
from model.gestor import *
from model.ong import *
from model.animal import *
from helpers.database import db
from helpers.base_logger import logger
from flask_restful import Resource, reqparse, marshal
from model.message import *
import re
from password_strength import PasswordPolicy

class AtualizarParceiro(Resource):
    def put(self, id):
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
            parceiro = Parceiro.query.get(id)

            if parceiro is None:
                logger.error(f"Parceiro {id} não encontrada")
                message = Message(f"Parceiro {id} não encontrada", 1)
                return marshal(message, message_fields), 404
            
            if args['nome']:
                parceiro.nome = args['nome']
            if args['cpf']:
                parceiro.cpf = args['cpf']
            if args['email']:
                parceiro.email = args['email']
            if args['senha']:
                parceiro.senha = args['senha']
            if args['nascimento']:
                parceiro.nascimento = args['nascimento']
            if args['telefone']:
                parceiro.telefone = args['telefone']


            if not args['nome'] or len(args['nome']) < 3:
                logger.info("Nome não informado ou não tem no mínimo 3 caracteres")
                message = Message("Nome não informado ou não tem no mínimo 3 caracteres", 2)
                return marshal(message, message_fields), 400
            
            if not args['nascimento']:
                logger.info("nascimento não informado")
                message = Message("nascimento não informado", 2)
                return marshal(message, message_fields), 400
            
            if not args['email']:
                logger.info("Email não informado")
                message = Message("Email não informado", 2)
                return marshal(message, message_fields), 400

            if re.match(r'^[\w\.-]+@[\w\.-]+$', args['email']) is None:
                logger.info("Email informado incorretamente")
                message = Message("Email informado incorretamente", 2)
                return marshal(message, message_fields), 400
            
            if args['cpf'] and not re.match(r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$', args['cpf']):
                logger.info("CPF não informado")
                message = Message("CPF informado incorretamente", 2)
                return marshal(message, message_fields), 400
            
            if not args['telefone']:
                logger.info("Telefone não informado")
                message = Message("Telefone não informado", 2)
                return marshal(message, message_fields), 400
            
            if not re.match(r'^\d{11}$', args['telefone']):
                logger.info("Telefone não informado")
                message = Message("Telefone informado incorretamente", 2)
                return marshal(message, message_fields), 400
            
            if not args['senha']:
                logger.info("Senha não informada")
                message = Message("Senha não informada", 2)
                return marshal(message, message_fields), 400
            
            if args['senha'] and len(padrao_senha.test(args['senha'])) != 0:
                message = Message("Senha informada incorretamente", 2)
                return marshal(message, message_fields), 400

            db.session.commit()

            logger.info("Parceiro atualizada com sucesso!")
            return marshal(parceiro, parceiro_fields), 200
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao atualizar parceiro", 2)
            return marshal(message, message_fields), 404

class AtualizarGestor(Resource):
    def put(self, id):
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
            gestor = Gestor.query.get(id)

            if gestor is None:
                logger.error(f"Gestor {id} não encontrada")
                message = Message(f"Gestor {id} não encontrada", 1)
                return marshal(message, message_fields)
            
            if args['nome']:
                gestor.nome = args['nome']
            if args['cpf']:
                gestor.cpf = args['cpf']
            if args['email']:
                gestor.email = args['email']
            if args['senha']:
                gestor.senha = args['senha']
            if args['nascimento']:
                gestor.nascimento = args['nascimento']
            if args['telefone']:
                gestor.telefone = args['telefone']


            if not args['nome'] or len(args['nome']) < 3:
                logger.info("Nome não informado ou não tem no mínimo 3 caracteres")
                message = Message("Nome não informado ou não tem no mínimo 3 caracteres", 2)
                return marshal(message, message_fields), 400
            
            if not args['nascimento']:
                logger.info("nascimento não informado")
                message = Message("nascimento não informado", 2)
                return marshal(message, message_fields), 400
            
            
            if not args['email']:
                logger.info("Email não informado")
                message = Message("Email não informado", 2)
                return marshal(message, message_fields), 400

            if re.match(r'^[\w\.-]+@[\w\.-]+$', args['email']) is None:
                logger.info("Email informado incorretamente")
                message = Message("Email informado incorretamente", 2)
                return marshal(message, message_fields), 400
            
            if args['cpf'] and not re.match(r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$', args['cpf']):
                logger.info("CPF não informado")
                message = Message("CPF informado incorretamente", 2)
                return marshal(message, message_fields), 400
            
            if not args['telefone']:
                logger.info("Telefone não informado")
                message = Message("Telefone não informado", 2)
                return marshal(message, message_fields), 400
            
            if not re.match(r'^\d{11}$', args['telefone']):
                logger.info("Telefone não informado")
                message = Message("Telefone informado incorretamente", 2)
                return marshal(message, message_fields), 400
            
            if not args['senha']:
                logger.info("Senha não informada")
                message = Message("Senha não informada", 2)
                return marshal(message, message_fields), 400
            
            if args['senha'] and len(padrao_senha.test(args['senha'])) != 0:
                message = Message("Senha informada incorretamente", 2)
                return marshal(message, message_fields), 400

            db.session.commit()

            logger.info("Gestor atualizada com sucesso!")
            return marshal(gestor, gestor_fields), 200
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao atualizar gestor", 2)
            return marshal(message, message_fields), 404
        
class AtualizarAnimal(Resource):

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str)
        parser.add_argument('especie', type=str)
        parser.add_argument('raca', type=str)
        parser.add_argument('idade', type=str)
        parser.add_argument('vacina_em_dia', type=bool)
        args = parser.parse_args()

        
        try:
            animal = Animal.query.get(id)

            if animal is None:
                logger.error(f"Animal {id} não encontrada")
                message = Message(f"Animal {id} não encontrada", 1)
                return marshal(message, message_fields)
            
            if args['nome']:
                animal.nome = args['nome']
            if args['especie']:
                animal.especie = args['especie']
            if args['raca']:
                animal.raca = args['raca']
            if args['idade']:
                animal.idade = args['idade']
            if args['vacina_em_dia']:
                animal.vacina_em_dia = args['vacina_em_dia']

            if not args['nome'] or len(args['nome']) < 3:
                logger.info("Nome não informado ou não tem no mínimo 3 caracteres")
                message = Message("Nome não informado ou não tem no mínimo 3 caracteres", 2)
                return marshal(message, message_fields), 400
            
            if not args['especie'] or len(args['especie']) < 3:
                logger.info("Especie não informado ou não tem no mínimo 3 caracteres")
                message = Message("Especie não informado ou não tem no mínimo 3 caracteres", 2)
                return marshal(message, message_fields), 400
            
            if not args['raca'] or len(args['raca']) < 3:
                logger.info("Raça não informado ou não tem no mínimo 3 caracteres")
                message = Message("Raça não informado ou não tem no mínimo 3 caracteres", 2)
                return marshal(message, message_fields), 400
            
            if not args['idade'] or len(args['idade']) < 0:
                logger.info("Idade não informado ou não tem no mínimo 3 caracteres")
                message = Message("Idade não informado ou não tem no mínimo 3 caracteres", 2)
                return marshal(message, message_fields), 400
            
            if args['vacina_em_dia'] not in [True, False]:
                return {"message": "O valor de 'vacina_em_dia' deve ser True ou False"}, 400

            db.session.commit()

            logger.info("Animal atualizada com sucesso!")
            return marshal(animal, animal_fields), 200
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao atualizar Animal", 2)
            return marshal(message, message_fields), 404
        
class AtualizarOng(Resource):
    def put(self, id):
        padrao_senha = PasswordPolicy.from_names(
            length=8,
            uppercase=1,
            numbers=1,
            special=1
        )
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str)
        parser.add_argument('cnpj', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('senha', type=str)
        parser.add_argument('telefone', type=str)
        parser.add_argument('logradouro', type=str)
        parser.add_argument('numero', type=int)
        parser.add_argument('bairro', type=str)
        parser.add_argument('complemento', type=str)
        parser.add_argument('referencia', type=str)
        parser.add_argument('cep', type=str)
        parser.add_argument('cidade', type=str)
        parser.add_argument('estado', type=str)
        args = parser.parse_args()

        try:
            ong = ONG.query.get(id)

            if ong is None:
                logger.error(f"ONG {id} não encontrada")
                message = Message(f"ONG {id} não encontrada", 1)
                return marshal(message, message_fields), 404  # HTTP 404 para recurso não encontrado

            if args['nome']:
                ong.nome = args['nome']
            if args['cnpj']:
                ong.cnpj = args['cnpj']
            if args['email']:
                ong.email = args['email']
            if args['senha']:
                ong.senha = args['senha']
            if args['telefone']:
                ong.telefone = args['telefone']
            if args['logradouro']:
                ong.logradouro = args['logradouro']
            if args['numero']:
                ong.numero = args['numero']
            if args['bairro']:
                ong.bairro = args['bairro']
            if args['complemento']:
                ong.complemento = args['complemento']
            if args['referencia']:
                ong.referencia = args['referencia']
            if args['cep']:
                ong.cep = args['cep']
            if args['cidade']:
                ong.cidade = args['cidade']
            if args['estado']:
                ong.estado = args['estado']
            if args['id_gestor']:
                ong.id_gestor = args['id_gestor']

            if not args['nome'] or len(args['nome']) < 3:
                logger.info("Nome não informado ou não tem no mínimo 3 caracteres")
                message = Message("Nome não informado ou não tem no mínimo 3 caracteres", 2)
                return marshal(message, message_fields), 400

            if not args['email']:
                logger.info("Email não informado")
                message = Message("Email não informado", 2)
                return marshal(message, message_fields), 400

            if re.match(r'^[\w\.-]+@[\w\.-]+$', args['email']) is None:
                logger.info("Email informado incorretamente")
                message = Message("Email informado incorretamente", 2)
                return marshal(message, message_fields), 400

            if args['cnpj'] and not re.match(r'^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$', args['cnpj']):
                logger.info("CNPJ informado incorretamente")
                message = Message("CNPJ informado incorretamente", 2)
                return marshal(message, message_fields), 400

            if not args['telefone']:
                logger.info("Telefone não informado")
                message = Message("Telefone não informado", 2)
                return marshal(message, message_fields), 400

            if not re.match(r'^\d{11}$', args['telefone']):
                logger.info("Telefone informado incorretamente")
                message = Message("Telefone informado incorretamente", 2)
                return marshal(message, message_fields), 400

            if not args['senha']:
                logger.info("Senha não informada")
                message = Message("Senha não informada", 2)
                return marshal(message, message_fields), 400

            if args['senha'] and len(padrao_senha.test(args['senha'])) != 0:
                logger.info("Senha informada incorretamente")
                message = Message("Senha informada incorretamente", 2)
                return marshal(message, message_fields), 400

            if (
                not args['logradouro'] or len(args['logradouro']) < 3 or
                not args['bairro'] or len(args['bairro']) < 3 or
                not args['complemento'] or len(args['complemento']) < 3 or
                not args['referencia'] or len(args['referencia']) < 3 or
                not args['cidade'] or len(args['cidade']) < 3 or 
                not args['estado'] or len(args['estado']) < 3
            ):
                logger.info("O campo não informado ou não tem no mínimo 3 caracteres")
                message = Message("O campo não informado ou não tem no mínimo 3 caracteres", 2)
                return marshal(message, message_fields), 400
            db.session.commit()

            logger.info("ONG atualizada com sucesso!")
            return marshal(ong, ong_fields), 200  # HTTP 200 para sucesso
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao atualizar a ong", 2)
            return marshal(message, message_fields), 500  # HTTP 500 para erro interno do servidor
