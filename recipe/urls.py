from django.urls import path
from . import views
app_name = 'recipe'
urlpatterns = [
    path('', views.recipe_list, name='recipe-list'),
    path('create/', views.recipe_create, name='recipe-create'),
    path('<int:pk>/', views.recipe_detail, name='recipe-detail'),
    path('<int:pk>/like/', views.recipe_like, name='recipe-like'),
]
