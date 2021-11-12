from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='learn-home'),
]