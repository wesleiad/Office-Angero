"""Gera as associações de arquivo da Office Angerô.

- instalador/assoc/<id>.iss  — registros incluídos pelos instaladores (programa.iss e office.iss)
- docs/ti/AssociacoesPadrao.xml — para a GPO "Definir um arquivo de configuração de associações padrão"

"padrao": o programa vira o padrão da extensão (opção "Usar como programa padrão" do instalador);
"abrir_com": só aparece em "Abrir com" (fotos e vídeos continuam no visualizador/player do Windows).
Uso: python gerar_associacoes.py
"""
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
BARRA = "\\"

PROGRAMAS = {
    "word": {"nome": "Word - Angerô", "exe": "word-angero.exe", "args": "",
             "padrao": {".docx": "Documento do Word", ".docm": "Documento do Word com macros",
                        ".dotx": "Modelo do Word", ".doc": "Documento do Word 97-2003"},
             "abrir_com": [".odt", ".rtf", ".txt", ".md"]},
    "excel": {"nome": "Excel - Angerô", "exe": "excel-angero.exe", "args": "",
              "padrao": {".xlsx": "Planilha do Excel", ".xlsm": "Planilha do Excel com macros",
                         ".xltx": "Modelo do Excel", ".xls": "Planilha do Excel 97-2003"},
              "abrir_com": [".ods", ".csv", ".tsv"]},
    "powerpoint": {"nome": "PowerPoint - Angerô", "exe": "powerpoint-angero.exe", "args": "",
                   "padrao": {".pptx": "Apresentação do PowerPoint", ".pptm": "Apresentação do PowerPoint com macros",
                              ".potx": "Modelo do PowerPoint", ".ppsx": "Apresentação de slides do PowerPoint",
                              ".ppt": "Apresentação do PowerPoint 97-2003"},
                   "abrir_com": [".odp"]},
}


def progid(pid, ext):
    return f"OfficeAngero.{pid}{ext}"


def chave(*partes):
    return BARRA.join(("Software", "Classes") + partes)


def iss(pid, p):
    """Registros do Inno Setup. {#AppPasta_<id>} = pasta do programa (definida por quem inclui o arquivo).
    Se o instalador definir Cmd_<id> antes, ele substitui o comando de abertura."""
    pasta = "{#AppPasta_" + pid + "}"
    # o arquivo vem antes das opções: os programas só abrem o arquivo quando ele é o primeiro argumento
    resto = BARRA + p["exe"] + '"" ""%1""' + ((" " + p["args"]) if p["args"] else "")
    linhas = [f"; gerado por gerar_associacoes.py: {p['nome']}",
              f"#ifndef Cmd_{pid}", f"  #define Cmd_{pid} '\"\"' + AppPasta_{pid} + '{resto}'", "#endif"]
    for ext in list(p["padrao"]) + p["abrir_com"]:
        pg = progid(pid, ext)
        desc = p["padrao"].get(ext, f"Arquivo {ext[1:].upper()}")
        linhas += [
            f'Root: HKCU; Subkey: "{chave(pg)}"; ValueType: string; ValueName: ""; ValueData: "{desc}"; Flags: uninsdeletekey',
            f'Root: HKCU; Subkey: "{chave(pg, "DefaultIcon")}"; ValueType: string; ValueName: ""; ValueData: "{pasta}{BARRA}icone.ico"',
            f'Root: HKCU; Subkey: "{chave(pg, "shell", "open", "command")}"; ValueType: string; ValueName: ""; ValueData: "{{#Cmd_{pid}}}"',
            f'Root: HKCU; Subkey: "{chave(ext, "OpenWithProgids")}"; ValueType: string; ValueName: "{pg}"; ValueData: ""; Flags: uninsdeletevalue',
        ]
        if ext in p["padrao"]:
            linhas.append(f'Root: HKCU; Subkey: "{chave(ext)}"; ValueType: string; ValueName: ""; '
                          f'ValueData: "{pg}"; Flags: uninsdeletevalue; Tasks: associar')
    return "\n".join(linhas) + "\n"


def xml_gpo():
    linhas = ['<?xml version="1.0" encoding="UTF-8"?>',
              "<!-- Office Angerô: associações padrão para a GPO (Configuração do Computador > Modelos Administrativos >",
              "     Componentes do Windows > Explorador de Arquivos > Definir um arquivo de configuração de associações padrão).",
              "     Os ProgIds são registrados pelos instaladores do Office Angerô. Gerado por instalador/gerar_associacoes.py. -->",
              "<DefaultAssociations>"]
    for pid, p in PROGRAMAS.items():
        for ext in p["padrao"]:
            linhas.append(f'  <Association Identifier="{ext}" ProgId="{progid(pid, ext)}" ApplicationName="{p["nome"]}" />')
    linhas.append("</DefaultAssociations>")
    return "\n".join(linhas) + "\n"


def main():
    pasta = AQUI / "assoc"
    pasta.mkdir(exist_ok=True)
    for pid, p in PROGRAMAS.items():
        (pasta / f"{pid}.iss").write_text(iss(pid, p), encoding="utf-8-sig", newline="\r\n")
    ti = RAIZ / "docs" / "ti"
    ti.mkdir(parents=True, exist_ok=True)
    (ti / "AssociacoesPadrao.xml").write_text(xml_gpo(), encoding="utf-8", newline="\r\n")
    print("ok:", ", ".join(PROGRAMAS))


if __name__ == "__main__":
    main()
