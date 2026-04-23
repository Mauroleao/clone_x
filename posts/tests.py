from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post

class PostTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        
        self.user = User.objects.create_user(username='autor', password='123')
        self.client.force_authenticate(user=self.user)
        
        
        self.url = '/api/posts/'

    def test_create_post(self):
        """
        Testa se um usuário logado consegue criar uma nova postagem.
        """
        data = {
            'content': 'Este é o meu primeiro post no Clone do X!'
        }
        
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Post.objects.count(), 1)
        
        self.assertEqual(Post.objects.first().author, self.user)

    def test_personalized_feed(self):
        """
        Testa se o Feed retorna apenas os posts do usuário e das pessoas que ele segue.
        """
        User = get_user_model()
        
        user_maria = User.objects.create_user(username='maria', password='123')
        user_pedro = User.objects.create_user(username='pedro', password='123')
        
        self.user.profile.follows.add(user_maria.profile)
        
        Post.objects.create(author=self.user, content='Post do Joao')
        Post.objects.create(author=user_maria, content='Post da Maria')
        Post.objects.create(author=user_pedro, content='Post do Pedro (Invisível)')
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), 2)
        
    def test_toggle_like_post(self):
        """
        Testa se um usuário consegue curtir e descurtir um post (Interruptor).
        """
        User = get_user_model()
        
        
        user_maria = User.objects.create_user(username='maria_autora', password='123')
        post_da_maria = Post.objects.create(author=user_maria, content='Bom dia, mundo!')
        
    
        url_like = f'/api/posts/{post_da_maria.id}/like/'
        
        
        response_like = self.client.post(url_like)
        
       
        self.assertEqual(response_like.status_code, status.HTTP_200_OK)
        self.assertEqual(post_da_maria.likes.count(), 1)
        
        
        response_unlike = self.client.post(url_like)
        
        
        self.assertEqual(response_unlike.status_code, status.HTTP_200_OK)
        self.assertEqual(post_da_maria.likes.count(), 0)    