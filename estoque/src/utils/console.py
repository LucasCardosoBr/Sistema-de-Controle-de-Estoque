"""Funcoes de interface de console: cores, tabelas, leitura validada."""
import os
import sys
from decimal import Decimal

_COR = sys.stdout.isatty()


def _c(codigo, texto):
    return f"\033[{codigo}m{texto}\033[0m" if _COR else texto


def azul(t): return _c("1;36", t)
def verde(t): return _c("1;32", t)
def vermelho(t): return _c("1;31", t)
def amarelo(t): return _c("1;33", t)


def limpar():
    os.system("cls" if os.name == "nt" else "clear")


def titulo(texto):
    linha = "=" * 64
    print(f"\n{azul(linha)}\n{azul(texto.center(64))}\n{azul(linha)}")


def sucesso(msg): print(verde(f"  ✔ {msg}"))
def erro(msg): print(vermelho(f"  ✘ {msg}"))
def aviso(msg): print(amarelo(f"  ! {msg}"))


def pausa():
    input("\n  Pressione Enter para continuar...")


def _fmt(valor):
    if valor is None:
        return "-"
    if isinstance(valor, (float, Decimal)):
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return str(valor)


def tabela(colunas, linhas):
    """Imprime uma tabela alinhada. Retorna sem erro se nao houver linhas."""
    if not linhas:
        aviso("Nenhum registro encontrado.")
        return
    cab = [str(c).replace("_", " ").upper() for c in colunas]
    dados = [[_fmt(v) for v in linha] for linha in linhas]
    larg = [max(len(cab[i]), *(len(l[i]) for l in dados)) for i in range(len(cab))]
    sep = "+-" + "-+-".join("-" * w for w in larg) + "-+"
    print(sep)
    print("| " + " | ".join(azul(cab[i].ljust(larg[i])) if _COR else cab[i].ljust(larg[i]) for i in range(len(cab))) + " |")
    print(sep)
    for l in dados:
        print("| " + " | ".join(l[i].ljust(larg[i]) for i in range(len(l))) + " |")
    print(sep)
    print(f"  {len(dados)} registro(s)")


def ler_opcao(validas, prompt="  Escolha uma opção: "):
    while True:
        op = input(prompt).strip()
        if op in validas:
            return op
        erro("Opção inválida. Tente novamente.")


def ler_texto(rotulo, obrigatorio=True, atual=None, max_len=None):
    """Le texto. Se `atual` for informado, Enter mantem o valor atual."""
    while True:
        dica = f" [{atual}]" if atual is not None else ""
        valor = input(f"  {rotulo}{dica}: ").strip()
        if not valor:
            if atual is not None:
                return atual
            if not obrigatorio:
                return ""
            erro("Campo obrigatório.")
            continue
        if max_len and len(valor) > max_len:
            erro(f"Máximo de {max_len} caracteres.")
            continue
        return valor


def ler_inteiro(rotulo, minimo=0, atual=None):
    while True:
        dica = f" [{atual}]" if atual is not None else ""
        bruto = input(f"  {rotulo}{dica}: ").strip()
        if not bruto and atual is not None:
            return int(atual)
        try:
            n = int(bruto)
        except ValueError:
            erro("Digite um número inteiro.")
            continue
        if n < minimo:
            erro(f"O valor deve ser >= {minimo}.")
            continue
        return n


def ler_decimal(rotulo, minimo=0, atual=None):
    while True:
        dica = f" [{atual}]" if atual is not None else ""
        bruto = input(f"  {rotulo}{dica}: ").strip().replace(",", ".")
        if not bruto and atual is not None:
            return float(atual)
        try:
            n = float(bruto)
        except ValueError:
            erro("Digite um número válido (ex.: 12,50).")
            continue
        if n < minimo:
            erro(f"O valor deve ser >= {minimo}.")
            continue
        return round(n, 2)


def confirmar(pergunta):
    resp = ler_opcao({"s", "n", "S", "N"}, f"  {pergunta} (s/n): ")
    return resp.lower() == "s"
