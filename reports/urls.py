from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('history/', views.diagnosis_history_view, name='history'),
    path('history/student/<int:student_id>/', views.diagnosis_history_view, name='history_student'),
    path('detail/<int:diagnosis_id>/', views.diagnosis_detail_view, name='detail'),
]
