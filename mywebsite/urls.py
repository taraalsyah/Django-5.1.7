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
from .views import CustomPasswordChangeView, unlink_social
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect

handler400 = "mywebsite.views.error_400"

urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('index/',views.index,name='index'),
    path('admin/', admin.site.urls, name='admin'),
    path('register/', views.register, name='register'),
    path('accounts/', include('allauth.urls')),
    path("accounts/unlink/<int:pk>/", unlink_social, name="unlink_social"),
    #path("unlink-google/", views.unlink_google, name="unlink_google"),
    #path('go-to-google-login/', views.google_redirect, name='google_redirect'),
    #path('login/google/', views.google_login_redirect, name='google_login_redirect'),
    path("verify/<uidb64>/<token>/", views.verify_email, name="verify_email"),
    path('login/', views.custom_login, name='login'),
    path('blog/',include(('blog.urls','blog'),namespace='blog')),
    path('',include(('about.urls','about'),namespace='about')),
    path('ticket/',include(('ticket.urls','ticket'),namespace='ticket')),
    path('logout/', views.logout_view, name='logout'),
    path('security/', views.security_view, name='security'),
    path('profile/', views.profile_view, name='profile'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('verify/<str:uid>/<str:token>/', views.verify_account, name='verify_account'),
    path('verify-success/', views.verify_success, name='verify_success'),
    path('verify-failed/', views.verify_failed, name='verify_failed'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    path("check-ip/", views.check_ip, name='check-ip'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)