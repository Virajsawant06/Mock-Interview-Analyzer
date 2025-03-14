from django.contrib import admin
from django.urls import path, include
from django.urls import path
from core.views import detect_emotion
from django.urls import path
from core.views import QuestionListView

urlpatterns = [
    path("api/questions/", QuestionListView.as_view(), name="question_list"),
    path("api/emotion/", detect_emotion, name="detect_emotion"),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]