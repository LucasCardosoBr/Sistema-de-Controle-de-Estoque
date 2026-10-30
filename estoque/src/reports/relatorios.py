import os

from conexion.oracle_queries import OracleQueries
from utils import console

PASTA_SQL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql")


class Relatorios:
    def __init__(self):
        self.db = OracleQueries()

    def _ler_sql(self, arquivo):
        with open(os.path.join(PASTA_SQL, arquivo), encoding="utf-8") as f:
            return f.read().strip().rstrip(";")

    def _executar(self, titulo, arquivo):
        console.titulo(titulo)
        colunas, linhas = self.db.query(self._ler_sql(arquivo))
        console.tabela(colunas, linhas)

    def quantidade_por_fornecedor(self):
        self._executar("QUANTIDADE COMPRADA POR FORNECEDOR", "relatorio_quantidade_por_fornecedor.sql")

    def estoque_baixo(self):
        self._executar("PRODUTOS COM ESTOQUE BAIXO", "relatorio_estoque_baixo.sql")

    def produtos_fornecedores(self):
        self._executar("PRODUTOS E SEUS FORNECEDORES", "relatorio_produtos_fornecedores.sql")
