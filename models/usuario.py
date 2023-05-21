from sql_alchemy import banco

# Construtor de modelo
class UserModel(banco.Model):
    __tablename__ = "usuarios"
    
    cpf_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    altura = banco.Column(banco.Float(precision=2))
    data_nasc = banco.Column(banco.String())
    senha = banco.Column(banco.String(40))
    pesos = banco.relationship("PesoModel")
    
    def __init__(self,cpf_id, nome, altura, data_nasc, senha):
        self.cpf_id = cpf_id
        self.nome = nome
        self.altura = altura
        self.data_nasc = data_nasc
        self.senha = senha
        
        
    def json(self):
        return {
            "cpf": self.cpf_id,
            "nome": self.nome,
            "altura": self.altura,
            "data_nasc": self.data_nasc,
            "pesos": [peso.json() for peso in self.pesos]
        }

    @classmethod
    def find_user(cls,cpf_id):
        user = cls.query.filter(cls.cpf_id == cpf_id).first()
        if user:
            return user
        return None
    
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()
        
    def update_user(self, nome, altura, data_nasc, senha):
        self.nome = nome
        self.altura = altura
        self.data_nasc = data_nasc
        self.senha = senha
    
    def delete_user(self):
        [peso.delete_peso() for peso in self.pesos]
        banco.session.delete(self)
        banco.session.commit()