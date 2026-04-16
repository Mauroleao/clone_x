from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    photo = serializers.ImageField(source='profile.photo', required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'photo')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

    
    def update(self, instance, validated_data):
        
        profile_data = validated_data.pop('profile', {})
        
        
        instance = super().update(instance, validated_data)
        
        if profile_data:
            profile = instance.profile
            if 'photo' in profile_data:
                profile.photo = profile_data['photo']
            profile.save()
            
        return instance