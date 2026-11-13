' despachar-agendado.vbs - o que o Agendador do Windows chama (tarefa "Continuum - despachante").
' Roda uma rodada do despachar.py sem abrir janela, com o Python direto (nunca o `py` da Store:
' cada chamada aciona o AppXSvc e vaza memoria). Saida acrescentada em %LOCALAPPDATA%\Continuum\despachante.log,
' fora do repo; o registro de cada rodada continua em tarefas/log/RODADA-*.md.
' Parar tudo: criar o arquivo tarefas/PAUSA. Desligar: schtasks /Change /TN "Continuum - despachante" /DISABLE
Option Explicit
Dim fso, sh, pasta, raiz, py, logdir, cmd
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
pasta = fso.GetParentFolderName(WScript.ScriptFullName)
raiz = fso.GetParentFolderName(fso.GetParentFolderName(pasta))
py = sh.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Python\bin\python.exe"
logdir = sh.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Continuum"
If Not fso.FolderExists(logdir) Then fso.CreateFolder logdir
sh.CurrentDirectory = raiz
cmd = "cmd /c ""echo ==== %DATE% %TIME% >> """ & logdir & "\despachante.log"" & """ & py & """ -X utf8 """ & pasta & "\despachar.py"" >> """ & logdir & "\despachante.log"" 2>&1"""
sh.Run cmd, 0, True
