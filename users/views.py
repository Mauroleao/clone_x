from rest_framework import generics
from .serializers import UseSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UseSerializer
    permission_classes = (AllowAny,)


