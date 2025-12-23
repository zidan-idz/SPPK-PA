from django import forms
from .models import Symptom
from students.models import Student


class DiagnosisForm(forms.Form):
    """Form untuk diagnosis dengan pilihan siswa dan gejala"""
    
    student = forms.ModelChoiceField(
        queryset=Student.objects.all().order_by('class_name', 'full_name'),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        }),
        label="Pilih Siswa",
        required=False,
        empty_label="-- Pilih Siswa (Opsional) --",
        help_text="Pilih siswa untuk menyimpan hasil diagnosis"
    )
    
    symptoms = forms.ModelMultipleChoiceField(
        queryset=Symptom.objects.all().order_by('code'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'w-4 h-4 text-blue-600 focus:ring-blue-500'
        }),
        label="Pilih Gejala yang Terlihat pada Anak",
        required=True,
        help_text="Pilih semua gejala yang Anda amati"
    )
    
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'rows': 3,
            'placeholder': 'Catatan tambahan observasi (opsional)...'
        }),
        label="Catatan Tambahan",
        required=False,
        help_text="Tambahkan catatan observasi jika diperlukan"
    )