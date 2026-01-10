from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'ticket'

urlpatterns = [
    path('', views.index, name='ticket_index'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('update/', views.update, name='update'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('get_ticket_status/', views.get_ticket_status, name='get_ticket_status'),  # The endpoint for auto-refresh
    re_path(r'^history/(?P<ticket_id>[0-9]+)/$',views.ticket_history,name="ticket_history"),
    re_path(r'^delete/(?P<input>[0-9]+)/$',views.delete_ticket,name="delete_ticket"),
    re_path(r'^showhistory/(?P<ticketId>[0-9]+)/$',views.showHistory,name="showHistory"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)