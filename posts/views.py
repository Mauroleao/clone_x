from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q 
from .models import Post
from .serializers import PostSerializer

class PostListCreateView(generics.ListCreateAPIView):
    # ... (Essa classe continua igualzinha, não mude nada nela!)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        perfis_seguidos = user.profile.follows.all()
        return Post.objects.filter(
            Q(author=user) | Q(author__profile__in=perfis_seguidos)
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# --- ADICIONE ESTA NOVA CLASSE NO FINAL ---
class ToggleLikePostView(APIView):
    """
    View para curtir ou descurtir uma postagem (Interruptor).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        # 1. Pega o post no banco de dados (ou dá 404 se não existir)
        post = get_object_or_404(Post, id=id)
        
        # 2. Quem está apertando o botão?
        user = request.user

        # 3. A Lógica do Interruptor
        if post.likes.filter(id=user.id).exists():
            # Se já curtiu, arranca o like
            post.likes.remove(user)
            return Response({"message": "Você descurtiu o post."}, status=status.HTTP_200_OK)
        else:
            # Se não curtiu, adiciona o like
            post.likes.add(user)
            return Response({"message": "Você curtiu o post."}, status=status.HTTP_200_OK)