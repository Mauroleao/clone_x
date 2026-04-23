#!/bin/bash
set -e

# Script para preparar o backend para produção

# Instalar dependências
echo "📦 Dependências já foram instaladas no build..."

# Fazer migrações
echo "📊 Rodando migrations..."
python manage.py migrate

# Coletar arquivos estáticos
echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar servidor com gunicorn
echo "🚀 Iniciando gunicorn na porta $PORT..."
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --log-file -
