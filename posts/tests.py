from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post

class PostTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        # Criamos o usuário autor do post e damos o "crachá" pra ele
        self.user = User.objects.create_user(username='autor', password='123')
        self.client.force_authenticate(user=self.user)
        
        # A URL que vamos criar para receber os posts
        self.url = '/api/posts/'

    def test_create_post(self):
        """
        Testa se um usuário logado consegue criar uma nova postagem.
        """
        data = {
            'content': 'Este é o meu primeiro post no Clone do X!'
        }
        
        # Enviamos os dados via POST
        response = self.client.post(self.url, data)
        
        # 1. A API deve retornar 201 CREATED (Criado com sucesso)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 2. O banco de dados deve ter exatamente 1 post agora
        self.assertEqual(Post.objects.count(), 1)
        
        # 3. O autor do post salvo no banco deve ser o nosso usuário logado
        self.assertEqual(Post.objects.first().author, self.user)

    def test_personalized_feed(self):
        """
        Testa se o Feed retorna apenas os posts do usuário e das pessoas que ele segue.
        """
        User = get_user_model()
        
        # 1. Criamos os figurantes
        user_maria = User.objects.create_user(username='maria', password='123')
        user_pedro = User.objects.create_user(username='pedro', password='123')
        
        # 2. O João (self.user) segue a Maria
        self.user.profile.follows.add(user_maria.profile)
        
        # 3. Todo mundo publica um post
        Post.objects.create(author=self.user, content='Post do Joao')
        Post.objects.create(author=user_maria, content='Post da Maria')
        Post.objects.create(author=user_pedro, content='Post do Pedro (Invisível)')
        
        # 4. O João acessa o Feed (Faz um GET na rota de posts)
        response = self.client.get(self.url)
        
        # 5. Validações
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # AQUI É O PONTO CHAVE: O banco tem 3 posts no total, 
        # mas a API tem que devolver apenas 2 na lista!
        self.assertEqual(len(response.data), 2)
        
    def test_toggle_like_post(self):
        """
        Testa se um usuário consegue curtir e descurtir um post (Interruptor).
        """
        User = get_user_model()
        
        # 1. Criamos a Maria e um post para ela
        user_maria = User.objects.create_user(username='maria_autora', password='123')
        post_da_maria = Post.objects.create(author=user_maria, content='Bom dia, mundo!')
        
        # A URL do botão de curtir (ex: /api/posts/1/like/)
        url_like = f'/api/posts/{post_da_maria.id}/like/'
        
        # 2. O João (nosso self.user que já está logado) clica em curtir a primeira vez
        response_like = self.client.post(url_like)
        
        # Esperamos que a API dê OK e que o post agora tenha 1 curtida no banco
        self.assertEqual(response_like.status_code, status.HTTP_200_OK)
        self.assertEqual(post_da_maria.likes.count(), 1)
        
        # 3. O João clica de novo (simulando que se arrependeu e descurtiu)
        response_unlike = self.client.post(url_like)
        
        # Esperamos que a API dê OK e que a curtida suma do banco
        self.assertEqual(response_unlike.status_code, status.HTTP_200_OK)
        self.assertEqual(post_da_maria.likes.count(), 0)    