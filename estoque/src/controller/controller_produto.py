from conexion.oracle_queries import OracleQueries, lit, num
from controller.controller_fornecedor import ControllerFornecedor
from model.produto import Produto
from utils import config, console


class ControllerProduto:
    def __init__(self):
        self.db = OracleQueries()
        self.ctrl_fornecedor = ControllerFornecedor()

    # ---------- consultas auxiliares ----------
    def buscar(self, id_produto):
        sql = ("select id_produto, nome, preco_unitario, quantidade_estoque, estoque_minimo, "
               "quantidade_comprada, id_fornecedor from produtos "
               "where id_produto = " + str(int(id_produto)))
        _, linhas = self.db.query(sql)
        if not linhas:
            return None
        l = linhas[0]
        fornecedor = self.ctrl_fornecedor.buscar(l[6])
        return Produto(l[0], l[1], float(l[2]), l[3], l[4], l[5], fornecedor)

    def listar(self):
        cols, linhas = self.db.query(
            "select p.id_produto, p.nome, p.quantidade_estoque, f.nome fornecedor "
            "from produtos p inner join fornecedores f on f.id_fornecedor = p.id_fornecedor "
            "order by p.id_produto")
        console.tabela(cols, linhas)
        return {str(l[0]) for l in linhas}

    def _escolher_fornecedor(self, atual=None):
        """Lista fornecedores e retorna o objeto escolhido (None se nao houver nenhum)."""
        ids = self.ctrl_fornecedor.listar()
        if not ids:
            console.erro("Cadastre um fornecedor antes de cadastrar produtos.")
            return None
        if atual is not None:
            id_sel = console.ler_opcao(ids | {""}, f"  ID do fornecedor [{atual}]: ")
            id_sel = id_sel or str(atual)
        else:
            id_sel = console.ler_opcao(ids, "  ID do fornecedor: ")
        return self.ctrl_fornecedor.buscar(id_sel)

    # ---------- inserir ----------
    def inserir(self):
        console.titulo("INSERIR PRODUTO")
        fornecedor = self._escolher_fornecedor()
        if fornecedor is None:
            return
        nome = console.ler_texto("Nome do produto", max_len=100)
        preco = console.ler_decimal("Preço unitário (R$)")
        estoque = console.ler_inteiro("Quantidade em estoque")
        minimo = console.ler_inteiro("Estoque mínimo")
        comprada = console.ler_inteiro("Quantidade comprada (total)")

        novo_id = self.db.scalar("select seq_produtos.nextval from dual")
        sql = ("insert into produtos (id_produto, nome, preco_unitario, quantidade_estoque, "
               "estoque_minimo, quantidade_comprada, id_fornecedor) values ("
               + str(novo_id) + ", " + lit(nome) + ", " + num(preco) + ", " + num(estoque) + ", "
               + num(minimo) + ", " + num(comprada) + ", "
               + str(int(fornecedor.get_id_fornecedor())) + ")")
        self.db.execute(sql)
        console.sucesso("Produto inserido:")
        print("  " + self.buscar(novo_id).to_string())

    # ---------- atualizar ----------
    def atualizar(self):
        console.titulo("ATUALIZAR PRODUTO")
        ids = self.listar()
        if not ids:
            return
        id_sel = console.ler_opcao(ids | {"0"}, "  ID do produto (0 cancela): ")
        if id_sel == "0":
            return
        prod = self.buscar(id_sel)
        print("  Atual: " + prod.to_string())
        print(config.MENU_ATUALIZAR)
        modo = console.ler_opcao({"0", "1", "2"})
        if modo == "0":
            return

        campos = ["nome", "preco", "estoque", "minimo", "comprada", "fornecedor"]
        if modo == "2":
            print("  Campos: 1-Nome  2-Preço  3-Estoque  4-Estoque mínimo  5-Qtd comprada  6-Fornecedor")
            campos = [campos[int(console.ler_opcao({"1", "2", "3", "4", "5", "6"})) - 1]]

        for campo in campos:
            if campo == "nome":
                prod.set_nome(console.ler_texto("Nome", atual=prod.get_nome(), max_len=100))
            elif campo == "preco":
                prod.set_preco_unitario(console.ler_decimal("Preço unitário", atual=prod.get_preco_unitario()))
            elif campo == "estoque":
                prod.set_quantidade_estoque(console.ler_inteiro("Quantidade em estoque", atual=prod.get_quantidade_estoque()))
            elif campo == "minimo":
                prod.set_estoque_minimo(console.ler_inteiro("Estoque mínimo", atual=prod.get_estoque_minimo()))
            elif campo == "comprada":
                prod.set_quantidade_comprada(console.ler_inteiro("Quantidade comprada", atual=prod.get_quantidade_comprada()))
            elif campo == "fornecedor":
                novo = self._escolher_fornecedor(prod.get_fornecedor().get_id_fornecedor())
                if novo is not None:
                    prod.set_fornecedor(novo)

        sql = ("update produtos set nome = " + lit(prod.get_nome())
               + ", preco_unitario = " + num(prod.get_preco_unitario())
               + ", quantidade_estoque = " + num(prod.get_quantidade_estoque())
               + ", estoque_minimo = " + num(prod.get_estoque_minimo())
               + ", quantidade_comprada = " + num(prod.get_quantidade_comprada())
               + ", id_fornecedor = " + str(int(prod.get_fornecedor().get_id_fornecedor()))
               + " where id_produto = " + str(int(prod.get_id_produto())))
        self.db.execute(sql)
        console.sucesso("Produto atualizado:")
        print("  " + self.buscar(prod.get_id_produto()).to_string())

    # ---------- excluir ----------
    def excluir(self):
        console.titulo("REMOVER PRODUTO")
        ids = self.listar()
        if not ids:
            return
        id_sel = console.ler_opcao(ids | {"0"}, "  ID do produto (0 cancela): ")
        if id_sel == "0":
            return
        print("  " + self.buscar(id_sel).to_string())
        if not console.confirmar("Deseja realmente remover este produto?"):
            console.aviso("Remoção cancelada.")
            return
        # PRODUTOS nao e referenciada por nenhuma outra tabela (nao tem tabela filha).
        self.db.execute("delete from produtos where id_produto = " + str(int(id_sel)))
        console.sucesso("Produto removido.")
