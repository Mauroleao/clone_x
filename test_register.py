#!/usr/bin/env python3
"""
Teste especifico para o endpoint de registro
"""

import requests
import json
from datetime import datetime
import time

BACKEND_URL = "https://clone-x-gml7.onrender.com"
API_URL = f"{BACKEND_URL}/api"

def test_register_detailed():
    """Testa o registro com detalhes"""
    
    print("\n" + "="*70)
    print("🔍 TESTE DETALHADO DE REGISTRO")
    print("="*70 + "\n")
    
    timestamp = int(datetime.now().timestamp())
    user_data = {
        "username": f"testuser_{timestamp}",
        "email": f"test_{timestamp}@example.com",
        "password": "TestPassword123!"
    }
    
    print(f"📤 Enviando dados:")
    print(json.dumps(user_data, indent=2))
    print()
    
    try:
        print("⏳ Conectando ao servidor...")
        response = requests.post(
            f"{API_URL}/users/register/",
            json=user_data,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"✅ Resposta recebida!\n")
        print(f"📊 Status HTTP: {response.status_code}")
        print(f"📋 Headers:")
        for key, value in response.headers.items():
            print(f"   {key}: {value}")
        
        print(f"\n📄 Response Body:")
        try:
            data = response.json()
            print(json.dumps(data, indent=2))
        except:
            print(response.text)
        
        print("\n" + "="*70)
        
        if response.status_code == 201:
            print("✅ SUCESSO! Usuário criado com sucesso!")
            print("="*70 + "\n")
            return True
        elif response.status_code == 400:
            print("⚠️  ERRO 400 - Bad Request (Dados inválidos)")
            print("="*70 + "\n")
            return False
        elif response.status_code == 500:
            print("❌ ERRO 500 - Server Error (Problema no servidor)")
            print("="*70 + "\n")
            return False
        else:
            print(f"❌ ERRO {response.status_code} - Resposta inesperada")
            print("="*70 + "\n")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Não conseguiu conectar ao servidor")
        print("Verifique se:")
        print("  - O servidor está online em https://clone-x-gml7.onrender.com")
        print("  - Você tem conexão com internet")
        print("="*70 + "\n")
        return False
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        print("="*70 + "\n")
        return False

def test_cors():
    """Testa se CORS está habilitado"""
    print("\n" + "="*70)
    print("🔍 TESTE DE CORS")
    print("="*70 + "\n")
    
    try:
        response = requests.options(
            f"{API_URL}/users/register/",
            headers={
                'Origin': 'http://localhost:5173',
                'Access-Control-Request-Method': 'POST'
            },
            timeout=5
        )
        
        cors_origin = response.headers.get('Access-Control-Allow-Origin')
        cors_methods = response.headers.get('Access-Control-Allow-Methods')
        
        print(f"Access-Control-Allow-Origin: {cors_origin}")
        print(f"Access-Control-Allow-Methods: {cors_methods}")
        
        if cors_origin:
            print("\n✅ CORS está habilitado!")
        else:
            print("\n⚠️  CORS pode não estar configurado corretamente")
        
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"❌ Erro ao testar CORS: {str(e)}")
        print("="*70 + "\n")

if __name__ == "__main__":
    print(f"\n🚀 Teste de Registro - Clone X")
    print(f"Backend: {BACKEND_URL}")
    print(f"Timestamp: {datetime.now()}\n")
    
    # Testar CORS
    test_cors()
    
    # Testar Registro
    success = test_register_detailed()
    
    if success:
        print("🎉 Tudo funcionando!")
    else:
        print("🔧 Há um problema a ser resolvido")
