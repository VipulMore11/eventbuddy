from django.urls import path
from . import views

urlpatterns = [
    path('create_event/', views.create_event, name='create_event'),
    path('get_event/', views.get_events, name='get_events'),
    path('send_notifications/', views.send_notification, name='send_notification'),
]
