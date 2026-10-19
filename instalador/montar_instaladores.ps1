# Monta os instaladores do Office Angerô a partir dos programas compilados nesta máquina.
# Saída padrão: Área de Trabalho\Instaladores Office Angerô
#   Instalar <Programa> - Angerô.exe    (um por programa)
# Uso: powershell -ExecutionPolicy Bypass -File montar_instaladores.ps1
# Versão = a do Cargo.toml de cada programa + ".0": as do GitHub (".<compilação>") são sempre maiores,
# então os programas instalados por aqui se atualizam sozinhos na primeira versão publicada.
param(
    [string]$Src = "$env:LOCALAPPDATA\OfficeAngero\src",
    [string]$Saida = (Join-Path ([Environment]::GetFolderPath('Desktop')) 'Instaladores Office Angerô')
)
$ErrorActionPreference = 'Stop'
$Raiz = Split-Path $PSScriptRoot -Parent
$Build = "$env:LOCALAPPDATA\OfficeAngero\build"
$Iscc = @("$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe", "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe") |
    Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $Iscc) { throw "Inno Setup 6 não encontrado (winget install JRSoftware.InnoSetup)" }

$Programas = @(
    @{ Id = 'word';       Nome = 'Word - Angerô';       Exe = 'word-angero';       Icone = 'word';       Pasta = 'word-angero';       Args = '' },
    @{ Id = 'excel';      Nome = 'Excel - Angerô';      Exe = 'excel-angero';      Icone = 'excel';      Pasta = 'excel-angero';      Args = '' },
    @{ Id = 'powerpoint'; Nome = 'PowerPoint - Angerô'; Exe = 'powerpoint-angero'; Icone = 'powerpoint'; Pasta = 'powerpoint-angero'; Args = '' }
)

New-Item -ItemType Directory -Force $Saida | Out-Null
$Prog = Join-Path $Build 'programas'
Remove-Item $Prog -Recurse -Force -ErrorAction SilentlyContinue

foreach ($p in $Programas) {
    $base = (Select-String -Path (Join-Path $Src "$($p.Pasta)\Cargo.toml") -Pattern '^version\s*=\s*"([^"]+)"' | Select-Object -First 1).Matches[0].Groups[1].Value
    $Versao = "$base.0"
    $rel = Join-Path $Src "$($p.Pasta)\target\release"
    $dest = Join-Path $Prog $p.Id
    New-Item -ItemType Directory -Force $dest | Out-Null
    foreach ($f in @("$($p.Exe).exe")) {  # o -cli.exe (linha de comando) não vai para os usuários
        if (-not (Test-Path "$rel\$f")) { throw "$($p.Nome): falta $rel\$f (compile antes: programas\compilar.sh)" }
        Copy-Item "$rel\$f" $dest
    }
    Copy-Item (Join-Path $Src "$($p.Pasta)\LICENSE-APACHE"), (Join-Path $Src "$($p.Pasta)\LICENSE-MIT"), (Join-Path $Src "$($p.Pasta)\NOTICE") $dest
    Set-Content -Path "$dest\versao.txt" -Value $Versao -NoNewline -Encoding ascii
    Write-Host "==> instalador avulso: $($p.Nome)"
    & $Iscc /Q "/DId=$($p.Id)" "/DNome=$($p.Nome)" "/DExe=$($p.Exe)" "/DIcone=$($p.Icone)" "/DArgs=$($p.Args)" `
        "/DVersao=$Versao" "/DFonte=$dest" "/DIcones=$Raiz\icones\ico" "/DSaida=$Saida" "$PSScriptRoot\programa.iss"
    if ($LASTEXITCODE -ne 0) { throw "ISCC falhou: $($p.Nome)" }
}

Get-ChildItem $Saida -Filter *.exe | Select-Object Name, @{n = 'MB'; e = { [math]::Round($_.Length / 1MB, 1) } } | Format-Table -AutoSize
