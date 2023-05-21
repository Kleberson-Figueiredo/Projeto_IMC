from flask_restful import Resource, reqparse
from models.peso import PesoModel
from models.usuario import UserModel
from flask_jwt_extended import jwt_required

class Pesos(Resource):
    def get(self):
        return {"Pesos": [pesos.json() for pesos in PesoModel.query.all()]}
    
class Peso(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("cpf", type=str, required=True, help="O campo 'cpf' não pode estar vazio.")
    argumentos.add_argument("peso", type=float, required=True, help="O campo 'peso' não pode estar vazio.")
    
    def get(self, data_id):
        data = PesoModel.find_data(data_id)
        if data:
            return data.json()
        return {"msg": "data not found."}, 404 # not found
    
    @jwt_required()
    def post(self, data_id):
        dados = Peso.argumentos.parse_args()
        if PesoModel.find_data(data_id):
            return{"msg": f"Já existe cadastro para essa data = {data_id}"}
        if UserModel.find_user(dados.cpf):
            data = PesoModel(data_id,**dados)
            try:
                data.save_peso()        
            except:
                return {"msg": "Erro de servidor interno, contate o admin para mais detalhes."}, 500
            return data.json()
        return {"msg": "Não existe Usuário com esse cpf"},404
    
    @jwt_required()  
    def put(self, data_id):
        dados = Peso.argumentos.parse_args()
        data_enc = PesoModel.find_data(data_id)
        if data_enc:
            data_enc.update_peso(**dados)
            data_enc.save_peso()
            return data_enc.json(), 200 #ok
        return {"msg": "Data não entrada"}, 404 # Created
    
    @jwt_required()    
    def delete(self, data_id):
        data = PesoModel.find_data(data_id)
        if data:
            try:
                data.delete_peso()
            except Exception as e:
                return {"msg": f"Erro = {e} ao deletar data, contate o admin para mais detalhes"}, 500
            return {"msg": "Data deletada"}, 200
        return {"msg": "Data não encotrada"},404