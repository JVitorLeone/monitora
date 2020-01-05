"""siteMonitora URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from users import views as user_views
from produtos import views as produto_views
from django.views.generic import TemplateView

urlpatterns = [
    path('', produto_views.index, name='index'),
    path('produto/', include('produtos.urls')),
    path('login/', user_views.entrar, name='entrar'),
    path('cadastro/', user_views.cadastrar, name='cadastrar'),
    path('logout/', user_views.sair, name="sair"), 
    path('painel/', include('users.urls')), 
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

