from django.urls import path
from . import views

app_name = 'expert'

urlpatterns = [
    path('check/', views.diagnose_view, name='diagnose'),
    path('check/<int:student_id>/', views.diagnose_view, name='diagnose_student'),
    path('students/', views.student_list_view, name='student_list'),
]