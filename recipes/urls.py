from django.urls import path
from . import views

# recipes:recipe
app_name = 'recipes'

urlpatterns = [
    path('',  views.Home.as_view(), name="home"), # Passa o caminho(url) e uma função que vai ser executada # noqa
    path('recipes/search/', views.Search.as_view(), name='search'), # noqa
    path('recipes/category/<int:category_id>/',  views.Category.as_view(), name="category"), # noqa
    path('recipes/<int:pk>/',  views.RecipeDetail.as_view(), name="recipe"),

    path('recipes/api/v1/',  views.RecipeListViewHomeApi.as_view(), name="recipe_api_v1"),


    path('recipes/api/v1/<int:pk>/',  views.RecipeDetailApi.as_view(), name="recipe_api_v1_detail"),
]
