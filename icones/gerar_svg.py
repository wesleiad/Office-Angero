"""Gera os ícones do Office Angerô em SVG, nas cores originais de cada programa do Office.

Cada programa: quadrado arredondado com degradê da cor do programa, uma folha clara ao fundo
(com linhas, grade ou slide, conforme o programa) e a letra em traço branco grosso numa etiqueta
mais escura. Office: as três cores em mosaico com a folha da Angerô (README e instaladores).
As letras são traços (não texto), assim não dependem de fonte. Sem filtros.

Saída: icones/svg/<nome>.svg  — depois `gerar_ico.py` converte para PNG/ICO.
"""
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / "svg"

CORES = {  # (clara, escura)
    "word": ("#41a5ee", "#185abd"),
    "excel": ("#33c481", "#107c41"),
    "powerpoint": ("#ff8f6b", "#c43e1c"),
}

LETRA = {
    "word": "M50 98 L64 158 L80 112 L96 158 L110 98",
    "excel": "M56 98 L104 158 M104 98 L56 158",
    "powerpoint": "M62 158 L62 98 L86 98 Q106 98 106 117 Q106 136 86 136 L62 136",
}


def folha(nome, clara, escura):
    """Folha branca à direita, com o "conteúdo" típico de cada programa."""
    base = f'<rect x="112" y="40" width="112" height="176" rx="14" fill="#ffffff" fill-opacity=".95"/>'
    if nome == "word":
        linhas = "".join(f'<rect x="134" y="{y}" width="{w}" height="10" rx="5" fill="{clara}"/>'
                         for y, w in ((70, 70), (96, 70), (122, 70), (148, 70), (174, 46)))
    elif nome == "excel":
        linhas = (f'<g stroke="{clara}" stroke-width="5">'
                  + "".join(f'<line x1="124" y1="{y}" x2="212" y2="{y}"/>' for y in (82, 118, 154, 190))
                  + "".join(f'<line x1="{x}" y1="58" x2="{x}" y2="198"/>' for x in (168,))
                  + "</g>")
    elif nome == "powerpoint":
        linhas = (f'<circle cx="168" cy="110" r="34" fill="{clara}"/>'
                  f'<path d="M168 110 L168 76 A34 34 0 0 1 200 122 Z" fill="{escura}"/>'
                  f'<rect x="134" y="166" width="68" height="10" rx="5" fill="{clara}"/>')
    else:
        linhas = (f'<rect x="130" y="70" width="76" height="40" rx="12" fill="{clara}"/>'
                  f'<rect x="130" y="126" width="60" height="40" rx="12" fill="{clara}" fill-opacity=".6"/>')
    return base + linhas


def programa(nome):
    clara, escura = CORES[nome]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{clara}"/><stop offset="1" stop-color="{escura}"/></linearGradient></defs>
<rect x="8" y="8" width="240" height="240" rx="48" fill="url(#g)"/>
{folha(nome, clara, escura)}
<rect x="28" y="72" width="112" height="112" rx="20" fill="{escura}"/>
<path d="{LETRA[nome]}" fill="none" stroke="#ffffff" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


def office():
    """Iniciador: mosaico das três cores + folha da Angerô em branco."""
    w, x, p = CORES["word"][1], CORES["excel"][1], CORES["powerpoint"][1]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">
<rect x="8" y="8" width="240" height="240" rx="48" fill="#ffffff"/>
<rect x="24" y="24" width="100" height="100" rx="22" fill="{w}"/>
<rect x="132" y="24" width="100" height="100" rx="22" fill="{x}"/>
<rect x="24" y="132" width="100" height="100" rx="22" fill="{p}"/>
<rect x="132" y="132" width="100" height="100" rx="22" fill="#2b3a8f"/>
<g transform="translate(134 157) scale(0.155)">
  <path d="M100 82 C160 40, 240 22, 300 30 C360 38, 400 45, 430 40 C500 45, 560 90, 585 140
           C590 160, 570 170, 540 185 C500 205, 450 215, 410 210 C350 200, 300 150, 250 115
           C200 85, 150 78, 100 82 Z" fill="#ffffff"/>
  <path d="M40 165 C70 120, 140 100, 190 108 C240 115, 280 160, 330 200 C380 238, 450 248, 505 243
           C460 265, 400 290, 330 292 C250 295, 160 290, 120 255 C90 235, 60 200, 40 165 Z" fill="#90d9f5"/>
</g>
</svg>
"""


def main():
    SAIDA.mkdir(exist_ok=True)
    for nome in CORES:
        (SAIDA / f"{nome}.svg").write_text(programa(nome), encoding="utf-8")
    (SAIDA / "office.svg").write_text(office(), encoding="utf-8")
    print("ok:", ", ".join(sorted(p.stem for p in SAIDA.glob("*.svg"))))


if __name__ == "__main__":
    main()
