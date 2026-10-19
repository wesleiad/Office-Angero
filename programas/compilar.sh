#!/usr/bin/env bash
# Compila os programas do Office Angerô (forks do ArtCraft) nesta máquina.
# Uso: bash compilar.sh [word excel powerpoint]   (sem argumentos: todos)
# Requer: Rust (MSVC), Visual Studio Build Tools (C++), e os forks em $SRC.
# JOBS=2 por padrão: com mais núcleos compilando ao mesmo tempo falta memória em PCs de 16 GB.
set -u
SRC="${SRC:-$LOCALAPPDATA/OfficeAngero/src}"
LOG="${LOG:-$LOCALAPPDATA/OfficeAngero/logs}"
mkdir -p "$LOG"
export PATH="$USERPROFILE/.cargo/bin:$PATH"
export CARGO_HTTP_CHECK_REVOKE=false          # proxies corporativos com inspeção HTTPS costumam bloquear a checagem de revogação
# Sem CRAFT_FONTS_DIR de propósito: as fontes extras do ArtCraft são só japonês/chinês/árabe/tailandês (40 MB);
# sem elas o .exe fica menor e gasta menos memória em computadores antigos. Textos latinos usam as fontes do Windows.
unset CRAFT_FONTS_DIR

declare -A PASTA=( [word]=word-angero [excel]=excel-angero [powerpoint]=powerpoint-angero )
declare -A PACOTE=( [word]=wordcraft [excel]=gridcraft [powerpoint]=deckcraft )

alvos=("$@")
[ ${#alvos[@]} -eq 0 ] && alvos=(word excel powerpoint)
for id in "${alvos[@]}"; do
  p=${PACOTE[$id]}
  echo "[$(date +%H:%M:%S)] compilando $id ($p)"
  ( cd "$SRC/${PASTA[$id]}" && cargo build --release -j "${JOBS:-2}" -p "$p" ) > "$LOG/build_$id.log" 2>&1
  r=$?
  echo "[$(date +%H:%M:%S)] $id: $([ $r -eq 0 ] && echo OK || echo "FALHOU (veja $LOG/build_$id.log)")"
done
