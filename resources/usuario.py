from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import jwt_required

argumentos = reqparse.RequestParser()
argumentos.add_argument("nome", type=str, required=True, help="O campo 'nome' não pode estar vazio.")
argumentos.add_argument("altura", type=float, required=True, help="O campo 'altura' não pode estar vazio.")
argumentos.add_argument("data_nasc", type=str, required=True, help="O campo 'data_nasc' não pode estar vazio.")
argumentos.add_argument("senha", type=str, required=True, help="O campo 'senha' não pode estar vazio.")

class User(Resource):

    def get(self, cpf_id):
        user = UserModel.find_user(cpf_id)
        if user:
            return user.json()
        return {"msg": "Usuario não encontrado."}, 404 # not found
    
    @jwt_required()  
    def delete(self, cpf_id):
        user = UserModel.find_user(cpf_id)
        if user:
            try:
                user.delete_user()
            except:
                return {"msg": f"Erro ao deletar usuário, contate o admin para mais detalhes"}, 500
            return {"msg": "Usuário deletado"}, 200
        return {"msg": "Usuário não encotrado"},404

class UserRegister(Resource):
    def post(self, cpf_id):
        if UserModel.find_user(cpf_id):
            return {"msg": f"Já existe um usuario com esse cpf {cpf_id}"}, 400
        dados = argumentos.parse_args()
        user = UserModel(cpf_id,**dados)
        try:
            user.save_user()        
        except Exception as e:
            return {"msg": f"Erro de servidor interno = {e}, contate o admin para mais detalhes."}, 500
        return user.json()
    
    @jwt_required()   
    def put(self, cpf_id):
        dados = argumentos.parse_args()
        user_enc = UserModel.find_user(cpf_id)
        if user_enc:
            user_enc.update_user(**dados)
            user_enc.save_user()
            return user_enc.json(), 200 #ok
        user = UserModel(cpf_id,**dados)
        try:
            user.save_user()        
        except:
            return {"msg": "Erro de servidor interno, contate o admin para mais detalhes."}, 500
        return user.json(), 201 # Created