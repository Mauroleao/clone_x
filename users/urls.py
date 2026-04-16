from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView, UserProfileView, FollowUserView 

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('<int:id>/follow/', FollowUserView.as_view(), name='follow_user'),
]