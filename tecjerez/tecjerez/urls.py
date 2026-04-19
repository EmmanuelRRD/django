"""
URL configuration for tecjerez project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.views.generic import TemplateView
from escolares.views import *

urlpatterns = [
    
    #panel de admin
    path('admin/', admin.site.urls),
    #Landin
    path('', TemplateView.as_view(template_name="lp.html"), name='inicio'),
    # Alumnos
    path('alumnos/', TemplateView.as_view(template_name="alumnos/index.html"), name='listar'),
    
    # Se manda la peticion a la api
    path('api/alumnos/', api_alumnos),
    path('api/alumnos/<int:pk>/', api_alumno_detalle),
    path('api/login/', api_login, name='api_login'),
    path('api/registro/', api_registro, name='api_registro'),
]

