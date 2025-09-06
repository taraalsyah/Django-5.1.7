from django.urls import path,re_path

from . import views

urlpatterns = [
    re_path(r'^(?P<update_id>[0-9]+)/$',views.update,name="update"),
    re_path(r'^delete/(?P<input>[0-9]+)/$',views.delete,name="delete"),
    #re_path(r'^(?P<sluginput>[\w-]+)/$',views.slugpost),
    path('download/posts/', views.download_posts_csv, name='download_posts_csv'),
    path('create/',views.create,name="create"),
    path('ajax/load-cities/', views.create, name='ajax_load_cities'),
    path('',views.index,name="index"),
]