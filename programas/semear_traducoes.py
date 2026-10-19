"""Monta a tabela pt-BR do PowerPoint aproveitando as traduções que o Word (pt-br.tsv) e o Excel (pt.rs)
já têm: todo texto do PowerPoint que for idêntico a um texto traduzido lá entra na tabela.

Uso: python semear_traducoes.py <textos.txt> <word pt-br.tsv> <excel pt.rs> <saída.tsv>
Saída: linhas "inglês<TAB>português"; textos sem par ficam de fora (para traduzir à mão).
"""
import re
import sys
from pathlib import Path


def tabela_word(p: Path) -> dict:
    t = {}
    for linha in p.read_text(encoding="utf-8").splitlines():
        if linha.startswith("#"):
            continue
        col = linha.split("\t")
        if len(col) >= 3 and col[1] and col[2]:
            t.setdefault(col[1], col[2])
    return t


def tabela_excel(p: Path) -> dict:
    t = {}
    par = re.compile(r'^\s*"((?:[^"\\]|\\.)*)"\s*=>\s*"((?:[^"\\]|\\.)*)",', re.M)
    for m in par.finditer(p.read_text(encoding="utf-8")):
        t.setdefault(m.group(1), m.group(2))
    return t


def main():
    textos, word, excel, saida = (Path(a) for a in sys.argv[1:5])
    fontes = [tabela_word(word), tabela_excel(excel)]
    pares = {}
    for t in textos.read_text(encoding="utf-8").splitlines():
        for f in fontes:
            if t in f and f[t] != t:
                pares[t] = f[t]
                break
    saida.write_text("".join(f"{a}\t{b}\n" for a, b in sorted(pares.items())), encoding="utf-8")
    print(len(pares), "traduções aproveitadas")


if __name__ == "__main__":
    main()
