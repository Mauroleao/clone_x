@echo off
REM Script auxiliar para Docker no Windows

if "%1"=="" (
    echo.
    echo Uso: docker-helper.bat [comando]
    echo.
    echo Comandos disponiveis:
    echo   up           - Iniciar containers
    echo   down         - Parar containers
    echo   build        - Fazer build das imagens
    echo   logs         - Ver logs
    echo   logs-backend - Ver logs do backend
    echo   logs-frontend- Ver logs do frontend
    echo   bash         - Acessar shell do backend
    echo   migrate      - Executar migrations
    echo   superuser    - Criar superuser
    echo   reset        - Reset completo (delete volumes)
    echo   shell        - Shell Django interativo
    echo.
    goto :eof
)

if "%1"=="up" (
    docker-compose up -d
    echo Backend em: http://localhost:8000
    echo Frontend em: http://localhost:5173
    goto :eof
)

if "%1"=="down" (
    docker-compose down
    goto :eof
)

if "%1"=="build" (
    docker-compose build
    goto :eof
)

if "%1"=="logs" (
    docker-compose logs -f
    goto :eof
)

if "%1"=="logs-backend" (
    docker-compose logs -f backend
    goto :eof
)

if "%1"=="logs-frontend" (
    docker-compose logs -f frontend
    goto :eof
)

if "%1"=="bash" (
    docker-compose exec backend bash
    goto :eof
)

if "%1"=="migrate" (
    docker-compose exec backend python manage.py migrate
    goto :eof
)

if "%1"=="superuser" (
    docker-compose exec backend python manage.py createsuperuser
    goto :eof
)

if "%1"=="shell" (
    docker-compose exec backend python manage.py shell
    goto :eof
)

if "%1"=="reset" (
    echo Deletando containers e volumes...
    docker-compose down -v
    echo Fazendo rebuild...
    docker-compose build --no-cache
    echo Iniciando...
    docker-compose up -d
    goto :eof
)

echo Comando nao reconhecido: %1
