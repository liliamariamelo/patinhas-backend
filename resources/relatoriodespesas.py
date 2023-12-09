from flask_restful import Resource, reqparse, marshal
from model.relatoriodespesas import *
from model.message import *
from helpers.database import db
from helpers.base_logger import logger

def parse_date(date_string):
  return datetime.strptime(date_string, '%Y-%m-%d')

parser = reqparse.RequestParser()
parser.add_argument('categoria', type=str, help='Problema na categoria', required=True)
parser.add_argument('valor', type=float, help='Problema no valor das despesas', required=True)
parser.add_argument('data', type=parse_date, help='Problema na data', required=True)
parser.add_argument('mes_Correspondente', type=int, help='Problema no mês correspondente', required=True)

class RelatoriosDespesas(Resource):
    def get(self):
        logger.info("Relatório listadas com sucesso!")
        relatorio = RelatorioDespesas.query.all()
        return marshal(relatorio, relatoriodespesas_fields), 200

    def post(self):
        args = parser.parse_args()

        try:
            categoria = args["categoria"]
            valor = args["valor"]
            data = args["data"]
            mes_Correspondente = args["mes_Correspondente"]

            relatorio = RelatorioDespesas(categoria, valor, data, mes_Correspondente)

            db.session.add(relatorio)
            db.session.commit()

            logger.info("Relatório cadastrado com sucesso!")

            return marshal(relatorio, relatoriodespesas_fields), 201


        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao cadastrar ao relatório", 2)
            return marshal(message, message_fields), 404


class RelatorioDespesasById(Resource):
    def get(self, id):
        relatorio = RelatorioDespesas.query.get(id)

        if relatorio is None:
            logger.error(f"Relatório {id} não encontrada")

            message = Message(f"Relatório {id} não encontrada", 1)
            return marshal(message, message_fields), 404

        logger.info(f"Relatório {id} encontrada com sucesso!")
        return marshal(relatorio, relatoriodespesas_fields)


    def put(self, id):
        args = parser.parse_args()

        try:
            relatorio = RelatorioDespesas.query.get(id)

            if relatorio is None:
                logger.error(f"Relatório {id} não encontrada")
                message = Message(f"Relatório {id} não encontrada", 1)
                return marshal(message, message_fields)

            relatorio.categoria = args["categoria"]
            relatorio.valor = args["valor"]
            relatorio.data = args["data"]
            relatorio.mes_Correspondente = args["mes_Correspondente"]

            db.session.add(relatorio)
            db.session.commit()

            logger.info("Relatório cadastrada com sucesso!")
            return marshal(relatorio, relatoriodespesas_fields), 200
        except Exception as e:
            logger.error(f"error: {e}")

            message = Message("Erro ao atualizar a relatorio", 2)
            return marshal(message, message_fields), 404

    def delete(self, id):
        relatorio = RelatorioDespesas.query.get(id)

        if relatorio is None:
            logger.error(f"Relatório {id} não encontrada")
            message = Message(f"Relatório {id} não encontrada", 1)
            return marshal(message, message_fields)

        db.session.delete(relatorio)
        db.session.commit()

        message = Message("Relatório deletada com sucesso!", 3)
        return marshal(message, message_fields), 200

class RelatorioDespesasByMes(Resource):
    def get(self, mes_Correspondente):
        relatorio = RelatorioDespesas.query.filter_by(mes_Correspondente=mes_Correspondente).all()

        if relatorio is None:
            logger.error(f"Relatório {id} não encontrado")

            message = Message(f"Relatório {id} não encontrado", 1)
            return marshal(message, message_fields), 404

        logger.info(f"Relatório {id} encontrado com sucesso!")
        return marshal(relatorio, relatoriodespesas_fields), 200


