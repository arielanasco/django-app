from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='learn-home'),
    path('profile/', views.profile, name='profile'),
    path('upload/', views.upload_file, name='upload-file'),
    path('activity/', views.create_activity, name='create-activity'),
    path('view/', views.view_subject, name='view-subject'),


]