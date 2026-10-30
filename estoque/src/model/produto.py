from model.fornecedor import Fornecedor


class Produto:
    """Produto associado a um Fornecedor (a associacao e um objeto, nao so o id)."""

    def __init__(self, id_produto=None, nome="", preco_unitario=0.0, quantidade_estoque=0,
                 estoque_minimo=0, quantidade_comprada=0, fornecedor: Fornecedor = None):
        self._id_produto = id_produto
        self._nome = nome
        self._preco_unitario = preco_unitario
        self._quantidade_estoque = quantidade_estoque
        self._estoque_minimo = estoque_minimo
        self._quantidade_comprada = quantidade_comprada
        self._fornecedor = fornecedor

    def get_id_produto(self): return self._id_produto
    def set_id_produto(self, v): self._id_produto = v
    def get_nome(self): return self._nome
    def set_nome(self, v): self._nome = v
    def get_preco_unitario(self): return self._preco_unitario
    def set_preco_unitario(self, v): self._preco_unitario = v
    def get_quantidade_estoque(self): return self._quantidade_estoque
    def set_quantidade_estoque(self, v): self._quantidade_estoque = v
    def get_estoque_minimo(self): return self._estoque_minimo
    def set_estoque_minimo(self, v): self._estoque_minimo = v
    def get_quantidade_comprada(self): return self._quantidade_comprada
    def set_quantidade_comprada(self, v): self._quantidade_comprada = v
    def get_fornecedor(self): return self._fornecedor
    def set_fornecedor(self, v): self._fornecedor = v

    def to_string(self):
        forn = self._fornecedor.get_nome() if self._fornecedor else "-"
        return (
            f"Produto #{self._id_produto} | {self._nome} | R$ {self._preco_unitario:.2f} | "
            f"Estoque: {self._quantidade_estoque} (mín. {self._estoque_minimo}) | "
            f"Comprado: {self._quantidade_comprada} | Fornecedor: {forn}"
        )
