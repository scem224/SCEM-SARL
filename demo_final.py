#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Démonstration finale du système de calcul de salaire brut
SCEM SARL - Présentation complète
"""

from calculateur_pratique import CalculateurPratique
from salary_calculator import SalaryCalculator
from config_salaire import TAUX_HORAIRES, TYPES_PRIMES


def demo_complete():
    """Démonstration complète du système"""
    print("=" * 60)
    print("SYSTÈME DE CALCUL DE SALAIRE BRUT - SCEM SARL")
    print("=" * 60)
    
    # 1. Calcul basique
    print("\n1. CALCUL BASIQUE")
    print("-" * 30)
    
    calc_basic = SalaryCalculator()
    calc_basic.set_base_salary(2500.0)
    calc_basic.add_bonus(300.0, "Prime mensuelle")
    result_basic = calc_basic.calculate_gross_salary()
    
    print(f"Salaire de base: {result_basic['base_salary']}€")
    print(f"Prime: {result_basic['total_bonuses']}€")
    print(f"TOTAL BRUT: {result_basic['gross_salary_total']}€")
    
    # 2. Calcul avancé avec le calculateur pratique
    print("\n2. CALCUL AVANCÉ - EMPLOYÉ STANDARD")
    print("-" * 40)
    
    calc_advanced = CalculateurPratique()
    result_advanced = (calc_advanced
                      .nouveau_calcul("Jean Dupont", "Janvier 2024")
                      .salaire_base(2800.0)
                      .heures_supplementaires(12)  # 12h supplémentaires
                      .prime(400.0, 'performance')
                      .prime(150.0, 'anciennete')
                      .indemnite(200.0, 'transport')
                      .commission(300.0)
                      .avantage(250.0, 'vehicule')
                      .calculer(afficher=False))
    
    print(f"Employé: Jean Dupont")
    print(f"Période: Janvier 2024")
    print(f"Salaire de base: {result_advanced['base_salary']:>10.2f}€")
    print(f"Heures supplémentaires: {result_advanced['overtime_amount']:>10.2f}€")
    print(f"Primes: {result_advanced['total_bonuses']:>10.2f}€")
    print(f"Indemnités: {result_advanced['total_allowances']:>10.2f}€")
    print(f"Commissions: {result_advanced['commissions']:>10.2f}€")
    print(f"Avantages: {result_advanced['total_benefits']:>10.2f}€")
    print(f"TOTAL BRUT: {result_advanced['gross_salary_total']:>10.2f}€")
    
    # 3. Comparaison de profils
    print("\n3. COMPARAISON DE PROFILS")
    print("-" * 35)
    
    # Profil 1: Employé
    calc1 = CalculateurPratique()
    employe = (calc1
               .nouveau_calcul("Marie Martin - Employée", "")
               .salaire_base(2200.0)
               .prime(150.0, 'assiduité')
               .indemnite(100.0, 'transport')
               .calculer(afficher=False))
    
    # Profil 2: Commercial
    calc2 = CalculateurPratique()
    commercial = (calc2
                  .nouveau_calcul("Pierre Durand - Commercial", "")
                  .salaire_base(2000.0)
                  .commission(800.0)
                  .prime(300.0, 'objectifs')
                  .avantage(300.0, 'vehicule')
                  .calculer(afficher=False))
    
    # Profil 3: Cadre
    calc3 = CalculateurPratique()
    cadre = (calc3
             .nouveau_calcul("Sophie Bernard - Cadre", "")
             .salaire_base(4000.0)
             .prime(600.0, 'treizieme_mois')
             .indemnite(400.0, 'kilometrique')
             .avantage(400.0, 'vehicule')
             .avantage(100.0, 'mutuelle')
             .calculer(afficher=False))
    
    print(f"Employée (Marie):    {employe['gross_salary_total']:>8.2f}€")
    print(f"Commercial (Pierre): {commercial['gross_salary_total']:>8.2f}€")
    print(f"Cadre (Sophie):      {cadre['gross_salary_total']:>8.2f}€")
    
    # 4. Statistiques
    print("\n4. STATISTIQUES")
    print("-" * 20)
    
    salaires = [employe['gross_salary_total'], 
                commercial['gross_salary_total'], 
                cadre['gross_salary_total']]
    
    print(f"Salaire moyen: {sum(salaires)/len(salaires):>10.2f}€")
    print(f"Salaire minimum: {min(salaires):>8.2f}€")
    print(f"Salaire maximum: {max(salaires):>8.2f}€")
    
    # 5. Configuration utilisée
    print("\n5. CONFIGURATION SYSTÈME")
    print("-" * 30)
    
    print(f"SMIC horaire: {TAUX_HORAIRES['smic']}€")
    print(f"Taux standard: {TAUX_HORAIRES['normal']}€")
    print(f"Majoration 150%: {TAUX_HORAIRES['overtime_150']}€")
    print(f"Types de primes: {len(TYPES_PRIMES)}")
    
    print("\n" + "=" * 60)
    print("DÉMONSTRATION TERMINÉE")
    print("Système opérationnel pour SCEM SARL")
    print("=" * 60)


def demo_cas_reel():
    """Démonstration avec un cas réel d'entreprise"""
    print("\n" + "=" * 50)
    print("CAS RÉEL D'ENTREPRISE - PAIE MENSUELLE")
    print("=" * 50)
    
    employees = [
        {
            'name': 'Alice Dubois',
            'role': 'Assistante administrative',
            'base': 2300.0,
            'overtime': 4,
            'bonuses': [('assiduité', 100.0)],
            'allowances': [('transport', 80.0), ('repas', 120.0)]
        },
        {
            'name': 'Bob Leroy',
            'role': 'Technicien',
            'base': 2600.0,
            'overtime': 8,
            'bonuses': [('performance', 200.0)],
            'allowances': [('transport', 100.0)]
        },
        {
            'name': 'Claire Moreau',
            'role': 'Responsable commerciale',
            'base': 3200.0,
            'overtime': 0,
            'bonuses': [('objectifs', 500.0), ('anciennete', 300.0)],
            'allowances': [('kilometrique', 250.0)],
            'commission': 600.0,
            'benefits': [('vehicule', 350.0), ('telephone', 50.0)]
        }
    ]
    
    total_masse_salariale = 0
    
    for emp in employees:
        calc = CalculateurPratique()
        calc.nouveau_calcul(emp['name'], "Janvier 2024")
        calc.salaire_base(emp['base'])
        
        if emp.get('overtime', 0) > 0:
            calc.heures_supplementaires(emp['overtime'])
        
        for bonus_type, amount in emp.get('bonuses', []):
            calc.prime(amount, bonus_type)
        
        for allowance_type, amount in emp.get('allowances', []):
            calc.indemnite(amount, allowance_type)
        
        if emp.get('commission', 0) > 0:
            calc.commission(emp['commission'])
        
        for benefit_type, amount in emp.get('benefits', []):
            calc.avantage(amount, benefit_type)
        
        result = calc.calculer(afficher=False)
        total_masse_salariale += result['gross_salary_total']
        
        print(f"{emp['name']} ({emp['role']}):")
        print(f"  Salaire brut: {result['gross_salary_total']:>8.2f}€")
        print(f"  Salaire net*: {result['gross_salary_total'] * 0.77:>8.2f}€")
        print()
    
    print("-" * 50)
    print(f"MASSE SALARIALE BRUTE TOTALE: {total_masse_salariale:>10.2f}€")
    print(f"MASSE SALARIALE NETTE*:       {total_masse_salariale * 0.77:>10.2f}€")
    print(f"CHARGES SOCIALES*:            {total_masse_salariale * 0.23:>10.2f}€")
    print("*Estimation approximative")


if __name__ == "__main__":
    # Lancer la démonstration complète
    demo_complete()
    
    # Cas réel d'entreprise
    demo_cas_reel()
    
    print("\n🎉 SYSTÈME PRÊT POUR PRODUCTION 🎉")
    print("\nFichiers disponibles:")
    print("- salary_calculator.py : Module principal")
    print("- calculateur_pratique.py : Interface simplifiée")
    print("- config_salaire.py : Configuration")
    print("- exemple_utilisation.py : Exemples détaillés")
    print("- README.md : Documentation complète")