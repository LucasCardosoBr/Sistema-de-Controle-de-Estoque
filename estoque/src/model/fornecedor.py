class Fornecedor:
    def __init__(self, id_fornecedor=None, nome="", cnpj="", telefone="", email=""):
        self._id_fornecedor = id_fornecedor
        self._nome = nome
        self._cnpj = cnpj
        self._telefone = telefone
        self._email = email

    def get_id_fornecedor(self): return self._id_fornecedor
    def set_id_fornecedor(self, v): self._id_fornecedor = v
    def get_nome(self): return self._nome
    def set_nome(self, v): self._nome = v
    def get_cnpj(self): return self._cnpj
    def set_cnpj(self, v): self._cnpj = v
    def get_telefone(self): return self._telefone
    def set_telefone(self, v): self._telefone = v
    def get_email(self): return self._email
    def set_email(self, v): self._email = v

    def to_string(self):
        return (
            f"Fornecedor #{self._id_fornecedor} | {self._nome} | CNPJ: {self._cnpj} | "
            f"Tel: {self._telefone or '-'} | Email: {self._email or '-'}"
        )
