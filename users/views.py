from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from .models import Follow, Profile
from .serializers import UserSerializer, UserDetailSerializer
import traceback
import logging

logger = logging.getLogger(__name__)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        """Override para melhor tratamento de erro"""
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print(f"Erro ao registrar usuário: {str(e)}")
            traceback.print_exc()
            return Response(
                {"error": f"Erro ao registrar: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, username=None):
        if username:
            user = get_object_or_404(User, username=username)
        else:
            user = request.user
        serializer = UserDetailSerializer(user, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, username=None):
        if username:
            user = get_object_or_404(User, username=username)
            if user != request.user:
                return Response(
                    {"error": "Você só pode atualizar seu próprio perfil"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            user = request.user
            
        profile = user.profile
        
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
            profile.save()
        
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        
        if 'email' in request.data:
            user.email = request.data['email']
        
        if 'bio' in request.data:
            profile.bio = request.data['bio']
            profile.save()
        
        user.save()
        
        serializer = UserDetailSerializer(user, context={'request': request})
        return Response(serializer.data)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response(
                {"error": "Senha atual e nova senha são obrigatórias"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.check_password(old_password):
            return Response(
                {"error": "Senha atual está incorreta"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        return Response({"message": "Senha alterada com sucesso"}, status=status.HTTP_200_OK)

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        user_to_follow = get_object_or_404(User, username=username)
        
        if request.user == user_to_follow:
            return Response(
                {"error": "Você não pode seguir a si mesmo"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        follow_obj, created = Follow.objects.get_or_create(
            user=request.user, 
            followed_user=user_to_follow
        )

        if not created:
            follow_obj.delete()
            return Response({"message": "Deixou de seguir"}, status=status.HTTP_200_OK)

        return Response({"message": "Seguindo com sucesso"}, status=status.HTTP_201_CREATED)


class DebugView(APIView):
    """Endpoint de debug - ver se as coisas estão funcionando"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Retornar informações de debug"""
        from django.conf import settings
        return Response({
            "status": "ok",
            "debug": settings.DEBUG,
            "allowed_hosts": settings.ALLOWED_HOSTS,
            "database": "ok" if User.objects.count() >= 0 else "error",
            "users_count": User.objects.count(),
            "profiles_count": Profile.objects.count(),
        })


class LoginView(APIView):
    """View customizada de login com melhor tratamento de erro"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Fazer login e retornar tokens JWT"""
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Usuário e senha são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Verificar se o usuário existe
            user = User.objects.filter(username=username).first()
            
            if not user:
                logger.warning(f"Tentativa de login com usuário inexistente: {username}")
                return Response(
                    {'error': 'Usuário ou senha inválidos'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Autenticar o usuário
            authenticated_user = authenticate(username=username, password=password)
            
            if not authenticated_user:
                logger.warning(f"Falha de autenticação para usuário: {username}")
                return Response(
                    {'error': 'Usuário ou senha inválidos'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Gerar tokens JWT
            refresh = RefreshToken.for_user(authenticated_user)
            
            logger.info(f"Login bem-sucedido para usuário: {username}")
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': authenticated_user.id,
                    'username': authenticated_user.username,
                    'email': authenticated_user.email,
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Erro no login: {str(e)}\n{traceback.format_exc()}")
            return Response(
                {'error': f'Erro ao fazer login: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )