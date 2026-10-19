# Programas padrão para cada tipo de arquivo

Os instaladores têm a opção **"Usar como programa padrão"**, que vem **desmarcada** (para não tirar os arquivos
do Microsoft Office onde ele existe). Sem ela, os programas aparecem só em "Abrir com". Marcada, registra:

| Programa | Vira o padrão de | Só aparece em "Abrir com" |
|---|---|---|
| Word - Angerô | .docx .docm .dotx .doc | .odt .rtf .txt .md |
| Excel - Angerô | .xlsx .xlsm .xltx .xls | .ods .csv .tsv |
| PowerPoint - Angerô | .pptx .pptm .potx .ppsx .ppt | .odp |

Limite do Windows 10/11: se o usuário já tinha escolhido "sempre abrir com" outro programa para uma extensão,
o Windows mantém a escolha dele. Para **forçar nos computadores sem Microsoft Office**:

1. Copie `docs/ti/AssociacoesPadrao.xml` para um compartilhamento que todos leem (ex.: `\servidor\NETLOGON\OfficeAngero\`).
2. GPO (filtrada para esses computadores) › Configuração do Computador › Modelos Administrativos › Componentes do Windows ›
   Explorador de Arquivos › **Definir um arquivo de configuração de associações padrão** › Habilitado › caminho do XML.
3. Vale no próximo logon (o Office Angerô precisa estar instalado).

O XML é gerado por `instalador/gerar_associacoes.py` (mesma lista dos instaladores).
