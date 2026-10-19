"""Lista os textos de interface (em inglês) de um programa sem tradução, para montar a tabela pt-BR.

Uso: python extrair_textos.py <pasta-do-fork> <saida.txt> [<tabela.tsv existente>]
Com a tabela existente, lista só os textos que ainda não têm tradução.
"""
import re
import sys
from pathlib import Path

LITERAL = re.compile(r'"((?:[^"\\\n]|\\.)*)"')
PASTAS = ["crates/ui-egui/src", "apps/deckcraft/src", "crates/engine/src"]


def textos(raiz: Path) -> set[str]:
    achados = set()
    for pasta in PASTAS:
        for p in (raiz / pasta).rglob("*.rs"):
            if "test" in p.name or "tests" in p.parts:
                continue
            s = p.read_text(encoding="utf-8")
            m = re.search(r"#\[cfg\(test\)\]\s*mod\s+\w+\s*\{", s)
            if m:
                s = s[:m.start()]
            for m in LITERAL.finditer(s):
                t = m.group(1)
                if len(t) < 2 or not re.search(r"[A-Za-z]{2}", t):
                    continue
                if not t[0].isupper() and t[0] not in "…(&":
                    continue
                if re.fullmatch(r"[A-Z0-9_$]+", t):  # constantes, variáveis de ambiente
                    continue
                if "{" in t or "::" in t or ("/" in t and " " not in t):
                    continue
                if re.fullmatch(r"[A-Z][a-z]+[A-Z]\w*", t):  # CamelCase (ids)
                    continue
                achados.add(t)
    return achados


def main():
    raiz, saida = Path(sys.argv[1]), Path(sys.argv[2])
    feitos = set()
    if len(sys.argv) > 3 and Path(sys.argv[3]).exists():
        for linha in Path(sys.argv[3]).read_text(encoding="utf-8").splitlines():
            if "\t" in linha and not linha.startswith("#"):
                feitos.add(linha.split("\t")[0])
    lista = sorted(textos(raiz) - feitos)
    saida.write_text("\n".join(lista) + "\n", encoding="utf-8")
    print(len(lista), "textos")


if __name__ == "__main__":
    main()
