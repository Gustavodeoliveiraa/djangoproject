from django.urls import path
from . import views

# recipes:recipe
app_name = 'recipes'

urlpatterns = [
    path('',  views.home, name="home"), # Passa o caminho(url) e uma função que vai ser executada # noqa
    path('recipes/category/<int:category_id>/',  views.category, name="category"), # noqa

    path('recipes/<int:id>/',  views.recipe, name="recipe")
]

