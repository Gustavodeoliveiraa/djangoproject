from django.urls import path
from . import views
from .view import DashboardRecipe, DashboardRecipeDelete

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('Logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'dashboard/recipe/new/',
        DashboardRecipe.as_view(), name='dashboard_recipe_new'
        ),
    path(
        'dashboard/recipe/delete/', DashboardRecipeDelete.as_view(),
        name='dashboard_recipe_delete'
        ),
    path(
        'dashboard/recipe/<int:id>/edit/', DashboardRecipe.as_view(),
        name='dashboard_recipe_edit'
        ),

]
