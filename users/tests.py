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