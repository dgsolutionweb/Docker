# Instruções para Implantação na VPS

## Pré-requisitos

Certifique-se de que sua VPS tenha:

- Docker instalado
- Docker Compose instalado
- PostgreSQL já rodando em contêiner Docker com porta 5432 exposta
- Porta 8000 liberada no firewall para a aplicação

## Preparação do Banco de Dados

Antes de iniciar a aplicação, crie um banco de dados chamado `estoque_db` no seu PostgreSQL:

```bash
docker exec -it SEU_CONTAINER_POSTGRES psql -U postgres -c "CREATE DATABASE estoque_db;"
```

## Passos para Implantação

1. Faça o upload dos arquivos para sua VPS:

```bash
# Se estiver usando SCP
scp -r . usuario@seu_servidor:/caminho/para/pasta
```

2. Acesse sua VPS via SSH:

```bash
ssh usuario@seu_servidor
```

3. Navegue até a pasta do projeto:

```bash
cd /caminho/para/pasta
```

4. Inicie o contêiner da aplicação:

```bash
docker-compose up -d
```

5. Verifique se o contêiner está rodando:

```bash
docker-compose ps
```

6. Verifique os logs se necessário:

```bash
docker-compose logs -f
```

7. Acesse o sistema através do navegador:

```
http://seu_ip_ou_dominio:8000
```

## Comandos Úteis

### Parar o contêiner

```bash
docker-compose down
```

### Reiniciar o contêiner

```bash
docker-compose restart
```

### Reconstruir a imagem após alterações

```bash
docker-compose down
docker-compose up --build -d
```

### Acessar o banco de dados PostgreSQL

```bash
docker exec -it SEU_CONTAINER_POSTGRES psql -U postgres -d estoque_db
```

### Acessar o shell do contêiner da aplicação

```bash
docker exec -it estoque_app bash
```

### Ver logs da aplicação

```bash
docker-compose logs -f web
```

## Solução de Problemas

1. Se a aplicação não iniciar, verifique os logs:

```bash
docker-compose logs -f web
```

2. Certifique-se de que o PostgreSQL está acessível:

```bash
docker exec -it estoque_app ping host.docker.internal
```

3. Verifique se o banco de dados estoque_db existe:

```bash
docker exec -it SEU_CONTAINER_POSTGRES psql -U postgres -c "\l"
```

4. Reinicie o contêiner após alterações no código:

```bash
docker-compose restart web
```