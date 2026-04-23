import logging
import threading
from django.core.management import call_command
from django.db.utils import OperationalError
from django.db import connection

logger = logging.getLogger(__name__)

_migrations_checked = False
_migrations_lock = threading.Lock()


class EnsureMigrationsMiddleware:
    """Executa migrations na primeira requisição (thread-safe)"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        global _migrations_checked
        
        if not _migrations_checked:
            with _migrations_lock:
                # Double-check depois de adquirir lock
                if not _migrations_checked:
                    self._ensure_migrations()
        
        return self.get_response(request)
    
    @staticmethod
    def _ensure_migrations():
        """Executa migrations se não tiverem sido executadas"""
        global _migrations_checked
        
        try:
            # Teste rápido: vê se a tabela auth_user existe
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='auth_user';")
                if cursor.fetchone():
                    # Tabelas já existem
                    _migrations_checked = True
                    return
            
            # Se chegou aqui, precisa fazer as migrations
            logger.info("Executando migrations...")
            call_command('migrate', verbosity=0, interactive=False)
            logger.info("Migrations completadas com sucesso")
            _migrations_checked = True
            
        except Exception as e:
            logger.error(f"Erro ao executar migrations: {str(e)}")
            _migrations_checked = False
            # Não falha o servidor se as migrations falharem
            pass
