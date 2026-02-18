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
    path('reporting/', views.reporting, name='reporting'),
    path('user-management/', views.user_management, name='user_management'),
    path('get_ticket_status/', views.get_ticket_status, name='get_ticket_status'),  # The endpoint for auto-refresh
    re_path(r'^history/(?P<ticket_id>[0-9]+)/$',views.ticket_history,name="ticket_history"),
    re_path(r'^delete/(?P<input>[0-9]+)/$',views.delete_ticket,name="delete_ticket"),
    re_path(r'^showhistory/(?P<ticketId>[0-9]+)/$',views.showHistory,name="showHistory"),
    path('update-user-role/', views.update_user_role, name='update_user_role'),
    path('delete-user/', views.delete_user, name='delete_user'),
    path('edit-user/', views.edit_user, name='edit_user'),
    path('toggle-user-status/', views.toggle_user_status, name='toggle_user_status'),
    path('categories/', views.category_management, name='category_management'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)