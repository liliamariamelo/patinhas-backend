from flask_restful import Resource, reqparse, marshal
from model.agendamento import *
from model.message import *
from helpers.database import db
from helpers.base_logger import logger
from datetime import datetime, time
from model.parceiro import Parceiro
from model.animal import Animal

def parse_date(date_string):
  return datetime.strptime(date_string, '%Y-%m-%d')

def parse_time(time_string):
   return datetime.strptime(time_string, '%H:%M')



parser = reqparse.RequestParser()
parser.add_argument('data_visita', type=parse_date, help='Problema na data da visita informado', required=True)
parser.add_argument('hora_visita', type=parse_time, help='Problema na hora da visita informado', required=True)
parser.add_argument('id_animal', type=int, help='ID do animal associado ao agendamento', required=False)
parser.add_argument('id_parceiro', type=int, help='ID do parceiro associado ao agendamento', required=False)

class Agendamentos(Resource):
    def get(self):
        logger.info("Datas e horários disponíveis com sucesso!")
        agendamentos = Agendamento.query.all()
        return marshal(agendamentos, agendamento_fields), 200

    def post(self):
        args = parser.parse_args()

        # try:
        data_visita = args["data_visita"]
        hora_visita = args["hora_visita"]
        id_animal = args["id_animal"]
        id_parceiro = args["id_parceiro"]
        
        animal = Animal.query.get(id_animal)

        if animal is None:
            logger.error(f"Animal de id: {id_animal} nao encontrado")
            codigo = Message(f"Animal de id: {id_animal} nao encontrado", 1)
            return marshal(codigo, message_fields), 404
        
        parceiro = Parceiro.query.get(id_parceiro)

        if parceiro is None:
            logger.error(f"Parceiro de id: {id_animal} nao encontrado")
            codigo = Message(f"Parceiro de id: {id_animal} nao encontrado", 1)
            return marshal(codigo, message_fields), 404

        agendamento = Agendamento(data_visita, hora_visita, animal, parceiro)
        print(agendamento)
        db.session.add(agendamento)
        db.session.commit()
        logger.info("Data e hora da visita para adoção cadastrada com sucesso!")

        return marshal(agendamento, agendamento_fields), 201

        # except Exception as e:
        #     logger.error(f"Erro: {e}")

        #     message = Message("Erro ao cadastrar a data e hora da visita para adoção", 2)
        #     return marshal(message, message_fields), 404

class AgendamentoById(Resource):
    def get(self, id):
        agendamento = Agendamento.query.get(id)

        if agendamento is None:
            logger.error(f"Agendamento {id} não encontrado")

            message = Message(f"Agendamento {id} não encontrado", 1)
            return marshal(message, message_fields), 404

        logger.info(f"Agendamento {id} encontrado com sucesso!")
        return marshal(agendamento, agendamento_fields)

    def put(self, id):
        args = parser.parse_args()

        try:
            agendamento = Agendamento.query.get(id)

            if agendamento is None:
                logger.error(f"Agendamento {id} não encontrado")
                message = Message(f"Agendamento {id} não encontrado", 1)
                return marshal(message, message_fields), 404

            agendamento.data_visita = args["data_visita"]
            agendamento.hora_visita = args["hora_visita"]
            agendamento.id_animal = args["id_animal"]
            agendamento.id_parceiro = args["id_parceiro"]

            db.session.add(agendamento)
            db.session.commit()

            logger.info("Agendamento atualizado com sucesso!")
            return marshal(agendamento, agendamento_fields), 200

        except Exception as e:
            logger.error(f"Erro: {e}")

            message = Message("Erro ao atualizar o agendamento", 2)
            return marshal(message,message_fields), 404

    def delete(self, id):
        agendamento = Agendamento.query.get(id)

        if agendamento is None:
            logger.error(f"Agendamento {id} não encontrado")
            message = Message(f"Agendamento {id} não encontrado", 1)
            return marshal(message, message_fields), 404

        db.session.delete(agendamento)
        db.session.commit()

        message = Message("Agendamento deletado com sucesso!", 3)
        return marshal(message, message_fields), 200
