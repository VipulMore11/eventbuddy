from django.urls import path
from . import views

urlpatterns = [
    path('chatrooms/', views.user_chatrooms, name='user_chatrooms'),
    path('chatrooms/c/', views.create_chatroom, name='create_chatroom'),
    path('chatrooms/<int:room_id>/messages/', views.list_messages, name='list_messages'),
    path('chatrooms/<int:room_id>/messages/create/', views.create_message, name='create_message'),
]
