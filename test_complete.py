#!/usr/bin/env python3
"""
Teste completo de API - Clone X
Sem dependência de comandos no servidor
"""

import requests
import json
from datetime import datetime

BACKEND_URL = "https://clone-x-gml7.onrender.com"
API_URL = f"{BACKEND_URL}/api"

def color(code, text):
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'end': '\033[0m'
    }
    return f"{colors.get(code, '')}{text}{colors['end']}"

def print_header(text):
    print(f"\n{color('blue', '='*70)}")
    print(f"  {text}")
    print(f"{color('blue', '='*70)}\n")

def test_1_health():
    """Teste 1: Servidor online?"""
    print_header("TESTE 1: Health Check")
    
    try:
        response = requests.get(f"{BACKEND_URL}/admin/", timeout=5)
        if response.status_code in [200, 301, 302]:
            print(color('green', f"✅ Servidor online (Status: {response.status_code})"))
            return True
        else:
            print(color('red', f"❌ Servidor retornou {response.status_code}"))
            return False
    except Exception as e:
        print(color('red', f"❌ Erro: {str(e)}"))
        return False

def test_2_debug():
    """Teste 2: Endpoint debug disponível?"""
    print_header("TESTE 2: Endpoint Debug")
    
    try:
        response = requests.get(f"{API_URL}/users/debug/", timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(color('green', "✅ Debug endpoint funciona!"))
            print(json.dumps(data, indent=2))
            return True
        else:
            print(color('yellow', f"⚠️  Debug retornou {response.status_code}"))
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(color('red', f"❌ Erro: {str(e)}"))
        return False

def test_3_cors():
    """Teste 3: CORS configurado?"""
    print_header("TESTE 3: CORS")
    
    try:
        response = requests.options(
            f"{API_URL}/users/register/",
            headers={'Origin': 'http://localhost:5173'},
            timeout=5
        )
        
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        if cors_header:
            print(color('green', f"✅ CORS habilitado: {cors_header}"))
            return True
        else:
            print(color('yellow', "⚠️  CORS header não encontrado"))
            return False
    except Exception as e:
        print(color('red', f"❌ Erro: {str(e)}"))
        return False

def test_4_register():
    """Teste 4: Criar usuário"""
    print_header("TESTE 4: Registro de Usuário")
    
    timestamp = int(datetime.now().timestamp())
    user_data = {
        "username": f"test_{timestamp}",
        "email": f"test_{timestamp}@example.com",
        "password": "TestPass123!"
    }
    
    print(f"📤 Dados: {json.dumps(user_data, indent=2)}\n")
    
    try:
        response = requests.post(
            f"{API_URL}/users/register/",
            json=user_data,
            timeout=10
        )
        
        print(f"Status HTTP: {response.status_code}")
        print(f"Response: {response.text[:500]}\n")
        
        if response.status_code == 201:
            print(color('green', "✅ Usuário criado com sucesso!"))
            return True, response.json()
        elif response.status_code == 400:
            print(color('yellow', "⚠️  Erro 400 - Dados inválidos"))
            return False, response.json()
        elif response.status_code == 500:
            print(color('red', "❌ Erro 500 - Problema no servidor"))
            print("Verificar logs no Render Dashboard")
            return False, None
        else:
            print(color('red', f"❌ Erro {response.status_code}"))
            return False, None
    except Exception as e:
        print(color('red', f"❌ Erro: {str(e)}"))
        return False, None

def test_5_login(user_data):
    """Teste 5: Fazer login"""
    if not user_data:
        print_header("TESTE 5: Login (PULADO - sem dados de usuário)")
        return False, None
    
    print_header("TESTE 5: Login")
    
    login_data = {
        "username": user_data.get("username"),
        "password": "TestPass123!"
    }
    
    print(f"📤 Login: {login_data['username']}\n")
    
    try:
        response = requests.post(
            f"{API_URL}/users/login/",
            json=login_data,
            timeout=10
        )
        
        print(f"Status HTTP: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access', 'N/A')
            print(color('green', "✅ Login bem-sucedido!"))
            print(f"Token: {token[:20]}...\n")
            return True, token
        else:
            print(color('red', f"❌ Erro {response.status_code}"))
            print(f"Response: {response.text}\n")
            return False, None
    except Exception as e:
        print(color('red', f"❌ Erro: {str(e)}\n"))
        return False, None

def test_6_profile(token):
    """Teste 6: Acessar perfil (requer token)"""
    if not token:
        print_header("TESTE 6: Perfil (PULADO - sem token)")
        return False
    
    print_header("TESTE 6: Perfil do Usuário")
    
    try:
        response = requests.get(
            f"{API_URL}/users/profile/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        print(f"Status HTTP: {response.status_code}")
        
        if response.status_code == 200:
            print(color('green', "✅ Perfil acessado!"))
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print(color('red', f"❌ Erro {response.status_code}"))
            return False
    except Exception as e:
        print(color('red', f"❌ Erro: {str(e)}"))
        return False

def main():
    print(f"\n{color('blue', '='*70)}")
    print("   🚀 TESTE COMPLETO - Clone X Backend")
    print(f"{color('blue', '='*70)}")
    print(f"URL: {BACKEND_URL}")
    print(f"API: {API_URL}")
    print(f"Hora: {datetime.now()}\n")
    
    # Executar testes
    test1_ok = test_1_health()
    if not test1_ok:
        print(color('red', "\n❌ Servidor offline! Deploy no Render ainda em progresso."))
        print("Aguarde e tente novamente em alguns minutos.")
        return
    
    test2_ok = test_2_debug()
    test3_ok = test_3_cors()
    test4_ok, user_data = test_4_register()
    test5_ok, token = test_5_login(user_data)
    test6_ok = test_6_profile(token)
    
    # Resumo
    print_header("📊 RESUMO DOS TESTES")
    
    tests = [
        ("Health Check", test1_ok),
        ("Debug Endpoint", test2_ok),
        ("CORS", test3_ok),
        ("Registro", test4_ok),
        ("Login", test5_ok),
        ("Perfil", test6_ok),
    ]
    
    for name, result in tests:
        status = color('green', "✅") if result else color('red', "❌")
        print(f"{status} {name}")
    
    print()
    if all([test1_ok, test4_ok]):
        print(color('green', "🎉 Tudo funcionando corretamente!"))
    else:
        print(color('yellow', "⚠️  Há problemas a resolver. Veja os testes acima."))
    
    print()

if __name__ == "__main__":
    main()
