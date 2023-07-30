from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
app_name = 'users'
urlpatterns = [
    path('register/', views.user_registration,
         name="create-user"),
    path('login/', views.user_login, name="login-user"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', views.user_logout, name='logout-user'),
    path('', views.user_profile, name='user-info'),
    path('profile/', views.user_profile_update,
         name='user-profile'),
    path('profile/avatar/', views.user_avatar,
         name='user-avatar'),
    path('profile/<int:pk>/bookmarks/', views.user_bookmarks,
         name='user-bookmark'),
    path('password/change/', views.password_change,
         name='change-password'),
]
