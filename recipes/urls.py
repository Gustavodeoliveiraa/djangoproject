from django.urls import path
from . import views

urlpatterns = [
    path('',  views.home, name="recipe-home"), # Passa o caminho(url) e uma função que vai ser executada # noqa
    path('recipes/<int:id>/',  views.recipe, name="recipes-recipe")
]
