from django.urls import path
from .views import PostListCreateView, ToggleLikePostView, CommentListCreateView, CommentDetailView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post_list_create'),
    path('<int:id>/like/', ToggleLikePostView.as_view(), name='toggle_like_post'),
    path('<int:post_id>/respostas/', CommentListCreateView.as_view(), name='comment_list_create'),
    path('respostas/<int:id>/', CommentDetailView.as_view(), name='comment_delete'),
]