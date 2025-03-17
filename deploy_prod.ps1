# Script para fazer deploy em produção
Write-Host "Iniciando deploy em ambiente de produção..." -ForegroundColor Green

# Gerar certificado SSL caso não exista
if (!(Test-Path ".\nginx\ssl\estoque.crt")) {
    Write-Host "Gerando certificado SSL..." -ForegroundColor Yellow
    .\gerar_certificado.ps1
}

# Verificar se .env.prod existe
if (!(Test-Path ".\.env.prod")) {
    Write-Host "ATENÇÃO: Arquivo .env.prod não encontrado!" -ForegroundColor Red
    Write-Host "Por favor, crie o arquivo .env.prod com as configurações corretas." -ForegroundColor Red
    Exit
}

# Backup do banco de dados (se estiver rodando)
Write-Host "Tentando fazer backup do banco de dados..." -ForegroundColor Yellow
$data = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = ".\backups"

if (!(Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir -Force
}

docker exec estoque_db pg_dump -U postgres estoque_db > "$backupDir\backup_$data.sql"
if ($LASTEXITCODE -eq 0) {
    Write-Host "Backup realizado com sucesso: $backupDir\backup_$data.sql" -ForegroundColor Green
} else {
    Write-Host "Aviso: Não foi possível fazer backup do banco de dados." -ForegroundColor Yellow
}

# Parar containers existentes
Write-Host "Parando containers existentes..." -ForegroundColor Yellow
docker-compose down

# Iniciar a aplicação em modo produção
Write-Host "Iniciando aplicação em modo produção..." -ForegroundColor Green
docker-compose -f docker-compose.prod.yml up -d

# Verificar status dos containers
Write-Host "Verificando status dos containers..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
docker ps

Write-Host "Deploy concluído! A aplicação está rodando em modo produção." -ForegroundColor Green
Write-Host "Para acessar: https://localhost" -ForegroundColor Green 