from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView, UserProfileView, FollowUserView, ChangePasswordView, DebugView, LoginView

urlpatterns = [
    path('debug/', DebugView.as_view(), name='debug'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user_profile_detail'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('<int:id>/follow/', FollowUserView.as_view(), name='follow_user'),
    path('follow/<str:username>/', FollowUserView.as_view(), name='follow_user'),
]