# Clone X

Projeto de rede social feito com Django (backend REST API) e React + Vite (frontend). Esse projeto simula as funcionalidades basicas do Twitter/X, como feed, perfis, curtidas e comentarios.

Excelente para quem esta estudando desenvolvimento web e quer ver como integrar um backend Python/Django com um frontend React.

## Pre-requisitos

Antes de comecar, voce vai precisar ter instalado na sua maquina:
- Git (para clonar o projeto)
- Python 3.11 ou superior
- Node.js 18 ou superior
- Poetry (gerenciador de dependencias do Python. Instale com: pip install poetry)

## Passo a passo para rodar localmente

### 1. Clonar o repositorio
Primeiro, baixe o codigo para a sua maquina:
```bash
git clone https://github.com/Mauroleao/clone_x.git
cd clone_x
```

### 2. Configurar e rodar o Backend (Django)
O backend usa Python. Vamos configurar as variaveis de sistema, instalar os pacotes e criar o banco de dados inicial (SQLite).

Crie uma copia do arquivo de configuracao (no Windows, voce pode copiar e colar pelo explorador de arquivos, basta copiar o .env.example e renomear a copia para .env):
```bash
cp .env.example .env
```

Agora, instale as dependencias e inicie o servidor:
```bash
# Instala as bibliotecas do Python
poetry install

# Ativa o ambiente virtual isolado do projeto
poetry shell

# Cria as tabelas do banco de dados (SQLite por padrao)
python manage.py migrate

# Inicia o servidor local do backend
python manage.py runserver
```

Se tudo deu certo, a API estara rodando em http://localhost:8000.

### 3. Configurar e rodar o Frontend (React)
Abra uma **nova aba ou janela no seu terminal** (deixe o terminal do backend rodando). 

Navegue ate a pasta do frontend, instale os pacotes do Node e inicie a interface:
```bash
# Entra na pasta do front
cd frontend

# Instala as dependencias (React, Vite, Axios, etc)
npm install

# Roda o servidor de desenvolvimento do frontend
npm run dev
```

O Vite vai inicializar a interface do site em http://localhost:5173. Basta abrir esse link no seu navegador.

## Observacoes
- **Banco de Dados**: O sistema comeca usando SQLite (um arquivo db.sqlite3 sera gerado automaticamente na sua pasta). Se for subir para producao futuramente, basta configurar a variavel DATABASE_URL no .env para apontar para um PostgreSQL.
- **CORS**: O projeto ja esta configurado no Django para permitir que o React local consiga fazer requisicoes para ele livremente.
