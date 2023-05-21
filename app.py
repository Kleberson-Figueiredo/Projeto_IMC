from flask import Flask, jsonify
from flask_restful import Api
from resources.peso import Pesos, Peso
from resources.usuario import UserRegister, User
from resources.login import UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "OutrosTempos"
app.config["JWT_BLACKLIST_ENABLED"] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({"msg": "Você foi deslogado"}), 401


api.add_resource(Pesos, "/pesos")
api.add_resource(Peso, "/pesos/<string:data_id>")
api.add_resource(User, "/usuarios/<string:cpf_id>")
api.add_resource(UserRegister, "/cadastro/<string:cpf_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")




if __name__ == "__main__":
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)