from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Main interview interface
    path('', views.IndexView.as_view(), name='index'),
    path('interview/', views.InterviewView.as_view(), name='interview'),
    path('interview/start/', views.StartInterviewView.as_view(), name='start_interview'),
    path('interview/end/', views.EndInterviewView.as_view(), name='end_interview'),
    
    # API endpoints for real-time interaction
    path('api/emotion/start/', views.StartEmotionDetectionView.as_view(), name='start_emotion'),
    path('api/emotion/stop/', views.StopEmotionDetectionView.as_view(), name='stop_emotion'),
    path('api/answer/verify/', views.VerifyAnswerView.as_view(), name='verify_answer'),
    path('api/emotion/', views.StartEmotionDetectionView.as_view(), name='detect_emotion'),
    
    # Results and reports
    path('results/<str:session_id>/', views.ResultsView.as_view(), name='results'),
    path('report/<str:session_id>/', views.ReportView.as_view(), name='report'),
    path('report/<str:session_id>/download/', views.DownloadReportView.as_view(), name='download_report'),
    
    # Question management
    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('questions/add/', views.AddQuestionView.as_view(), name='add_question'),
    path('questions/<str:question_id>/edit/', views.EditQuestionView.as_view(), name='edit_question'),
    path('questions/<str:question_id>/delete/', views.DeleteQuestionView.as_view(), name='delete_question'),
]
