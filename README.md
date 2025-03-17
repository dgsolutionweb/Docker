# Sistema de Gerenciamento de Estoque

Um sistema simples para gerenciamento de estoque desenvolvido com Python, Flask e PostgreSQL, pronto para ser executado em Docker.

## Características

- Cadastro de produtos e categorias
- Controle de entradas e saídas de produtos
- Dashboard com informações de estoque e movimentações
- Relatórios de movimentações com filtros
- Interface amigável e responsiva
- Pronto para uso em ambiente de produção com Docker

## Tecnologias Utilizadas

- **Backend**: Python com Flask e SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript com Bootstrap 5
- **Banco de Dados**: PostgreSQL
- **Conteinerização**: Docker e Docker Compose

## Como Executar

### Pré-requisitos

- Docker
- Docker Compose

### Passos para Execução

1. Clone este repositório
2. Execute o comando:

```bash
docker-compose up -d
```

3. Acesse o sistema em seu navegador: http://localhost:8000

## Estrutura do Projeto

```
.
├── app/
│   ├── models/          # Modelos de dados e formulários
│   ├── static/          # Arquivos estáticos (CSS, JS)
│   ├── templates/       # Templates HTML
│   ├── app.py           # Aplicação principal
│   ├── config.py        # Configurações
│   ├── Dockerfile       # Configuração Docker
│   └── requirements.txt # Dependências Python
└── docker-compose.yml   # Configuração Docker Compose
```

## Screenshots

Acesse as imagens do sistema em funcionamento na pasta `screenshots/` (se disponível).

## Desenvolvimento

### Como Fazer Modificações

1. Edite os arquivos conforme necessário
2. Para reconstruir a imagem e atualizar os containers:

```bash
docker-compose down
docker-compose up --build -d
```

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

## Contato

Para mais informações ou dúvidas, entre em contato. 