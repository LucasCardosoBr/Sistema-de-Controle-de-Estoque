"""Configuracoes da aplicacao: conexao com o Oracle e textos dos menus."""
import os

NOME_SISTEMA = "Sistema de Controle de Estoque"
INTEGRANTES = ["Lucas Cardoso"]
PROFESSOR = "Howard Roatti"
DISCIPLINA = "Banco de Dados"
SEMESTRE = "2026/2"


def _carregar_env():
    """Le o arquivo .env da raiz do projeto (se existir), sem dependencias extras."""
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    caminho = os.path.join(raiz, ".env")
    if not os.path.exists(caminho):
        return
    with open(caminho, encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            chave, valor = linha.split("=", 1)
            os.environ.setdefault(chave.strip(), valor.strip().strip('"').strip("'"))


_carregar_env()

ORACLE_USER = os.environ.get("ORACLE_USER", "")
ORACLE_PASSWORD = os.environ.get("ORACLE_PASSWORD", "")
ORACLE_DSN = os.environ.get("ORACLE_DSN", "localhost:1521/XEPDB1")

MENU_PRINCIPAL = """
  1 - Relatórios
  2 - Inserir registros
  3 - Remover registros
  4 - Atualizar registros
  0 - Sair
"""

MENU_ENTIDADES = """
  1 - Fornecedores
  2 - Produtos
  0 - Voltar ao menu principal
"""

MENU_RELATORIOS = """
  1 - Quantidade comprada e valor por fornecedor (sumarização)
  2 - Produtos com estoque baixo (junção)
  3 - Lista de produtos com seus fornecedores (junção)
  0 - Voltar ao menu principal
"""

MENU_ATUALIZAR = """
  1 - Informar todos os campos (Enter mantém o valor atual)
  2 - Escolher um único campo
  0 - Cancelar
"""
