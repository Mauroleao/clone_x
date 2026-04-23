from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    bio = models.CharField(max_length=160, blank=True, default='')

    def __str__(self):
        return f"Perfil de {self.user.username}"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Sinal para criar um Profile quando um novo usuário é criado
    Otimizado para evitar queries extras durante autenticação
    """
    try:
        if created:
            # Usuário novo - criar Profile uma única vez
            Profile.objects.create(user=instance)
    except Exception as e:
        # Log do erro para debugging
        print(f"Erro ao criar Profile para usuário {instance.username}: {str(e)}")
        import traceback
        traceback.print_exc()

class Follow(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f"{self.user.username} segue {self.followed_user.username}"