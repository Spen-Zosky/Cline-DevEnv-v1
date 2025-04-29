# Script PowerShell Avanzato - Commit e Push automatico su GitHub
Write-Host "=== Git Commit & Push Automation (Advanced) ===" -ForegroundColor Cyan

# Naviga nella directory del progetto
Set-Location "D:\Cline"

# Verifica se esistono modifiche da committare
Write-Host "Controllo modifiche in corso..." -ForegroundColor Yellow
$changes = git status --porcelain

if (-not $changes) {
    Write-Host "Nessuna modifica rilevata. Nessuna azione necessaria." -ForegroundColor Green
    exit
}

# Mostra i file modificati
Write-Host "Modifiche rilevate:" -ForegroundColor Yellow
git status -s

# Chiede il messaggio del commit
$message = Read-Host "Inserisci il messaggio per il commit"

# Controlla che il messaggio non sia vuoto
if ([string]::IsNullOrWhiteSpace($message)) {
    Write-Host "Errore: il messaggio del commit non può essere vuoto." -ForegroundColor Red
    exit
}

try {
    # Esegue git add
    Write-Host "Aggiunta dei file modificati..." -ForegroundColor Yellow
    git add .

    # Esegue git commit
    Write-Host "Creazione del commit..." -ForegroundColor Yellow
    git commit -m "$message"

    # Esegue git push
    Write-Host "Invio dei cambiamenti su GitHub..." -ForegroundColor Yellow
    git push origin main

    Write-Host "Operazione completata con successo." -ForegroundColor Green
}
catch {
    Write-Host "Errore durante il processo Git:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
