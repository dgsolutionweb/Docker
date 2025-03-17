# Sistema de Gerenciamento de Estoque - Ambiente de Produção

Este documento contém instruções para configurar e executar o sistema em ambiente de produção.

## Requisitos

- Docker e Docker Compose instalados
- OpenSSL (para geração de certificados)
- Domínio configurado (opcional, para produção real)

## Configuração Inicial

1. **Clone o repositório**

```powershell
git clone <URL-DO-REPOSITORIO>
cd <DIRETORIO-DO-PROJETO>
```

2. **Configure as variáveis de ambiente**

Edite o arquivo `.env.prod` com as suas configurações:

```
# Configurações do Banco de Dados
DB_USER=postgres
DB_PASSWORD=sua-senha-segura
DB_NAME=estoque_db

# Configurações da Aplicação
SECRET_KEY=sua-chave-secreta-gerada-aleatoriamente
FLASK_ENV=production
DEBUG=False
```

Para gerar uma SECRET_KEY segura, você pode executar:

```powershell
openssl rand -base64 32
```

3. **Prepare os certificados SSL**

Para ambiente de teste, você pode usar certificados autoassinados:

```powershell
# Execute o script para gerar certificados
.\gerar_certificado.ps1
```

Para produção real, recomendamos obter certificados válidos (Let's Encrypt).

## Deploy

Execute o script de deploy:

```powershell
.\deploy_prod.ps1
```

Este script irá:
- Gerar certificados SSL (se necessário)
- Fazer backup do banco de dados (se existir)
- Parar containers existentes
- Iniciar a aplicação em modo produção
- Verificar status dos containers

## Acesso

Após o deploy, o sistema estará disponível em:

- https://seu-dominio (substituir pelo seu domínio)
- https://localhost (ambiente local)

## Backup e Manutenção

### Backup Manual do Banco de Dados

```powershell
$data = Get-Date -Format "yyyyMMdd_HHmmss"
docker exec estoque_db pg_dump -U postgres estoque_db > "./backups/backup_$data.sql"
```

### Restaurar Backup

```powershell
docker exec -i estoque_db psql -U postgres estoque_db < "./backups/seu_arquivo_backup.sql"
```

### Verificar Logs

```powershell
# Logs da aplicação
docker logs estoque_app

# Logs do Nginx
docker logs estoque_nginx

# Logs do banco de dados
docker logs estoque_db
```

## Segurança

- Mude regularmente as senhas no arquivo `.env.prod`
- Mantenha os containers atualizados
- Faça backups regulares do banco de dados
- Configure firewall na VPS

## Troubleshooting

### Aplicação não inicia
```
docker logs estoque_app
```

### Problemas com Nginx
```
docker logs estoque_nginx
```

### Problemas com Certificados SSL
Verifique se os certificados foram gerados corretamente em `./nginx/ssl/` 