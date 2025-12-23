from .models import Rule

class InferenceEngine:
    def __init__(self):
        # Ambil semua aturan untuk efisiensi agar tidak query berulang
        self.rules = Rule.objects.prefetch_related('symptoms', 'condition').all()

    def diagnose(self, selected_symptom_ids):
        """
        Melakukan inferensi Forward Chaining.
        Input: List ID gejala yang dipilih (contoh: [1, 3, 5])
        Output: List objek Condition yang terpenuhi
        """
        # Ubah input menjadi Set agar pencarian lebih cepat (O(1))
        user_symptoms = set(map(int, selected_symptom_ids))
        
        matched_conditions = []

        for rule in self.rules:
            # Ambil ID gejala dari aturan tersebut
            rule_symptoms = set(rule.symptoms.values_list('id', flat=True))
            
            # LOGIKA UTAMA: Apakah gejala aturan adalah subset dari input user?
            # Jika user memilih G1, G2, G3. Dan aturan butuh G1, G2.
            # Maka {G1, G2} adalah subset dari {G1, G2, G3} -> MATCH.
            if rule_symptoms.issubset(user_symptoms) and rule_symptoms:
                matched_conditions.append(rule.condition)
        
        return matched_conditions