from sql_alchemy import banco

# Construtor de modelo
class PesoModel(banco.Model):
    __tablename__ = "pesos"
    peso_id = banco.Column(banco.Integer(), primary_key=True)
    data_id = banco.Column(banco.String())
    cpf = banco.Column(banco.String(80), banco.ForeignKey("usuarios.cpf_id"))
    peso = banco.Column(banco.Float(precision=2))
    usuario = banco.relationship("UserModel")
    
    def __init__(self,data_id,cpf,peso,):
        self.data_id = data_id
        self.cpf = cpf
        self.peso = peso
    def json(self):
        return {
            "peso_id": self.peso_id,
            "data_id": self.data_id,
            "cpf": self.cpf,
            "peso": self.peso
        }

    @classmethod
    def find_data(cls,data_id):
        data = cls.query.filter(cls.data_id == data_id).first()
        if data:
            return data
        return None
    
    @classmethod
    def find_cpf(cls,cpf):
        data = cls.query.filter(cls.peso_id == cpf).first()
        if data:
            return data
        return None
    
    
    def save_peso(self):
        banco.session.add(self)
        banco.session.commit()
        
    def update_peso(self,cpf, peso):
        self.cpf = cpf
        self.peso = peso
    
