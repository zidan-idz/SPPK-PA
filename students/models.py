from django.db import models

class Student(models.Model):
    """
    Data siswa yang akan dinilai kondisi psikologisnya.
    """
    nis = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    # Gunakan DateField untuk umur yang akurat, atau IntegerField untuk simpel
    date_of_birth = models.DateField() 
    gender_choices = [('L', 'Laki-laki'), ('P', 'Perempuan')]
    gender = models.CharField(max_length=1, choices=gender_choices)
    class_name = models.CharField(max_length=20) # Misal: 10 IPA 1

    def __str__(self):
        return f"{self.full_name} ({self.class_name})"