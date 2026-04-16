from django.urls import path
# Não esqueça de adicionar a ToggleLikePostView na importação!
from .views import PostListCreateView, ToggleLikePostView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post_list_create'),
    
    # A nossa nova rota do botão de curtir
    path('<int:id>/like/', ToggleLikePostView.as_view(), name='toggle_like_post'),
]