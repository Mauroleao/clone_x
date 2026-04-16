from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class UserRegistrationTests(APITestCase):
    def test_register_new_user(self):
        """
        Testa se a API permite a criação de um novo usuário
        enviando username, email e password.
        """
        url = '/api/users/register/' 
        
        data = {
            'username': 'novousuario',
            'email': 'novo@email.com',
            'password': 'senhaforte123'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        User = get_user_model()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'novousuario')
        
        
    def test_register_existing_username(self):
        """
        Testa se a API bloqueia a criação de um usuário 
        com um username que já existe no banco de dados.
        """
        User = get_user_model()
        
        # 1. Primeiro, criamos um usuário direto no banco de dados
        User.objects.create_user(username='clone', email='original@email.com', password='123')
        
        # 2. Agora, tentamos usar a API para criar outro com o mesmo username
        url = '/api/users/register/'
        data = {
            'username': 'clone', # Username repetido!
            'email': 'impostor@email.com',
            'password': 'senhaforte'
        }
        response = self.client.post(url, data)
        
        # 3. A API DEVE negar o cadastro (Status 400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # 4. Garantimos que o banco de dados continua tendo apenas 1 usuário
        self.assertEqual(User.objects.count(), 1)    