$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\🚀 Start Fusion 360 Remote Server.lnk")
$Shortcut.TargetPath = "cmd.exe"
$Shortcut.Arguments = "/c `"cd /d `"$PWD`" && start-server-now.bat`""
$Shortcut.WorkingDirectory = "$PWD"
$Shortcut.IconLocation = "shell32.dll,277"
$Shortcut.Description = "Start Fusion 360 Remote Control Server"
$Shortcut.Save()

Write-Host "✅ Desktop shortcut created!"
Write-Host "📱 Double-click '🚀 Start Fusion 360 Remote Server' on Desktop to start"
