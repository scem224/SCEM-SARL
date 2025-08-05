#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exemple d'utilisation du calculateur de salaire brut
SCEM-SARL - Exemple pratique
"""

from salary_calculator import SalaryCalculator, OdooSalaryIntegration


def exemple_simple():
    """Exemple simple de calcul de salaire"""
    print("=== EXEMPLE SIMPLE ===")
    
    # Créer le calculateur
    calc = SalaryCalculator()
    
    # Configurer le salaire
    calc.set_base_salary(2000.0)  # 2000€ de base
    calc.add_overtime(5, 1.25)    # 5h sup à 125%
    calc.add_bonus(200.0, "Prime mensuelle")
    
    # Calculer
    result = calc.calculate_gross_salary(hourly_rate=15.0)
    
    print(f"Salaire brut total: {result['gross_salary_total']:.2f}€")
    return result


def exemple_complet():
    """Exemple complet avec tous les composants"""
    print("\n=== EXEMPLE COMPLET ===")
    
    calc = SalaryCalculator()
    
    # Salaire de base
    calc.set_base_salary(2800.0)
    
    # Heures supplémentaires
    calc.add_overtime(12, 1.5)  # 12h à 150%
    
    # Primes diverses
    calc.add_bonus(400.0, "Prime de performance")
    calc.add_bonus(200.0, "Prime d'assiduité")
    calc.add_bonus(100.0, "Prime de transport")
    
    # Indemnités
    calc.add_allowance(150.0, "Indemnité kilométrique")
    calc.add_allowance(80.0, "Indemnité repas")
    
    # Commissions
    calc.set_commission(600.0)
    
    # Avantages en nature
    calc.add_benefit(300.0, "Véhicule de fonction")
    calc.add_benefit(50.0, "Téléphone")
    calc.add_benefit(100.0, "Tickets restaurant")
    
    # Calcul final
    result = calc.calculate_gross_salary(hourly_rate=18.0)
    
    # Affichage détaillé
    print("Détail du calcul:")
    print(f"- Salaire de base: {result['base_salary']:.2f}€")
    print(f"- Heures supplémentaires: {result['overtime_amount']:.2f}€")
    print(f"- Total primes: {result['total_bonuses']:.2f}€")
    print(f"- Total indemnités: {result['total_allowances']:.2f}€")
    print(f"- Commissions: {result['commissions']:.2f}€")
    print(f"- Avantages en nature: {result['total_benefits']:.2f}€")
    print(f"\n*** TOTAL BRUT: {result['gross_salary_total']:.2f}€ ***")
    
    return result


def exemple_integration_odoo():
    """Exemple d'intégration avec Odoo"""
    print("\n=== INTÉGRATION ODOO ===")
    
    # Créer l'intégration
    odoo = OdooSalaryIntegration()
    
    # Simuler des données de contrat
    contract_data = {
        'wage': 2500.0,
        'overtime_hours': 8,
        'bonuses': [
            {'amount': 250.0, 'description': 'Prime mensuelle'},
            {'amount': 100.0, 'description': 'Prime ancienneté'}
        ]
    }
    
    # Mettre à jour depuis le contrat
    odoo.update_salary_components_from_contract(contract_data)
    
    # Ajouter des éléments supplémentaires
    odoo.calculator.set_commission(300.0)
    odoo.calculator.add_benefit(150.0, "Mutuelle entreprise")
    
    # Créer un enregistrement de paie
    employee_data = {
        'id': 42,
        'name': 'Marie Martin',
        'period_start': '2024-01-01',
        'period_end': '2024-01-31'
    }
    
    salary_record = odoo.create_salary_record(employee_data)
    
    print(f"Employé: {salary_record['employee_name']}")
    print(f"Période: {salary_record['period_start']} au {salary_record['period_end']}")
    print(f"Salaire brut: {salary_record['salary_calculation']['gross_salary_total']:.2f}€")
    print(f"État: {salary_record['state']}")
    
    return salary_record


def calculateur_interactif():
    """Calculateur interactif simple"""
    print("\n=== CALCULATEUR INTERACTIF ===")
    
    calc = SalaryCalculator()
    
    try:
        # Saisie du salaire de base
        base = float(input("Salaire de base (€): "))
        calc.set_base_salary(base)
        
        # Heures supplémentaires
        overtime = input("Heures supplémentaires (0 si aucune): ")
        if overtime and float(overtime) > 0:
            hours = float(overtime)
            rate = input("Taux de majoration (1.25, 1.5, etc. - Entrée pour 1.5): ")
            rate = float(rate) if rate else 1.5
            calc.add_overtime(hours, rate)
        
        # Prime
        bonus = input("Prime mensuelle (0 si aucune): ")
        if bonus and float(bonus) > 0:
            calc.add_bonus(float(bonus), "Prime mensuelle")
        
        # Commission
        commission = input("Commission (0 si aucune): ")
        if commission and float(commission) > 0:
            calc.set_commission(float(commission))
        
        # Calcul
        hourly_rate = input("Taux horaire pour heures sup (15€ par défaut): ")
        hourly_rate = float(hourly_rate) if hourly_rate else 15.0
        
        result = calc.calculate_gross_salary(hourly_rate)
        
        print(f"\n*** VOTRE SALAIRE BRUT: {result['gross_salary_total']:.2f}€ ***")
        
    except ValueError:
        print("Erreur: Veuillez saisir des nombres valides")
    except KeyboardInterrupt:
        print("\nCalcul annulé")


if __name__ == "__main__":
    # Exécuter tous les exemples
    exemple_simple()
    exemple_complet()
    exemple_integration_odoo()
    
    # Proposer le calculateur interactif
    print("\n" + "="*50)
    response = input("Voulez-vous utiliser le calculateur interactif? (o/n): ")
    if response.lower() in ['o', 'oui', 'y', 'yes']:
        calculateur_interactif()