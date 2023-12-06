import os
from dotenv import load_dotenv
from flask_restful import Api
from flask import Flask, Blueprint

from helpers.cors import cors
from helpers.database import db, migrate
from resources.pessoa import Pessoas
from resources.parceiro import Parceiros, ParceiroById, ParceiroByNome
from resources.gestor import Gestores, GestorById, GestorByNome
from resources.ong import ONGs, ONGByNome, ONGById
from resources.animal import Animais
from resources.listar import ListarTodos
from resources.deletar import  DeletarParceiro, DeletarAnimal, DeletarGestor, DeletarOng
from resources.atualizar import  AtualizarParceiro, AtualizarGestor, AtualizarAnimal, AtualizarOng
from resources.adicionar import  AdicionarAnimal, AdicionarGestor, AdicionarParceiro
from resources.adicionarongadmin import AdicionarONG
from resources.vacina import AnimalVacina, Vacinas
from resources.agendamento import Agendamentos
from resources.relatoriodespesas import RelatoriosDespesas, RelatorioByFiltro
load_dotenv()

# create the app
app = Flask(__name__)

# restful
api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix="/api")

postgresUser = os.getenv("POSTGRES_USER")
postgresPassword = os.getenv("POSTGRES_PASSWORD")

DB_URL = f"postgresql://{postgresUser}:{postgresPassword}@localhost:5432/abracepatinhas"
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# initialize the app with the extension
db.init_app(app)
cors.init_app(app)
migrate.init_app(app, db)

api.add_resource(Pessoas, '/pessoas')

api.add_resource(Parceiros, '/parceiros')
api.add_resource(ParceiroById, '/parceiros/<int:id>')
api.add_resource(ParceiroByNome,'/parceiros/<nome>')

api.add_resource(Gestores, '/gestores')
api.add_resource(GestorById, '/gestores/<int:id>')
api.add_resource(GestorByNome,'/gestores/<nome>')

api.add_resource(ONGs, '/ongs')
api.add_resource(ONGById, '/ongs/<int:id>')
api.add_resource(ONGByNome,'/ongs/<nome>')
api.add_resource(Animais, '/animais')

api.add_resource(ListarTodos, '/listartodos')

api.add_resource(DeletarOng, '/deletarrong/<int:id>')
api.add_resource(DeletarParceiro, '/deletarparceiro/<int:id>')
api.add_resource(DeletarGestor, '/deletargestor/<int:id>')
api.add_resource(DeletarAnimal, '/deletaranimal/<int:id>')

api.add_resource(AtualizarParceiro, '/atualizarparceiro/<int:id>')
api.add_resource(AtualizarGestor, '/atualizargestor/<int:id>')
api.add_resource(AtualizarAnimal, '/atualizaranimal/<int:id>')
api.add_resource(AtualizarOng, '/atualizarong/<int:id>')

api.add_resource(AdicionarAnimal, '/adicionaranimal')
api.add_resource(AdicionarParceiro, '/adicionarparceiro')
api.add_resource(AdicionarGestor, '/adicionargestor')
api.add_resource(AdicionarONG, '/adicionarong')

api.add_resource(Vacinas, '/vacina')
api.add_resource(AnimalVacina, '/AnimalVacina')

api.add_resource(Agendamentos, '/agendamento')

api.add_resource(RelatoriosDespesas, '/relatorio')
api.add_resource(RelatorioByFiltro, '/relatoriobusca')



# Blueprints para Restful
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)