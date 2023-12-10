import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_restful import Resource, reqparse
from helpers.database import db
from model.parceiro import Parceiro
from model.agendamento import Agendamento
from helpers.base_logger import logger
import os
from dotenv import load_dotenv

load_dotenv()

parser = reqparse.RequestParser()
parser.add_argument('data_visita', type=str, help='Data da visita para adoção', required=True)
parser.add_argument('hora_visita', type=str, help='Hora da visita para adoção', required=True)
parser.add_argument('id_animal', type=int, help='ID do animal associado ao agendamento', required=False)
parser.add_argument('id_parceiro', type=int, help='ID do parceiro associado ao agendamento', required=False)

class EnviarEmailAgendamento(Resource):
    def get(self):
        logger.info("Emails listados com sucesso!")
        return {'message': 'Emails listados com sucesso!'}

    def post(self):
        try:
            args = parser.parse_args()

            agendamento = Agendamento(**args)
            parceiro = Parceiro.query.get(agendamento.id_parceiro)

            if not parceiro:
                raise ValueError('Erro: Parceiro não encontrado')

            destinatarios = [parceiro.email]
            mensagem = f"Olá, {parceiro.nome}, seu agendamento foi marcado !!!"

            if not all([destinatarios, mensagem]):
                raise ValueError('Erro: Todos os campos são obrigatórios')

            self.enviar_email(destinatarios, mensagem)

            self.enviar_email_confirmacao(agendamento, parceiro)

            return {'message': 'E-mail enviado com sucesso'}
        except ValueError as ve:
            logger.error(f"Erro ao enviar o e-mail: {ve}")
            return {'message': str(ve)}, 404
        except Exception as e:
            logger.error(f"Erro ao enviar o e-mail: {e}")
            return {'message': 'Erro ao enviar o e-mail'}, 404

    def enviar_email(self, destinatarios, mensagem):
        remetente = os.getenv('EMAIL')
        senha = os.getenv('SENHA')
        servidor_smtp = 'smtp.gmail.com'
        porta_smtp = 587

        with smtplib.SMTP(servidor_smtp, porta_smtp) as server:
            server.starttls()
            server.login(remetente, senha)

            for destinatario in destinatarios:
                mensagem_mime = MIMEMultipart()
                mensagem_mime['From'] = remetente
                mensagem_mime['To'] = destinatario
                mensagem_mime['Subject'] = 'Agendamento'
                mensagem_mime.attach(MIMEText(mensagem, 'plain'))

                server.sendmail(remetente, destinatario, mensagem_mime.as_string())

    def enviar_email_confirmacao(self, agendamento, parceiro):
        remetente = os.getenv('EMAIL')
        senha = os.getenv('SENHA')  # Use variáveis de ambiente para senhas
        servidor_smtp = 'smtp.gmail.com'
        porta_smtp = 587

        assunto = 'Confirmação de Agendamento'

        destinatario_email = parceiro.email
        corpo = f'Olá, {parceiro.nome}, seu agendamento para adoção foi confirmado.\nData: {agendamento.data_visita}\nHora: {agendamento.hora_visita}'

        with smtplib.SMTP(servidor_smtp, porta_smtp) as server:
            server.starttls()
            server.login(remetente, senha)

            mensagem_mime = MIMEMultipart()
            mensagem_mime['From'] = remetente
            mensagem_mime['To'] = destinatario_email
            mensagem_mime['Subject'] = assunto
            mensagem_mime.attach(MIMEText(corpo, 'plain'))

            server.sendmail(remetente, destinatario_email, mensagem_mime.as_string())
