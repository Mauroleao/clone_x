import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
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
        
        
        User.objects.create_user(username='clone', email='original@email.com', password='123')
        
        
        url = '/api/users/register/'
        data = {
            'username': 'clone', 
            'email': 'impostor@email.com',
            'password': 'senhaforte'
        }
        response = self.client.post(url, data)
        
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
        self.assertEqual(User.objects.count(), 1)  
        
class UserLoginTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='usuario_teste',
            password='senha_super_secreta'
        )
        self.login_url = '/api/users/login/'
    def test_login_success(self):
        data = {
            'username': 'usuario_teste',
            'password': 'senha_super_secreta'
        }           
        
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        
class UserProfileUpdateTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        
        self.user = User.objects.create_user(
            username='usuario_perfil',
            password='senha_secreta',
            first_name='Nome Antigo'
        )
        self.profile_url = '/api/users/profile/'


        self.client.force_authenticate(user=self.user)

    def test_update_profile_name(self):
        """
        Testa se o usuário consegue alterar apenas o seu nome (Atualização Parcial/PATCH).
        """
        data = {
            'first_name': 'Nome Novo Atualizado'
            
        }
        
        
        response = self.client.patch(self.profile_url, data)
        
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Nome Novo Atualizado')        
        
    def test_update_profile_photo(self):
        """
        Testa se o usuário consegue enviar e salvar uma foto de perfil.
        """
        
        image_file = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(image_file, 'jpeg')
        image_file.seek(0)
        
    
        photo_upload = SimpleUploadedFile(
            "foto_teste.jpg", 
            image_file.read(), 
            content_type="image/jpeg"
        )
        
        data = {'photo': photo_upload}
        response = self.client.patch(self.profile_url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        
        self.assertTrue(self.user.profile.photo.name.startswith('profile_photos/foto_teste'))        