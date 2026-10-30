"""Acesso ao Oracle usando python-oracledb (sem ORM).

As consultas sao montadas como texto e concatenadas com os atributos,
conforme exige o edital. Textos passam por `lit()` para escapar aspas simples.
"""
import oracledb

from utils import config


def lit(valor):
    """Converte um texto em literal SQL seguro: 'valor' com aspas simples escapadas."""
    if valor is None or valor == "":
        return "NULL"
    return "'" + str(valor).replace("'", "''") + "'"


def num(valor):
    """Converte numero em literal SQL (ponto decimal, independente do locale)."""
    return repr(float(valor)) if isinstance(valor, float) else str(int(valor))


class OracleQueries:
    def __init__(self):
        self.conn = None

    def connect(self):
        if not config.ORACLE_USER or not config.ORACLE_PASSWORD:
            raise RuntimeError(
                "Credenciais do Oracle não configuradas. Copie .env.example para .env e preencha."
            )
        self.conn = oracledb.connect(
            user=config.ORACLE_USER,
            password=config.ORACLE_PASSWORD,
            dsn=config.ORACLE_DSN,
        )
        return self.conn

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def query(self, sql):
        """Executa SELECT e retorna (colunas, linhas)."""
        self.connect()
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            colunas = [d[0].lower() for d in cur.description]
            linhas = cur.fetchall()
            cur.close()
            return colunas, linhas
        finally:
            self.close()

    def scalar(self, sql):
        _, linhas = self.query(sql)
        return linhas[0][0] if linhas else None

    def execute(self, sql):
        """Executa INSERT/UPDATE/DELETE com commit. Retorna linhas afetadas."""
        self.connect()
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            afetadas = cur.rowcount
            self.conn.commit()
            cur.close()
            return afetadas
        except Exception:
            self.conn.rollback()
            raise
        finally:
            self.close()
