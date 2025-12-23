from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import DiagnosisResult
from students.models import Student
from expert.models import Symptom, Condition


@login_required
def dashboard_view(request):
    """Dashboard untuk guru melihat statistik diagnosis"""
    # Get statistics
    total_diagnoses = DiagnosisResult.objects.filter(diagnosed_by=request.user).count()
    total_students = Student.objects.filter(
        diagnoses__diagnosed_by=request.user
    ).distinct().count()
    
    # Recent diagnoses (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_diagnoses = DiagnosisResult.objects.filter(
        diagnosed_by=request.user,
        created_at__gte=week_ago
    ).count()
    
    # Most common conditions
    common_conditions = Condition.objects.filter(
        diagnosisresult__diagnosed_by=request.user
    ).annotate(
        count=Count('diagnosisresult')
    ).order_by('-count')[:5]
    
    # Latest diagnoses
    latest_diagnoses = DiagnosisResult.objects.filter(
        diagnosed_by=request.user
    ).select_related('student', 'diagnosed_by').prefetch_related('conditions')[:10]
    
    context = {
        'total_diagnoses': total_diagnoses,
        'total_students': total_students,
        'recent_diagnoses': recent_diagnoses,
        'common_conditions': common_conditions,
        'latest_diagnoses': latest_diagnoses,
    }
    
    return render(request, 'reports/dashboard.html', context)


@login_required
def diagnosis_history_view(request, student_id=None):
    """Melihat history diagnosis, bisa difilter per siswa"""
    diagnoses = DiagnosisResult.objects.filter(
        diagnosed_by=request.user
    ).select_related('student', 'diagnosed_by').prefetch_related('symptoms', 'conditions')
    
    if student_id:
        student = get_object_or_404(Student, id=student_id)
        diagnoses = diagnoses.filter(student=student)
    else:
        student = None
    
    context = {
        'diagnoses': diagnoses,
        'student': student,
    }
    
    return render(request, 'reports/history.html', context)


@login_required
def diagnosis_detail_view(request, diagnosis_id):
    """Detail dari satu diagnosis"""
    diagnosis = get_object_or_404(
        DiagnosisResult.objects.select_related('student', 'diagnosed_by').prefetch_related('symptoms', 'conditions'),
        id=diagnosis_id,
        diagnosed_by=request.user
    )
    
    context = {
        'diagnosis': diagnosis,
    }
    
    return render(request, 'reports/detail.html', context)
