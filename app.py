import os
from dotenv import load_dotenv
from flask_restful import Api
from flask import Flask, Blueprint


from helpers.cors import cors
from helpers.database import db, migrate

from resources.pessoa import Pessoas, PessoaById, PessoaByNome
from resources.parceiro import Parceiros, ParceiroById, ParceiroByNome
from resources.gestor import Gestores, GestorById, GestorByNome
from resources.ong import ONGs, ONGByNome, ONGById
from resources.endereco import Enderecos, EnderecosById
from resources.animal import Animais
from resources.listar import ListarTodos
from resources.deletar import DeletarPessoa, DeletarParceiro, DeletarAnimal, DeletarGestor, DeletarOng
from resources.atualizar import AtualizarPessoa, AtualizarParceiro, AtualizarGestor, AtualizarAnimal

load_dotenv()

# create the app
app = Flask(__name__)

# restful
api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix="/api")

postgresUser = os.getenv("POSTGRES_USER")
postgresPassword = os.getenv("POSTGRES_PASSWORD")

DB_URL = f"postgresql://{postgresUser}:{postgresPassword}@localhost:5432/patinhas-alegres"
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# initialize the app with the extension
db.init_app(app)
cors.init_app(app)
migrate.init_app(app, db)

api.add_resource(Pessoas, '/pessoas')
api.add_resource(PessoaById, '/pessoas/<int:id>')
api.add_resource(PessoaByNome,'/pessoas/<nome>')
api.add_resource(Parceiros, '/parceiros')
api.add_resource(ParceiroById, '/parceiros/<int:id>')
api.add_resource(ParceiroByNome,'/parceiros/<nome>')
api.add_resource(Gestores, '/gestores')
api.add_resource(GestorById, '/gestores/<int:id>')
api.add_resource(GestorByNome,'/gestores/<nome>')
api.add_resource(ONGs, '/ongs')
api.add_resource(ONGById, '/ongs/<int:id>')
api.add_resource(ONGByNome,'/ongs/<nome>')
api.add_resource(Enderecos, '/enderecos')
api.add_resource(EnderecosById, '/enderecos/<int:id>')
api.add_resource(Animais, '/animais')
api.add_resource(ListarTodos, '/listartodos')
api.add_resource(DeletarOng, '/deletarrong/<int:id>')
api.add_resource(DeletarPessoa, '/deletarpessoa/<int:id>')
api.add_resource(DeletarParceiro, '/deletarparceiro/<int:id>')
api.add_resource(DeletarGestor, '/deletargestor/<int:id>')
api.add_resource(DeletarAnimal, '/deletaranimal/<int:id>')
api.add_resource(AtualizarPessoa, '/atualizarpessoa/<int:id>')
api.add_resource(AtualizarParceiro, '/atualizarparceiro/<int:id>')
api.add_resource(AtualizarGestor, '/atualizargestor/<int:id>')
api.add_resource(AtualizarAnimal, '/atualizaranimal/<int:id>')





# Blueprints para Restful
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)