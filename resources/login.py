from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from hmac import compare_digest
from blacklist import BLACKLIST

argumentos = reqparse.RequestParser()
argumentos.add_argument("cpf_id", type=str, required=True, help="O campo 'cpf' não pode estar vazio.")
argumentos.add_argument("senha", type=str, required=True, help="O campo 'senha' não pode estar vazio.")

class UserLogin(Resource):    
    @classmethod
    def post(cls):
        dados = argumentos.parse_args()
        user = UserModel.find_user(dados["cpf_id"])
        
        if user and compare_digest(user.senha, dados["senha"]):
            token_de_acesso = create_access_token(identity=user.cpf_id)
            return {"access_token": token_de_acesso}, 200
        return {"msg": "cpf ou senha incorreta."}, 401

class UserLogout(Resource):
    
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()["jti"]
        BLACKLIST.add(jwt_id)
        return {"msg": "Logout out successfuly!"}, 200