from django.core.management.base import BaseCommand
from students.models import Student
from datetime import date


class Command(BaseCommand):
    help = 'Load sample student data untuk testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Memulai loading sample students...')
        
        # Clear existing students
        Student.objects.all().delete()
        
        # Create sample students
        students_data = [
            ('2024001', 'Ahmad Rizki Pratama', date(2012, 3, 15), 'L', '10 IPA 1'),
            ('2024002', 'Siti Nurhaliza', date(2012, 7, 22), 'P', '10 IPA 1'),
            ('2024003', 'Budi Santoso', date(2012, 1, 8), 'L', '10 IPA 2'),
            ('2024004', 'Dewi Lestari', date(2012, 11, 30), 'P', '10 IPA 2'),
            ('2024005', 'Eko Prasetyo', date(2012, 5, 17), 'L', '10 IPS 1'),
            ('2024006', 'Fitri Handayani', date(2012, 9, 25), 'P', '10 IPS 1'),
            ('2024007', 'Gilang Ramadan', date(2012, 2, 14), 'L', '10 IPS 2'),
            ('2024008', 'Hana Safitri', date(2012, 8, 19), 'P', '10 IPS 2'),
            ('2024009', 'Irfan Hakim', date(2012, 4, 11), 'L', '11 IPA 1'),
            ('2024010', 'Jasmine Putri', date(2011, 12, 5), 'P', '11 IPA 1'),
        ]
        
        for nis, name, dob, gender, class_name in students_data:
            student = Student.objects.create(
                nis=nis,
                full_name=name,
                date_of_birth=dob,
                gender=gender,
                class_name=class_name
            )
            self.stdout.write(f'  ✓ Created student: {nis} - {name}')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Berhasil membuat {len(students_data)} siswa'))
