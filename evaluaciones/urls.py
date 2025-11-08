"""
URL configuration for evaluaciones project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from reg_notas.views_front import (crear_nota, mostrar_notas, 
                                   lista_notas, filtrar_notas, filtrar_notas_avanzado)
from reg_notas.views_api import (api_filtrar_notas, api_crear_nota)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('reg_notas.urls_api')),
    path('api-auth/', include('rest_framework.urls')),
    path('formulario/', crear_nota, name='crear_nota'),
    path('ver-notas/', mostrar_notas, name='ver_notas'),
    path('pregunta1/', lista_notas, name='pregunta1'),
    path('pregunta2/', filtrar_notas, name='filtrar_notas'),
    path('pregunta3/', filtrar_notas_avanzado, name = 'filtrar_avanzado'),
    path('api/notasfiltro/', api_filtrar_notas, name="api_filtrar_notas"),
    path('api/notas_crear/', api_crear_nota, name='api_crear_nota'),
    
]
