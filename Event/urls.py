from django.urls import path
from . import views

urlpatterns = [
    path('create_event/', views.create_event, name='create_event'),
    path('get_event/', views.get_events, name='get_events'),
    path('send_notifications/', views.send_notification, name='send_notification'),
    path('create_tasks/', views.create_task, name='create_task'),
    path('get_task_org/', views.get_all_tasks, name='get_all_tasks'),
    path('get_task_staff/', views.get_all_staff_tasks, name='get_all_staff_tasks'),
    path('get_all_staff/', views.get_all_staff, name='get_all_staff'),
    path('get_all_notifications/', views.get_notifications, name='get_notifications'),
    path('is_seen/', views.is_seen, name='is_seen'),
    path('staff_task/', views.staff_task, name='staff_task'),
]
