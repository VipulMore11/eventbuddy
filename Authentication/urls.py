from django.urls import path
from .views import *

app_name = 'Authentication'

urlpatterns = [
    path('register/organiser/', register_organiser_view, name='register_organiser'),
    path('register/staff/', register_staff_view, name='register_staff'),
    path('login/', login_view, name='login'),
    path('profile/', get_profile_view, name='get_profile_view'),
]
