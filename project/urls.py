"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static  # é para configurar os arquivos estáticos nas urls # noqa
from django.conf import settings # é a importação do modulo settings (from recipes import settings),  mas o recomendado é usar o django.conf # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('authors/', include('authors.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]

# configura o roteamento de urls dos arquivos de mídia no desenvolvimento
urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    ) # entender melhor essa coisa aqui
 