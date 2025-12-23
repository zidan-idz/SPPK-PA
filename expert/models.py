from django.db import models

class Symptom(models.Model):
    """
    Merepresentasikan Gejala (Fakta) yang diobservasi guru.
    Contoh: 'Sering melamun', 'Agresif terhadap teman'.
    """
    code = models.CharField(max_length=10, unique=True)  # Misal: G01
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return f"[{self.code}] {self.description}"

class Condition(models.Model):
    """
    Merepresentasikan Kondisi Psikologis (Konklusi).
    Disertai saran penanganan awal.
    """
    code = models.CharField(max_length=10, unique=True)  # Misal: P01
    name = models.CharField(max_length=100)
    suggestion = models.TextField(help_text="Saran teknis untuk Guru")
    
    def __str__(self):
        return f"[{self.code}] {self.name}"

class Rule(models.Model):
    """
    Basis Aturan untuk Forward Chaining.
    Logika: JIKA semua 'symptoms' terpenuhi, MAKA 'condition' terjadi.
    """
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    symptoms = models.ManyToManyField(Symptom)
    
    def __str__(self):
        return f"Aturan untuk {self.condition.name}"