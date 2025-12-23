from django.db import models
from django.contrib.auth.models import User
from students.models import Student
from expert.models import Symptom, Condition


class DiagnosisResult(models.Model):
    """
    Menyimpan history hasil diagnosis untuk tracking dan laporan.
    """
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE,
        related_name='diagnoses',
        verbose_name='Siswa'
    )
    diagnosed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='diagnoses_made',
        verbose_name='Didiagnosis oleh'
    )
    symptoms = models.ManyToManyField(
        Symptom,
        verbose_name='Gejala yang Dipilih'
    )
    conditions = models.ManyToManyField(
        Condition,
        verbose_name='Kondisi Terdeteksi',
        blank=True
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Catatan Tambahan',
        help_text='Catatan observasi guru'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Tanggal Diagnosis'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Terakhir Diupdate'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Hasil Diagnosis'
        verbose_name_plural = 'Hasil Diagnosis'
    
    def __str__(self):
        return f"Diagnosis {self.student.full_name} - {self.created_at.strftime('%d/%m/%Y')}"
    
    def get_conditions_summary(self):
        """Return comma-separated list of detected conditions"""
        return ", ".join([c.name for c in self.conditions.all()])
    
    def get_symptoms_summary(self):
        """Return comma-separated list of symptoms"""
        return ", ".join([s.description for s in self.symptoms.all()])
