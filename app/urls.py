from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('interview_python', views.execute_python_code, name="execute_python_code"),
    path('interview_java', views.execute_java_code, name="execute_java_code"),
    path('feedback', views.feedback_result, name="feedback_display"),
    
]