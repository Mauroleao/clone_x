#!/bin/bash

# Script auxiliar para Docker (Linux/Mac)

if [ -z "$1" ]; then
    echo ""
    echo "Uso: ./docker-helper.sh [comando]"
    echo ""
    echo "Comandos disponiveis:"
    echo "  up            - Iniciar containers"
    echo "  down          - Parar containers"
    echo "  build         - Fazer build das imagens"
    echo "  logs          - Ver logs"
    echo "  logs-backend  - Ver logs do backend"
    echo "  logs-frontend - Ver logs do frontend"
    echo "  bash          - Acessar shell do backend"
    echo "  migrate       - Executar migrations"
    echo "  superuser     - Criar superuser"
    echo "  reset         - Reset completo (delete volumes)"
    echo "  shell         - Shell Django interativo"
    echo ""
    exit 0
fi

case "$1" in
    up)
        docker-compose up -d
        echo "Backend em: http://localhost:8000"
        echo "Frontend em: http://localhost:5173"
        ;;
    down)
        docker-compose down
        ;;
    build)
        docker-compose build
        ;;
    logs)
        docker-compose logs -f
        ;;
    logs-backend)
        docker-compose logs -f backend
        ;;
    logs-frontend)
        docker-compose logs -f frontend
        ;;
    bash)
        docker-compose exec backend bash
        ;;
    migrate)
        docker-compose exec backend python manage.py migrate
        ;;
    superuser)
        docker-compose exec backend python manage.py createsuperuser
        ;;
    shell)
        docker-compose exec backend python manage.py shell
        ;;
    reset)
        echo "Deletando containers e volumes..."
        docker-compose down -v
        echo "Fazendo rebuild..."
        docker-compose build --no-cache
        echo "Iniciando..."
        docker-compose up -d
        ;;
    *)
        echo "Comando nao reconhecido: $1"
        ;;
esac
