#!/usr/bin/env python
import os
import sys
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

max_setup_attempts = 3
for attempt in range(1, max_setup_attempts + 1):
    try:
        django.setup()
        break
    except Exception as e:
        if attempt < max_setup_attempts:
            time.sleep(2)
        else:
            sys.exit(1)

def run_migrations():
    from django.core.management import call_command
    from django.db import connection
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
            if cursor.fetchone():
                return True
    except:
        pass
    
    for attempt in range(1, 4):
        try:
            call_command('migrate', verbosity=0, interactive=False)
            return True
        except:
            if attempt < 3:
                time.sleep(2)
    
    return False

def verify_database():
    try:
        from django.contrib.auth.models import User
        user_count = User.objects.count()
        if user_count == 0:
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        return True
    except:
        return False

def collect_static():
    try:
        from django.core.management import call_command
        call_command('collectstatic', verbosity=0, interactive=False)
        return True
    except:
        return False

def start_gunicorn():
    port = os.getenv('PORT', '8000')
    workers = os.getenv('WEB_CONCURRENCY', '2')
    
    if sys.platform == 'win32':
        from django.core.management import call_command
        call_command('runserver', f'0.0.0.0:{port}', verbosity=2)
    else:
        cmd = f"gunicorn backend.wsgi:application --bind 0.0.0.0:{port} --workers {workers}"
        os.system(cmd)

def main():
    run_migrations()
    verify_database()
    collect_static()
    start_gunicorn()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        sys.exit(1)

