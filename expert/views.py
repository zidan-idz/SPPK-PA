from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import DiagnosisForm
from .services import InferenceEngine
from students.models import Student
from reports.models import DiagnosisResult


@login_required
def diagnose_view(request, student_id=None):
    """
    View untuk melakukan diagnosis.
    Bisa dipanggil dengan student_id untuk diagnosis langsung ke siswa tertentu.
    """
    results = None
    student = None
    
    if student_id:
        student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = DiagnosisForm(request.POST)
        if form.is_valid():
            # 1. Ambil data gejala yang dipilih user
            selected_symptoms = form.cleaned_data['symptoms']
            symptom_ids = [s.id for s in selected_symptoms]
            
            # 2. Ambil student jika ada
            if 'student' in form.cleaned_data and form.cleaned_data['student']:
                student = form.cleaned_data['student']
            
            # 3. Panggil Inference Engine (Business Logic)
            engine = InferenceEngine()
            results = engine.diagnose(symptom_ids)
            
            # 4. Simpan hasil diagnosis SELALU jika ada student (bahkan jika tidak ada kondisi terdeteksi)
            if student:
                diagnosis = DiagnosisResult.objects.create(
                    student=student,
                    diagnosed_by=request.user
                )
                diagnosis.symptoms.set(selected_symptoms)
                
                # Set conditions jika ada hasil
                if results:
                    diagnosis.conditions.set(results)
                
                # Tambahkan notes jika ada
                if 'notes' in form.cleaned_data and form.cleaned_data['notes']:
                    diagnosis.notes = form.cleaned_data['notes']
                    diagnosis.save()
                
                if results:
                    messages.success(
                        request, 
                        f'Ditemukan {len(results)} kondisi untuk {student.full_name}. Hasil telah disimpan.'
                    )
                else:
                    messages.info(
                        request,
                        f'Tidak ditemukan kondisi spesifik untuk {student.full_name}. Hasil tetap disimpan untuk dokumentasi.'
                    )
            elif not student:
                messages.info(
                    request,
                    'Hasil diagnosis tidak disimpan karena tidak ada siswa yang dipilih. '
                    'Pilih siswa untuk menyimpan hasil diagnosis.'
                )
            
    else:
        # Pre-fill student jika ada
        initial = {}
        if student:
            initial['student'] = student
        form = DiagnosisForm(initial=initial)

    return render(request, 'expert/diagnose.html', {
        'form': form,
        'results': results,
        'student': student,
    })


@login_required
def student_list_view(request):
    """Menampilkan daftar siswa untuk dipilih untuk diagnosis"""
    students = Student.objects.all().order_by('class_name', 'full_name')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(full_name__icontains=search_query) |
            Q(nis__icontains=search_query) |
            Q(class_name__icontains=search_query)
        )
    
    context = {
        'students': students,
        'search_query': search_query,
    }
    
    return render(request, 'expert/student_list.html', context)