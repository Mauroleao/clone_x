from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # Campo calculado que não existe no banco, mas aparecerá no JSON
    likes_count = serializers.SerializerMethodField()
    # Para mostrar o nome do autor em vez de apenas o ID no feed
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'content', 'image', 'created_at', 'likes_count']
        read_only_fields = ['author', 'created_at']

    # Lógica para o campo likes_count
    def get_likes_count(self, obj):
        return obj.likes.count()