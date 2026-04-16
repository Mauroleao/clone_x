from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    # Campo para foto do post. null=True e blank=True permitem posts só com texto.
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)

    class Meta:
        ordering = ['-created_at'] 

    def __str__(self):
        return f"Post de {self.author.username}"