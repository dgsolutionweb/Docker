# Instruções para Implantação na VPS

## Pré-requisitos

Certifique-se de que sua VPS tenha:

- Docker instalado
- Docker Compose instalado
- Portas 8000 (aplicação) e 5432 (PostgreSQL) liberadas no firewall

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

4. Inicie os contêineres Docker:

```bash
docker-compose up -d
```

5. Verifique se os contêineres estão rodando:

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

### Parar os contêineres

```bash
docker-compose down
```

### Reiniciar os contêineres

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
docker exec -it estoque_db psql -U postgres -d estoque_db
```

### Acessar o shell do contêiner da aplicação

```bash
docker exec -it estoque_app bash
```

### Ver logs da aplicação

```bash
docker-compose logs -f web
```

### Ver logs do banco de dados

```bash
docker-compose logs -f db
```

## Solução de Problemas

1. Se a aplicação não iniciar, verifique os logs:

```bash
docker-compose logs -f web
```

2. Se o banco de dados não iniciar, verifique os logs:

```bash
docker-compose logs -f db
```

3. Reinicie os contêineres após alterações no código:

```bash
docker-compose restart web
```

4. Verifique o status da rede Docker:

```bash
docker network ls
docker network inspect estoque_network
```

5. Em caso de problemas com o volume do PostgreSQL:

```bash
docker volume ls
docker volume inspect postgres_data
``` 