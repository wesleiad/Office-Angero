; Instalador avulso de um programa do Office Angerô (Inno Setup 6).
; Compilado por montar_instaladores.ps1 (ou pelo GitHub Actions) com:
;   ISCC /DId=word /DNome="Word - Angerô" /DExe=word-angero /DIcone=word
;        /DVersao=1.0.0.1 /DFonte=<pasta com os .exe> /DIcones=<pasta icones\ico> /DSaida=<pasta> programa.iss
; Instala por usuário (sem senha de administrador): o programa se atualiza sozinho trocando os próprios arquivos.

#ifndef Args
  #define Args ""
#endif

; pasta usada pelas associações de arquivo (assoc\<id>.iss)
#define AppPasta_word "{app}"
#define AppPasta_excel "{app}"
#define AppPasta_powerpoint "{app}"

[Setup]
AppId={{Office-Angero-{#Id}}
AppName={#Nome}
AppVersion={#Versao}
AppVerName={#Nome} {#Versao}
AppPublisher=Grupo Angerô
AppPublisherURL=https://github.com/wesleiad/Office-Angero
AppSupportURL=https://github.com/wesleiad/Office-Angero/blob/main/docs/ajuda/{#Id}.md
DefaultDirName={localappdata}\Programs\Office Angero\{#Nome}
DefaultGroupName=Office Angerô
DisableProgramGroupPage=yes
DisableDirPage=yes
PrivilegesRequired=lowest
OutputDir={#Saida}
OutputBaseFilename=Instalar {#Nome}
SetupIconFile={#Icones}\{#Icone}.ico
UninstallDisplayIcon={app}\{#Exe}.exe
UninstallDisplayName={#Nome}
WizardStyle=modern
Compression=lzma2/max
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes
ChangesAssociations=yes
VersionInfoCompany=Grupo Angerô
VersionInfoProductName={#Nome}
VersionInfoVersion={#Versao}

[Languages]
Name: "pt"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
; desmarcado: em computadores com o Microsoft Office, os arquivos continuam abrindo nele
Name: "associar"; Description: "Usar o {#Nome} como programa padrão para os arquivos dele"; GroupDescription: "Arquivos:"; Flags: unchecked
Name: "atalho"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Atalhos:"

[Files]
Source: "{#Fonte}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; dicionário de português (LibreOffice/VERO, LGPLv3/MPL) para a correção ortográfica do Word e do PowerPoint
Source: "{#SourcePath}..\dicionarios\*"; DestDir: "{localappdata}\hunspell"; Flags: ignoreversion uninsneveruninstall
Source: "{#Icones}\{#Icone}.ico"; DestDir: "{app}"; DestName: "icone.ico"; Flags: ignoreversion

[Icons]
Name: "{group}\{#Nome}"; Filename: "{app}\{#Exe}.exe"; Parameters: "{#Args}"; IconFilename: "{app}\icone.ico"
Name: "{userdesktop}\{#Nome}"; Filename: "{app}\{#Exe}.exe"; Parameters: "{#Args}"; IconFilename: "{app}\icone.ico"; Tasks: atalho

[Registry]
; inventário para o TI: onde está e qual versão foi instalada
Root: HKCU; Subkey: "Software\Grupo Angero\Office Angero\Programas\{#Id}"; ValueType: string; ValueName: "Pasta"; ValueData: "{app}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Grupo Angero\Office Angero\Programas\{#Id}"; ValueType: string; ValueName: "Versao"; ValueData: "{#Versao}"

[UninstallDelete]
; restos da atualização automática (arquivos trocados com o programa aberto)
Type: files; Name: "{app}\*.old"
Type: files; Name: "{app}\*.novo"

#include AddBackslash(SourcePath) + "assoc\" + Id + ".iss"

[Run]
Filename: "{app}\{#Exe}.exe"; Parameters: "{#Args}"; Description: "Abrir o {#Nome}"; Flags: nowait postinstall skipifsilent
