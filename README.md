# Office Angerô

Programas de escritório gratuitos do **Grupo Angerô**: texto, planilha e apresentação. Cada um é um programa
separado, com o próprio instalador, que se atualiza sozinho e é leve o bastante para computadores antigos.

| Programa | Para quê | Ajuda |
|---|---|---|
| **Word - Angerô** | Textos, ofícios, relatórios e mala direta; abre e salva .docx | [docs/ajuda/word.md](docs/ajuda/word.md) |
| **Excel - Angerô** | Planilhas, fórmulas, gráficos, filtros e tabelas dinâmicas; abre e salva .xlsx | [docs/ajuda/excel.md](docs/ajuda/excel.md) |
| **PowerPoint - Angerô** | Apresentações de slides; abre e salva .pptx | [docs/ajuda/powerpoint.md](docs/ajuda/powerpoint.md) |

## Instalar

Na aba **Releases** do repositório de cada programa há o **Instalar <Programa> - Angerô.exe**:

| Programa | Repositório |
|---|---|
| Word - Angerô | [word-angero](https://github.com/wesleiad/word-angero) |
| Excel - Angerô | [excel-angero](https://github.com/wesleiad/excel-angero) |
| PowerPoint - Angerô | [powerpoint-angero](https://github.com/wesleiad/powerpoint-angero) |

Os instaladores não pedem senha de administrador (instalam por usuário). A opção "usar como programa padrão"
vem desmarcada: em computadores que já têm o Microsoft Office, os arquivos continuam abrindo nele, e o
programa da Angerô aparece em "Abrir com" (ver `docs/ti/associacoes.md`).

## Atualização automática

1. Alteração no código do programa → `git push` no ramo `angero` do repositório dele.
2. O GitHub Actions compila e publica uma versão nova em **Releases** (`versao.txt` + `.zip` + instalador).
3. Cada programa instalado confere o GitHub ao abrir e a cada 6 horas; se houver versão nova, baixa e troca os
   próprios arquivos em segundo plano — vale na próxima vez que for aberto. Não precisa de administrador.
   (`programas/atualizacao.rs`, copiado para cada programa; `OFFICE_ANGERO_SEM_ATUALIZACAO=1` desliga.)

## Computadores antigos

- Sem as fontes extras do ArtCraft (japonês/chinês/árabe/tailandês): executáveis ~40 MB menores e menos memória.
- PowerPoint: modo leve automático com até 6 GB de RAM (caches de imagem e desfazer com um quarto do tamanho);
  `POWERPOINT_ANGERO_MEMORIA=baixa|normal` força.
- Vídeo: DirectX 12 e, sem ele (Intel antigas), OpenGL; `WGPU_BACKEND=gl` força o OpenGL.

## Estrutura

```
programas/    rebrand.py, limpar_fork.py, textos_visiveis.py — aplicam a identidade Angerô nos forks;
              extrair_textos.py e semear_traducoes.py — tabela pt-BR do PowerPoint; atualizacao.rs; compilar.sh
icones/       ícones (gerar_svg.py desenha, gerar_ico.py gera PNG/ICO)
instalador/   instalador Inno Setup de cada programa (programa.iss), associações de arquivo e o modelo do
              GitHub Actions dos forks (workflow-programa.yml → preencher_workflows.py)
dicionarios/  dicionário pt_BR (Hunspell) instalado em %LOCALAPPDATA%\hunspell para o Word e o PowerPoint
docs/         ajuda dos programas e notas para o TI
```

## Código-base e licença

Desenvolvido por **Weslei Domingues (TI)** para o Grupo Angerô. © 2026 Weslei Domingues (ícones em `icones/`).

Os três programas foram construídos a partir do código aberto do projeto **ArtCraft**
(WordCraft, GridCraft e DeckCraft — https://github.com/storytold), usado como base, sob licença
MIT OU Apache-2.0; os avisos de licença originais estão em cada repositório.
Correção ortográfica em português: dicionário pt_BR do projeto VERO/LibreOffice (`dicionarios/`, LGPLv3 ou MPL).
Word, Excel e PowerPoint são marcas da Microsoft; o Office Angerô não tem relação com a Microsoft.
O código deste repositório está sob a licença MIT (arquivo `LICENSE`).
