from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='learn-home'),
    path('profile/', views.profile, name='profile'),
    path('upload-file/', views.upload_file, name='upload-file'),
    path('create-activity/', views.create_activity, name='create-activity'),
    path('download-file/<path:path>', views.download_file, name='downloadfile'),
    path('remove-file/<int:id>', views.delete_file, name='remove-file'),
    path('view-subject-student/<int:id>/', views.view_subject, name='view-subject-student'),
    path('view-subject-teacher/<int:id>/', views.view_subject, name='view-subject-teacher'),


]

