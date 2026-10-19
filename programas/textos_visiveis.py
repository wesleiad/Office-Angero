"""Troca o nome antigo do programa (WordCraft/GridCraft/DeckCraft) pelo nome Angerô em TODOS os textos
entre aspas do código Rust: mensagens, títulos, relatórios, ajuda da linha de comando e também as
chaves das traduções e os testes — assim tudo continua batendo (o texto-fonte é a chave da tradução).

Só mexe dentro de literais de string; nomes internos (crates, funções, wordcraft_engine, extensões
de arquivo em minúsculas, variáveis de ambiente em maiúsculas) ficam como estão.

Uso: python textos_visiveis.py <pasta-do-fork> <id>        (depois de rebrand.py e limpar_fork.py)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rebrand import PROGRAMAS  # noqa: E402

LITERAL = re.compile(r'"(?:[^"\\\n]|\\.)*"')


def trocar(raiz: Path, pid: str) -> int:
    cfg = PROGRAMAS[pid]
    # depois de uma quebra de linha escrita no código (\n) o nome também conta
    antigo = re.compile(rf'(?:(?<![\w-])|(?<=\\n)){cfg["orig"]}(?![\w])')
    # dentro dos programas, só o primeiro nome (Word, Excel, PowerPoint); "- Angerô" fica nos atalhos/instalador
    novo = cfg["curto"]
    n = 0
    for p in raiz.rglob("*.rs"):
        if "target" in p.parts or "vendor" in p.parts:
            continue
        s = p.read_text(encoding="utf-8")
        if cfg["orig"] not in s:
            continue

        def literal(m):
            return antigo.sub(novo, m.group(0))

        r = LITERAL.sub(literal, s)
        # "Sobre o Excel - Angerô" fica estranho em português: nas traduções o rebrand já pôs o nome curto
        if r != s:
            p.write_text(r, encoding="utf-8", newline="\n")
            n += 1
    return n


if __name__ == "__main__":
    print("arquivos:", trocar(Path(sys.argv[1]), sys.argv[2]))
