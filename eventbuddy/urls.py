from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('Authentication.urls')),
    path('chat/', include('Chat.urls')),
    path('event/', include('Event.urls')),

]
