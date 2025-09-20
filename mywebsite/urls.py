'''
URL configuration for mywebsite project.

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
'''
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomPasswordChangeView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('index/',views.index,name='index'),
    path('admin/', admin.site.urls, name='admin'),
    path('register/', views.register, name='register'),
    path('accounts/', include('allauth.urls')),
    #path('go-to-google-login/', views.google_redirect, name='google_redirect'),
    #path('login/google/', views.google_login_redirect, name='google_login_redirect'),
    path("verify/<uidb64>/<token>/", views.verify_email, name="verify_email"),
    path('login/', views.custom_login, name='login'),
    path('blog/',include(('blog.urls','blog'),namespace='blog')),
    path('about/',include(('about.urls','about'),namespace='about')),
    path('logout/', views.logout_view, name='logout'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='password_change'),
]