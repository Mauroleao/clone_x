from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    author_photo = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_username', 'author_photo', 'content', 'created_at']
        read_only_fields = ['author', 'created_at']

    def get_author_photo(self, obj):
        if hasattr(obj.author, 'profile') and obj.author.profile.photo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.author.profile.photo.url) if request else obj.author.profile.photo.url
        return None

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    author_photo = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'author_photo', 'content', 'image', 'created_at', 'likes_count', 'comments', 'comments_count']
        read_only_fields = ['author', 'created_at']

    def get_author_photo(self, obj):
        if hasattr(obj.author, 'profile') and obj.author.profile.photo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.author.profile.photo.url) if request else obj.author.profile.photo.url
        return None

    def get_likes_count(self, obj):
        return obj.likes.count() if hasattr(obj, 'likes') else 0

    def get_comments_count(self, obj):
        return obj.comments.count() if hasattr(obj, 'comments') else 0