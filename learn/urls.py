from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.home, name='learn-home'),
    path('profile/', views.profile, name='profile'),
    path('upload-file/', views.upload_file, name='upload-file'),
    path('create-activity/<int:id>', views.create_activity, name='create-activity'),
    path('deploy-activity/<int:id>', views.deploy_activity, name='deploy-activity'),
    path('download-file/<path:path>', views.download_file, name='download-file'),
    path('delete-file/<int:id>', views.delete_file, name='remove-file'),
    path('delete-question/<int:mode>/<int:id>', views.delete_question, name='deletequestion'),
    path('delete-activity/<int:id>', views.delete_activity, name='remove-activity'),
    path('view-subject-student/<int:id>/', views.view_subject, name='view-subject-student'),
    path('view-subject-teacher/<int:id>/', views.view_subject, name='view-subject-teacher'),
    path('answer-activity/<int:id>/', views.answer_activity, name='answer-activity'),
    path('question-and-answer-submit/<int:id>/<int:total>/', views.question_and_answer_submit, name='question-and-answer-submit'),
    path('evaluate/<int:activity>/<int:user>/', views.evaluate, name='evaluate'),
    path('delete-image/<int:id>/', views.delete_image, name='delete-image'),
    path('download-csv/<str:id>/', views.download_csv, name='download-csv')
]

