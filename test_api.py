#!/usr/bin/env python3
"""
Script para testar conexão com o backend Django no Render
Execute: python test_api.py
"""

import requests
import json
from datetime import datetime

# Configuração
BACKEND_URL = "https://clone-x-gml7.onrender.com"
API_URL = f"{BACKEND_URL}/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.END}\n")

def test_health():
    """Testa se o servidor está online"""
    print_header("🔍 Teste 1: Health Check")
    
    try:
        response = requests.get(f"{BACKEND_URL}/admin/", timeout=10)
        if response.status_code == 301 or response.status_code == 200:
            print(f"{Colors.GREEN}✅ Servidor respondendo (Status: {response.status_code}){Colors.END}")
            return True
        else:
            print(f"{Colors.RED}❌ Servidor respondeu com status {response.status_code}{Colors.END}")
            return False
    except Exception as e:
        print(f"{Colors.RED}❌ Erro ao conectar: {str(e)}{Colors.END}")
        return False

def test_register():
    """Testa o endpoint de registro"""
    print_header("🔍 Teste 2: Registro de Usuário")
    
    timestamp = int(datetime.now().timestamp())
    user_data = {
        "username": f"testuser_{timestamp}",
        "email": f"test_{timestamp}@example.com",
        "password": "TestPassword123!"
    }
    
    print(f"Enviando: {json.dumps(user_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{API_URL}/users/register/",
            json=user_data,
            timeout=10
        )
        
        print(f"\nStatus: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print(f"{Colors.GREEN}✅ Usuário criado com sucesso!{Colors.END}")
            return response.json()
        elif response.status_code == 400:
            print(f"{Colors.YELLOW}⚠️  Erro de validação (possivelmente usuário já existe){Colors.END}")
            return None
        else:
            print(f"{Colors.RED}❌ Erro ao criar usuário (Status: {response.status_code}){Colors.END}")
            return None
    except Exception as e:
        print(f"{Colors.RED}❌ Erro na requisição: {str(e)}{Colors.END}")
        return None

def test_login():
    """Testa o endpoint de login"""
    print_header("🔍 Teste 3: Login")
    
    login_data = {
        "username": "testuser_login",
        "password": "TestPassword123!"
    }
    
    print(f"Tentando login com: {login_data['username']}")
    
    try:
        response = requests.post(
            f"{API_URL}/users/login/",
            json=login_data,
            timeout=10
        )
        
        print(f"\nStatus: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"{Colors.GREEN}✅ Login bem-sucedido!{Colors.END}")
            print(f"Access Token: {data.get('access', 'N/A')[:20]}...")
            return data.get('access')
        elif response.status_code == 401:
            print(f"{Colors.YELLOW}⚠️  Credenciais inválidas{Colors.END}")
            print(f"Response: {response.text}")
            return None
        else:
            print(f"{Colors.RED}❌ Erro ao fazer login (Status: {response.status_code}){Colors.END}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"{Colors.RED}❌ Erro na requisição: {str(e)}{Colors.END}")
        return None

def test_profile(token):
    """Testa o endpoint de perfil (requer token)"""
    print_header("🔍 Teste 4: Perfil do Usuário (Autenticado)")
    
    if not token:
        print(f"{Colors.YELLOW}⚠️  Token não disponível, pulando teste{Colors.END}")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{API_URL}/users/profile/",
            headers=headers,
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"{Colors.GREEN}✅ Perfil acessado com sucesso!{Colors.END}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"{Colors.RED}❌ Erro ao acessar perfil (Status: {response.status_code}){Colors.END}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"{Colors.RED}❌ Erro na requisição: {str(e)}{Colors.END}")
        return False

def test_cors():
    """Testa se CORS está configurado"""
    print_header("🔍 Teste 5: CORS Configuration")
    
    headers = {
        "Origin": "http://localhost:5173"
    }
    
    try:
        response = requests.options(
            f"{API_URL}/users/register/",
            headers=headers,
            timeout=10
        )
        
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        if cors_header:
            print(f"{Colors.GREEN}✅ CORS habilitado!{Colors.END}")
            print(f"Access-Control-Allow-Origin: {cors_header}")
            return True
        else:
            print(f"{Colors.YELLOW}⚠️  CORS header não encontrado{Colors.END}")
            return False
    except Exception as e:
        print(f"{Colors.RED}❌ Erro ao testar CORS: {str(e)}{Colors.END}")
        return False

def main():
    print(f"\n{Colors.BLUE}{'='*60}")
    print("   🚀 Teste de Conectividade - Clone X Backend")
    print(f"{'='*60}{Colors.END}")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"API URL: {API_URL}")
    print(f"Timestamp: {datetime.now()}")
    
    # Executar testes
    health_ok = test_health()
    
    if not health_ok:
        print(f"\n{Colors.RED}❌ Servidor offline. Verifique o Render Dashboard.{Colors.END}")
        return
    
    cors_ok = test_cors()
    register_ok = test_register()
    token = test_login()
    test_profile(token)
    
    # Resumo
    print_header("📊 Resumo dos Testes")
    print(f"✅ Servidor Online: SIM")
    print(f"✅ CORS: {'SIM' if cors_ok else 'NÃO'}")
    print(f"✅ Registro: {'SIM' if register_ok else 'NÃO'}")
    print(f"✅ Login: {'SIM' if token else 'NÃO'}")
    print(f"✅ Perfil: Testado com token")
    
    print(f"\n{Colors.GREEN}Testes concluídos!{Colors.END}\n")

if __name__ == "__main__":
    main()
