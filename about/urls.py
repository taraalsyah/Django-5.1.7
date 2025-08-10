from django.urls import path,re_path
from . import views
from .views import IndexClassView,Template,Createview,Updateview,Listview,Ubsi

urlpatterns = [
    re_path(r'^listview/(?P<page>[0-9]+)$',Listview.as_view(),name='listview'),
    re_path(r'^update/(?P<pk>[0-9]+)$',Updateview.as_view()),
    re_path(r'^template/(?P<parameter>[0-9]+)$',Template.as_view()),
    re_path(r'^class2/',IndexClassView.as_view(template_name='about/templates/about/index2.html'),name='class-index2'),
    re_path(r'^createview',Createview.as_view(),name='create'),
    re_path(r'^ubsi',Ubsi.as_view(),name='ubsi'),
    path('',IndexClassView.as_view(),name='index'),
]