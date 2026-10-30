from conexion.oracle_queries import OracleQueries
from utils import config, console


class SplashScreen:
    def __init__(self):
        self.db = OracleQueries()

    def _total(self, tabela):
        # select count(1) total_{entidade} from {entidade}
        return self.db.scalar(f"select count(1) total_{tabela} from {tabela}")

    def exibir(self):
        console.limpar()
        print(console.azul("""
  ╔══════════════════════════════════════════════════════════╗
  ║                                                          ║
  ║          📦  SISTEMA DE CONTROLE DE ESTOQUE  📦          ║
  ║                                                          ║
  ╚══════════════════════════════════════════════════════════╝"""))
        print(f"\n  Aplicação : {config.NOME_SISTEMA}")
        print(f"  Disciplina: {config.DISCIPLINA}")
        print(f"  Professor : {config.PROFESSOR}")
        print(f"  Semestre  : {config.SEMESTRE}")
        print("  Grupo     : " + ", ".join(config.INTEGRANTES))

        print("\n  Registros nas tabelas:")
        for tabela in ("fornecedores", "produtos"):
            total = self._total(tabela)
            marca = console.verde("com registros") if total else console.amarelo("vazia")
            print(f"    - {tabela:<13}: {total:>4}  ({marca})")
