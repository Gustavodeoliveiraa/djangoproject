from django.urls import path
from recipes.views import home

urlpatterns = [
    path('',  home), # Passa o caminho(url) e uma função que vai ser executada # noqa

]
