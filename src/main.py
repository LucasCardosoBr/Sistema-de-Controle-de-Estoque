"""Ponto de entrada: python3 src/main.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller.controller_fornecedor import ControllerFornecedor
from controller.controller_produto import ControllerProduto
from reports.relatorios import Relatorios
from utils import config, console
from utils.splash_screen import SplashScreen

fornecedores = ControllerFornecedor()
produtos = ControllerProduto()
relatorios = Relatorios()


def menu_relatorios():
    while True:
        console.titulo("RELATÓRIOS")
        print(config.MENU_RELATORIOS)
        op = console.ler_opcao({"0", "1", "2", "3"})
        if op == "0":
            return
        {"1": relatorios.quantidade_por_fornecedor,
         "2": relatorios.estoque_baixo,
         "3": relatorios.produtos_fornecedores}[op]()
        console.pausa()


def escolher_entidade(titulo):
    console.titulo(titulo)
    print(config.MENU_ENTIDADES)
    return console.ler_opcao({"0", "1", "2"})


def fluxo_crud(titulo, acao):
    """Repete a acao ate o usuario dizer que nao quer continuar.
    Ao responder "sim", volta ao menu de entidades."""
    while True:
        ent = escolher_entidade(titulo)
        if ent == "0":
            return
        controller = fornecedores if ent == "1" else produtos
        getattr(controller, acao)()
        if not console.confirmar("Deseja realizar outra operação neste menu?"):
            return


def main():
    try:
        SplashScreen().exibir()
    except Exception as e:
        console.erro(f"Não foi possível conectar ao Oracle: {e}")
        console.aviso("Confira o arquivo .env e se as tabelas foram criadas (sql/01_criar_tabelas.sql).")
        sys.exit(1)
    console.pausa()

    while True:
        console.limpar()
        console.titulo(config.NOME_SISTEMA.upper() + " - MENU PRINCIPAL")
        print(config.MENU_PRINCIPAL)
        op = console.ler_opcao({"0", "1", "2", "3", "4"})
        try:
            if op == "1":
                menu_relatorios()
            elif op == "2":
                fluxo_crud("INSERIR REGISTROS", "inserir")
            elif op == "3":
                fluxo_crud("REMOVER REGISTROS", "excluir")
            elif op == "4":
                fluxo_crud("ATUALIZAR REGISTROS", "atualizar")
            elif op == "0":
                console.sucesso("Obrigado por usar o sistema. Até logo!")
                return
        except Exception as e:
            console.erro(f"Erro ao acessar o banco: {e}")
            console.pausa()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n  Encerrado.")
