from flask_restful import Resource, reqparse, marshal
from model.ong import *
from model.endereco import *
from model.message import *
from helpers.database import db
from helpers.base_logger import logger


parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema no nome da ong', required=True)
parser.add_argument('cnpj', type=str, help='Problema no cnpj', required=True)
parser.add_argument('email', type=str, help='Problema no email', required=True)
parser.add_argument('senha', type=str, help='Problema no senha', required=True)
parser.add_argument('telefone', type=str, help='Problema no telefone', required=True)
parser.add_argument('endereco', type=dict, help='Problema no id_endereco', required=True)


class ONGs(Resource):
    def get(self):
        logger.info("ONGs listadas com sucesso!")
        ongs = Ong.query.all()
        return marshal(ongs, ong_fields), 200

    def post(self):
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

            db.session.add(endereco)
            db.session.commit()

            ong = Ong(nome, cnpj, email, senha, telefone, id_endereco=endereco.id)

            db.session.add(ong)
            db.session.commit()

            logger.info("ONG cadastrada com sucesso!")

            return marshal(ong, ong_fields), 201
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao cadastrar a ong", 2)
            return marshal(message, message_fields), 404

class ONGById(Resource):
    def get(self, id):
        ong = Ong.query.get(id)

        if ong is None:
            logger.error(f"ONG {id} não encontrada")

            message = Message(f"ONG {id} não encontrada", 1)
            return marshal(message), 404

        logger.info(f"ONG {id} encontrada com sucesso!")
        return marshal(ong, ong_fields)


    def put(self, id):
        args = parser.parse_args()

        try:
            ong = Ong.query.get(id)

            if ong is None:
                logger.error(f"ONG {id} não encontrada")
                message = Message(f"ONG {id} não encontrada", 1)
                return marshal(message, message_fields)

            ong.nome = args["nome"]
            ong.cnpj = args["cnpj"]
            ong.email = args["email"]
            ong.senha = args["senha"]
            ong.telefone = args["telefone"]
            ong.id_endereco = args["id_endereco"]
            
            db.session.add(ong)
            db.session.commit()

            logger.info("ONG cadastrada com sucesso!")
            return marshal(ong, ong_fields), 200
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao atualizar a ong", 2)
            return marshal(message, message_fields), 404

   
    def delete(self, id):
        ong = Ong.query.get(id)

        if ong is None:
            logger.error(f"ONG {id} não encontrada")
            message = Message(f"ONG {id} não encontrada", 1)
            return marshal(message, message_fields)

        db.session.delete(ong)
        db.session.commit()

        message = Message("ONG deletada com sucesso!", 3)
        return marshal(message, message_fields), 200

class ONGByNome(Resource):
    def get(self, nome):
        ong = Ong.query.filter_by(nome=nome).all()

        if ong is None:
            logger.error(f"ONG {id} não encontrado")

            message = Message(f"ONG {id} não encontrado", 1)
            return marshal(message), 404

        logger.info(f"ONG {id} encontrado com sucesso!")
        return marshal(ong, ong_fields), 200

class ONGMe(Resource):
    def get(self):
        ong = Ong.query

        if ong is None:
            logger.error(f"ONG {id} não encontrada")

            message = Message(f"ONG {id} não encontrada", 1)
            return marshal(message), 404

        logger.info(f"ONG {id} encontrada com sucesso!")
        return marshal(ong, ong_fields), 200