from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'photo', 'photo_url', 'bio']

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url
        return None

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile']

    def validate_username(self, value):
        """Validar se username já existe"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuário já existe.")
        return value
    
    def validate_email(self, value):
        """Validar se email já existe"""
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está registrado.")
        return value
    
    def validate_password(self, value):
        """Validar senha"""
        if len(value) < 6:
            raise serializers.ValidationError("Senha deve ter pelo menos 6 caracteres.")
        return value

    def create(self, validated_data):
        """Criar usuário com melhor tratamento de erro"""
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data.get('email', ''),
                password=validated_data['password']
            )
            return user
        except Exception as e:
            print(f"Erro ao criar usuário: {str(e)}")
            import traceback
            traceback.print_exc()
            raise serializers.ValidationError(f"Erro ao criar usuário: {str(e)}")

class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        
        if 'bio' in self.initial_data:
            instance.profile.bio = self.initial_data['bio']
            instance.profile.save()
        
        return instance