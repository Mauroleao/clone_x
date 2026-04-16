from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated 
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] 

    def get_object(self):
        return self.request.user
    
    
class FollowUserView(APIView):
    """
    View para seguir ou deixar de seguir um usuário (Toggle).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, id): # Recebe o ID da URL!
        # 1. Quem é o usuário alvo (A Maria)? 
        # O get_object_or_404 já retorna erro 404 automático se o ID não existir no banco.
        target_user = get_object_or_404(User, id=id)

        # 2. Quem está fazendo a ação (O João dono do token)?
        me = request.user.profile
        target_profile = target_user.profile

        # 3. Regra de segurança: Não posso seguir a mim mesmo!
        if me == target_profile:
            return Response(
                {"error": "Você não pode seguir a si mesmo."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. A Lógica do Interruptor
        if me.follows.filter(id=target_profile.id).exists():
            # Se já segue, arranca da lista (Unfollow)
            me.follows.remove(target_profile)
            return Response({"message": f"Você deixou de seguir {target_user.username}"}, status=status.HTTP_200_OK)
        else:
            # Se não segue, adiciona na lista (Follow)
            me.follows.add(target_profile)
            return Response({"message": f"Você agora segue {target_user.username}"}, status=status.HTTP_200_OK)    