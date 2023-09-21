from flask_restful import Resource, reqparse, marshal
from model.endereco import *
from model.message import *
from helpers.database import db
from helpers.base_logger import logger

parser = reqparse.RequestParser()
parser.add_argument('cep', type=str, help= 'Problema no cep', required=True)
parser.add_argument('numero', type=str, help='Problema no número', required=True)
parser.add_argument('complemento', type=str, help='Problema no complemento', required=True)
parser.add_argument('bairro', type=str, help='Problema no bairro', required=True)
parser.add_argument('referencia', type=str, help='Problema na referência', required=True)
parser.add_argument('logradouro', type=str, help='Problema no logradouro', required=True)
parser.add_argument('cidade', type=str, help='Problema na cidade', required=True)
parser.add_argument('estado', type=str, help='Problema no estado', required=True)


class Enderecos(Resource):
    def get(self):
        logger.info("Endereço listado com sucesso!")
        enderecos = Endereco.query.all()
        return marshal(enderecos, endereco_fields), 200

    
    def post(self):
        args = parser.parse_args()
        try:
            cep = args["cep"]
            numero = args["numero"]
            complemento = args["complemento"]
            bairro = args["bairro"]
            referencia = args["referencia"]
            logradouro = args["logradouro"]
            cidade = args["cidade"]
            estado = args["estado"]

            endereco = Endereco(cep, numero, complemento, bairro, referencia, logradouro, cidade, estado)

            db.session.add(endereco)
            db.session.commit()
            logger.info("Endereço cadastrado com sucesso!")

            return marshal(endereco, endereco_fields), 201
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao cadastrar o endereço", 2)
            return marshal(message, message_fields), 404

class EnderecosById(Resource):
    def get(self, id):
        endereco = Endereco.query.get(id)

        if endereco is None:
            logger.error(f"Endereço {id} não encontrado")

            message = Message(f"Endereço {id} não encontrado", 1)
            return marshal(message), 404

        logger.info(f"Endereço {id} encontrado com sucesso!")
        return marshal(endereco, endereco_fields)

    
    def put(self, id):
        args = parser.parse_args()

        try:
            endereco = Endereco.query.get(id)

            if endereco is None:
                logger.error(f"Endereço {id} não encontrado")
                message = Message(f"Endereço {id} não encontrado", 1)
                return marshal(message, message_fields)

            endereco.cidade = args["cidade"]
            endereco.estado = args["estado"]
            endereco.bairro = args["bairro"]
            endereco.cep = args["cep"]
            endereco.numero = args["numero"]
            endereco.complemento = args["complemento"]
            endereco.referencia = args["referencia"]
            endereco.logradouro = args["logradouro"]

            db.session.add(endereco)
            db.session.commit()

            logger.info("Endereço cadastrado com sucesso!")
            return marshal(endereco, endereco_fields), 200
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao atualizar o endereço", 2)
            return marshal(message, message_fields), 404

   
    def delete(self, id):
        endereco = Endereco.query.get(id)

        if endereco is None:
            logger.error(f"Endereço {id} não encontrado")
            message = Message(f"Endereço {id} não encontrado", 1)
            return marshal(message, message_fields)

        db.session.delete(endereco)
        db.session.commit()

        message = Message("Endereço deletado com sucesso!", 3)
        return marshal(message, message_fields), 200

class EnderecosByLogradouro(Resource):
    def get(self, logradouro):
        endereco = Endereco.query.filter(
            Endereco.logradouro.ilike(f"%{logradouro}%")
        ).all()

        if endereco is None:
            logger.error(f"Endereço {id} não encontrado")

            message = Message(f"Endereço {id} não encontrado", 1)
            return marshal(message), 404

        logger.info(f"Endereço {id} encontrado com sucesso!")
        return marshal(endereco, endereco_fields), 200
