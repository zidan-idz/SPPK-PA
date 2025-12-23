from django.core.management.base import BaseCommand
from expert.models import Symptom, Condition, Rule


class Command(BaseCommand):
    help = 'Load sample data untuk sistem pakar'

    def handle(self, *args, **kwargs):
        self.stdout.write('Memulai loading sample data...')
        
        # Clear existing data
        Rule.objects.all().delete()
        Condition.objects.all().delete()
        Symptom.objects.all().delete()
        
        # Create Symptoms (Gejala)
        symptoms_data = [
            # Gejala Kecemasan
            ('G01', 'Sering terlihat gelisah atau cemas tanpa alasan jelas'),
            ('G02', 'Menghindari interaksi sosial dengan teman sebaya'),
            ('G03', 'Sering mengeluh sakit perut atau sakit kepala tanpa penyebab medis'),
            ('G04', 'Sulit berkonsentrasi dalam belajar'),
            ('G05', 'Mudah terkejut atau takut berlebihan'),
            
            # Gejala Depresi
            ('G06', 'Terlihat sedih atau murung berkepanjangan'),
            ('G07', 'Kehilangan minat pada aktivitas yang biasanya disukai'),
            ('G08', 'Perubahan pola tidur (terlalu banyak atau terlalu sedikit)'),
            ('G09', 'Perubahan nafsu makan signifikan'),
            ('G10', 'Sering mengatakan hal-hal negatif tentang diri sendiri'),
            
            # Gejala ADHD
            ('G11', 'Tidak bisa duduk diam, selalu bergerak'),
            ('G12', 'Sering mengganggu teman saat belajar'),
            ('G13', 'Kesulitan mengikuti instruksi'),
            ('G14', 'Sering kehilangan barang-barang pribadi'),
            ('G15', 'Berbicara berlebihan, sulit menunggu giliran'),
            
            # Gejala Gangguan Perilaku
            ('G16', 'Sering berkelahi atau agresif terhadap teman'),
            ('G17', 'Tidak mematuhi aturan sekolah secara konsisten'),
            ('G18', 'Merusak barang milik orang lain dengan sengaja'),
            ('G19', 'Berbohong atau mencuri'),
            ('G20', 'Tidak menunjukkan penyesalan setelah berbuat salah'),
        ]
        
        symptoms = {}
        for code, desc in symptoms_data:
            symptom = Symptom.objects.create(code=code, description=desc)
            symptoms[code] = symptom
            self.stdout.write(f'  ✓ Created symptom: {code}')
        
        # Create Conditions (Kondisi Psikologis)
        conditions_data = [
            (
                'P01',
                'Kecemasan Sosial',
                'Konsultasikan dengan psikolog sekolah untuk assessment lebih lanjut. '
                'Berikan dukungan emosional dan ciptakan lingkungan kelas yang aman dan mendukung. '
                'Hindari memaksa anak untuk berinteraksi sosial secara mendadak. '
                'Libatkan orang tua dalam proses penanganan. '
                'Pertimbangkan untuk memberikan tugas kelompok dengan teman yang sudah dekat terlebih dahulu.'
            ),
            (
                'P02',
                'Indikasi Depresi Ringan',
                'SEGERA rujuk ke psikolog atau konselor profesional untuk evaluasi menyeluruh. '
                'Pantau perubahan perilaku secara ketat dan dokumentasikan. '
                'Libatkan orang tua/wali dengan segera. '
                'Ciptakan suasana kelas yang supportif dan hindari kritik berlebihan. '
                'Berikan perhatian khusus namun tidak berlebihan. '
                'Jika ada indikasi self-harm, segera hubungi profesional kesehatan mental.'
            ),
            (
                'P03',
                'Kemungkinan ADHD (Attention Deficit Hyperactivity Disorder)',
                'Rujuk ke psikolog untuk assessment dan diagnosis formal. '
                'Berikan instruksi yang jelas, singkat, dan terstruktur. '
                'Gunakan metode pembelajaran yang interaktif dan melibatkan gerakan. '
                'Berikan break time yang cukup. '
                'Koordinasi dengan orang tua untuk konsistensi penanganan di rumah dan sekolah. '
                'Pertimbangkan modifikasi lingkungan belajar (misal: duduk di depan, jauh dari distraksi).'
            ),
            (
                'P04',
                'Gangguan Perilaku (Conduct Disorder)',
                'SEGERA rujuk ke psikolog atau psikiater anak. '
                'Dokumentasikan semua insiden perilaku bermasalah. '
                'Libatkan orang tua dan jika perlu, pihak berwenang. '
                'Terapkan konsekuensi yang konsisten dan adil. '
                'Berikan reinforcement positif untuk perilaku baik. '
                'Pertimbangkan konseling keluarga. '
                'Pastikan keamanan anak lain di kelas.'
            ),
            (
                'P05',
                'Kecemasan Umum',
                'Konsultasikan dengan konselor sekolah. '
                'Ajarkan teknik relaksasi sederhana (breathing exercises). '
                'Berikan struktur dan rutinitas yang jelas. '
                'Hindari situasi yang terlalu menekan. '
                'Libatkan orang tua untuk dukungan di rumah. '
                'Monitor perkembangan secara berkala.'
            ),
        ]
        
        conditions = {}
        for code, name, suggestion in conditions_data:
            condition = Condition.objects.create(
                code=code,
                name=name,
                suggestion=suggestion
            )
            conditions[code] = condition
            self.stdout.write(f'  ✓ Created condition: {code} - {name}')
        
        # Create Rules (Aturan)
        rules_data = [
            ('P01', ['G01', 'G02', 'G03']),  # Kecemasan Sosial
            ('P02', ['G06', 'G07', 'G08', 'G09']),  # Depresi
            ('P03', ['G11', 'G12', 'G13', 'G14']),  # ADHD
            ('P04', ['G16', 'G17', 'G18', 'G19']),  # Gangguan Perilaku
            ('P05', ['G01', 'G04', 'G05']),  # Kecemasan Umum
            
            # Rules dengan kombinasi berbeda
            ('P02', ['G06', 'G10', 'G08']),  # Depresi (alternatif)
            ('P03', ['G11', 'G15', 'G13']),  # ADHD (alternatif)
        ]
        
        for condition_code, symptom_codes in rules_data:
            rule = Rule.objects.create(condition=conditions[condition_code])
            for symptom_code in symptom_codes:
                rule.symptoms.add(symptoms[symptom_code])
            rule.save()
            self.stdout.write(f'  ✓ Created rule: IF {", ".join(symptom_codes)} THEN {condition_code}')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Berhasil membuat:'))
        self.stdout.write(self.style.SUCCESS(f'   - {len(symptoms_data)} gejala'))
        self.stdout.write(self.style.SUCCESS(f'   - {len(conditions_data)} kondisi'))
        self.stdout.write(self.style.SUCCESS(f'   - {len(rules_data)} aturan'))
