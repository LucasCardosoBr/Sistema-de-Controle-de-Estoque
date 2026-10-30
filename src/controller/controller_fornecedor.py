from conexion.oracle_queries import OracleQueries, lit
from model.fornecedor import Fornecedor
from utils import config, console


class ControllerFornecedor:
    def __init__(self):
        self.db = OracleQueries()

    # ---------- consultas auxiliares ----------
    def existe(self, id_fornecedor):
        sql = "select count(1) total from fornecedores where id_fornecedor = " + str(int(id_fornecedor))
        return self.db.scalar(sql) > 0

    def cnpj_existe(self, cnpj, ignorar_id=None):
        sql = "select count(1) total from fornecedores where cnpj = " + lit(cnpj)
        if ignorar_id is not None:
            sql += " and id_fornecedor <> " + str(int(ignorar_id))
        return self.db.scalar(sql) > 0

    def buscar(self, id_fornecedor):
        sql = ("select id_fornecedor, nome, cnpj, telefone, email from fornecedores "
               "where id_fornecedor = " + str(int(id_fornecedor)))
        _, linhas = self.db.query(sql)
        if not linhas:
            return None
        l = linhas[0]
        return Fornecedor(l[0], l[1], l[2], l[3] or "", l[4] or "")

    def listar(self):
        """Mostra a lista (PK + campo descritivo + CNPJ) e devolve os ids validos."""
        cols, linhas = self.db.query(
            "select id_fornecedor, nome, cnpj from fornecedores order by id_fornecedor")
        console.tabela(cols, linhas)
        return {str(l[0]) for l in linhas}

    def _pedir_cnpj(self, atual=None, ignorar_id=None):
        while True:
            cnpj = console.ler_texto("CNPJ (ex.: 12.345.678/0001-90)", atual=atual, max_len=18)
            if self.cnpj_existe(cnpj, ignorar_id):
                console.erro("Já existe um fornecedor com esse CNPJ.")
                atual = None
                continue
            return cnpj

    # ---------- inserir ----------
    def inserir(self):
        console.titulo("INSERIR FORNECEDOR")
        nome = console.ler_texto("Nome", max_len=100)
        cnpj = self._pedir_cnpj()
        telefone = console.ler_texto("Telefone (opcional)", obrigatorio=False, max_len=20)
        email = console.ler_texto("Email (opcional)", obrigatorio=False, max_len=100)

        novo_id = self.db.scalar("select seq_fornecedores.nextval from dual")
        sql = ("insert into fornecedores (id_fornecedor, nome, cnpj, telefone, email) values ("
               + str(novo_id) + ", " + lit(nome) + ", " + lit(cnpj) + ", "
               + lit(telefone) + ", " + lit(email) + ")")
        self.db.execute(sql)
        console.sucesso("Fornecedor inserido:")
        print("  " + self.buscar(novo_id).to_string())

    # ---------- atualizar ----------
    def atualizar(self):
        console.titulo("ATUALIZAR FORNECEDOR")
        ids = self.listar()
        if not ids:
            return
        id_sel = console.ler_opcao(ids | {"0"}, "  ID do fornecedor (0 cancela): ")
        if id_sel == "0":
            return
        forn = self.buscar(id_sel)
        print("  Atual: " + forn.to_string())
        print(config.MENU_ATUALIZAR)
        modo = console.ler_opcao({"0", "1", "2"})
        if modo == "0":
            return

        campos = ["nome", "cnpj", "telefone", "email"]
        if modo == "2":
            print("  Campos: 1-Nome  2-CNPJ  3-Telefone  4-Email")
            campos = [campos[int(console.ler_opcao({"1", "2", "3", "4"})) - 1]]

        for campo in campos:
            if campo == "nome":
                forn.set_nome(console.ler_texto("Nome", atual=forn.get_nome(), max_len=100))
            elif campo == "cnpj":
                forn.set_cnpj(self._pedir_cnpj(forn.get_cnpj(), forn.get_id_fornecedor()))
            elif campo == "telefone":
                forn.set_telefone(console.ler_texto("Telefone", obrigatorio=False,
                                                    atual=forn.get_telefone() or None, max_len=20))
            elif campo == "email":
                forn.set_email(console.ler_texto("Email", obrigatorio=False,
                                                 atual=forn.get_email() or None, max_len=100))

        sql = ("update fornecedores set nome = " + lit(forn.get_nome())
               + ", cnpj = " + lit(forn.get_cnpj())
               + ", telefone = " + lit(forn.get_telefone())
               + ", email = " + lit(forn.get_email())
               + " where id_fornecedor = " + str(int(forn.get_id_fornecedor())))
        self.db.execute(sql)
        console.sucesso("Fornecedor atualizado:")
        print("  " + self.buscar(forn.get_id_fornecedor()).to_string())

    # ---------- excluir ----------
    def excluir(self):
        console.titulo("REMOVER FORNECEDOR")
        ids = self.listar()
        if not ids:
            return
        id_sel = console.ler_opcao(ids | {"0"}, "  ID do fornecedor (0 cancela): ")
        if id_sel == "0":
            return
        forn = self.buscar(id_sel)
        print("  " + forn.to_string())
        if not console.confirmar("Deseja realmente remover este fornecedor?"):
            console.aviso("Remoção cancelada.")
            return

        filhos = self.db.scalar(
            "select count(1) total from produtos where id_fornecedor = " + str(int(id_sel)))
        if filhos > 0:
            console.aviso(f"Este fornecedor possui {filhos} produto(s) vinculado(s).")
            if not console.confirmar("Remover também os produtos vinculados?"):
                console.aviso("Não é possível remover o fornecedor enquanto houver produtos. Cancelado.")
                return
            self.db.execute("delete from produtos where id_fornecedor = " + str(int(id_sel)))
            console.sucesso(f"{filhos} produto(s) removido(s).")

        self.db.execute("delete from fornecedores where id_fornecedor = " + str(int(id_sel)))
        console.sucesso("Fornecedor removido.")
