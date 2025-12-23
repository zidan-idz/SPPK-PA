from django.contrib import admin
from .models import DiagnosisResult


@admin.register(DiagnosisResult)
class DiagnosisResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'diagnosed_by', 'created_at', 'get_conditions_count']
    list_filter = ['created_at', 'diagnosed_by']
    search_fields = ['student__full_name', 'student__nis', 'notes']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['symptoms', 'conditions']
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('student', 'diagnosed_by')
        }),
        ('Hasil Diagnosis', {
            'fields': ('symptoms', 'conditions', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_conditions_count(self, obj):
        return obj.conditions.count()
    get_conditions_count.short_description = 'Jumlah Kondisi'
