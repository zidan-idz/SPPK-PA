from django.core.management.base import BaseCommand
from expert.models import Rule, Symptom, Condition
from expert.services import InferenceEngine


class Command(BaseCommand):
    help = 'Debug dan test inference engine'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('\n=== DEBUG INFERENCE ENGINE ===\n'))
        
        # 1. Tampilkan semua rules
        rules = Rule.objects.prefetch_related('symptoms', 'condition').all()
        self.stdout.write(f'Total Rules: {rules.count()}\n')
        
        for i, rule in enumerate(rules, 1):
            symptom_codes = list(rule.symptoms.values_list('code', flat=True))
            self.stdout.write(
                f'Rule {i}: IF {symptom_codes} THEN {rule.condition.code} ({rule.condition.name})'
            )
        
        # 2. Test case 1: Kecemasan Sosial
        self.stdout.write(self.style.WARNING('\n\n=== TEST CASE 1: Kecemasan Sosial ==='))
        test_symptoms_1 = ['G01', 'G02', 'G03']
        self.stdout.write(f'Input symptoms: {test_symptoms_1}')
        
        symptom_ids_1 = list(Symptom.objects.filter(code__in=test_symptoms_1).values_list('id', flat=True))
        self.stdout.write(f'Symptom IDs: {symptom_ids_1}')
        
        engine = InferenceEngine()
        results_1 = engine.diagnose(symptom_ids_1)
        
        if results_1:
            self.stdout.write(self.style.SUCCESS(f'✓ Detected {len(results_1)} condition(s):'))
            for cond in results_1:
                self.stdout.write(f'  - {cond.code}: {cond.name}')
        else:
            self.stdout.write(self.style.ERROR('✗ No conditions detected'))
        
        # 3. Test case 2: ADHD
        self.stdout.write(self.style.WARNING('\n\n=== TEST CASE 2: ADHD ==='))
        test_symptoms_2 = ['G11', 'G12', 'G13', 'G14']
        self.stdout.write(f'Input symptoms: {test_symptoms_2}')
        
        symptom_ids_2 = list(Symptom.objects.filter(code__in=test_symptoms_2).values_list('id', flat=True))
        self.stdout.write(f'Symptom IDs: {symptom_ids_2}')
        
        results_2 = engine.diagnose(symptom_ids_2)
        
        if results_2:
            self.stdout.write(self.style.SUCCESS(f'✓ Detected {len(results_2)} condition(s):'))
            for cond in results_2:
                self.stdout.write(f'  - {cond.code}: {cond.name}')
        else:
            self.stdout.write(self.style.ERROR('✗ No conditions detected'))
        
        # 4. Tampilkan semua symptoms
        self.stdout.write(self.style.WARNING('\n\n=== ALL SYMPTOMS ==='))
        symptoms = Symptom.objects.all().order_by('code')
        for symptom in symptoms:
            self.stdout.write(f'{symptom.code}: {symptom.description}')
        
        self.stdout.write(self.style.SUCCESS('\n\n=== DEBUG COMPLETE ===\n'))
