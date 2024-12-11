"""
URL configuration for mapka project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home_view'),
    path('register/', register_view, name='register_view'),
    path('login/', login_view, name='login_view'),
    path('edit/', edit_view, name='edit_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('map/', map_view, name='map_view'),
    path('generate_users/', generate_users_view, name='generate_users_view'),
    path('remove_users/', remove_users_view, name='remove_users_view'),
    path('click_count/', click_count_view, name='click_count_view'),
    path('chart/', chart_view, name='chart_view'),
  

]
