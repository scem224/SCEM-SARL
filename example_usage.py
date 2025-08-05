#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemple d'utilisation du Calculateur de Salaire Odoo
===================================================

Ce script montre comment utiliser le calculateur de salaire brut.
"""

from odoo_salary_calculator import OdooSalaryCalculator
from config import ODOO_CONFIG
from datetime import datetime

def example_single_employee():
    """
    Exemple: Calcul du salaire pour un employé spécifique
    """
    print("=== Exemple: Calcul pour un employé ===")
    
    try:
        # Création du calculateur
        calculator = OdooSalaryCalculator(**ODOO_CONFIG)
        
        # ID de l'employé (à remplacer par l'ID réel)
        employee_id = 1
        
        # Calcul du salaire brut
        result = calculator.calculate_gross_salary(employee_id)
        
        if 'error' not in result:
            print(f"✅ Employé: {result['employee_name']}")
            print(f"📅 Période: {result['period']}")
            print(f"💰 Salaire de base: {result['base_salary']:.2f} €")
            print(f"➕ Allocations: {result['allowances']['total']:.2f} €")
            print(f"➖ Déductions: {result['deductions']['total']:.2f} €")
            print(f"🎁 Primes: {result['bonuses']['total']:.2f} €")
            print(f"💵 Salaire brut total: {result['final_gross_salary']:.2f} €")
            
            # Export du résultat
            filename = calculator.export_to_json(result)
            print(f"📄 Résultat exporté: {filename}")
            
        else:
            print(f"❌ Erreur: {result['error']}")
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")

def example_all_employees():
    """
    Exemple: Calcul du salaire pour tous les employés
    """
    print("\n=== Exemple: Calcul pour tous les employés ===")
    
    try:
        # Création du calculateur
        calculator = OdooSalaryCalculator(**ODOO_CONFIG)
        
        # Calcul pour tous les employés
        all_results = calculator.calculate_all_employees_gross_salary()
        
        if all_results:
            total_payroll = sum(emp['final_gross_salary'] for emp in all_results)
            avg_salary = total_payroll / len(all_results)
            
            print(f"👥 Nombre d'employés: {len(all_results)}")
            print(f"💼 Masse salariale totale: {total_payroll:.2f} €")
            print(f"📊 Salaire moyen: {avg_salary:.2f} €")
            
            # Affichage des 5 premiers employés
            print("\n📋 Détail des 5 premiers employés:")
            for i, emp in enumerate(all_results[:5], 1):
                print(f"  {i}. {emp['employee_name']}: {emp['final_gross_salary']:.2f} €")
            
            # Export complet
            complete_report = {
                'calculation_date': datetime.now().isoformat(),
                'total_employees': len(all_results),
                'total_payroll': total_payroll,
                'average_salary': avg_salary,
                'employees': all_results
            }
            
            filename = calculator.export_to_json(complete_report, 'rapport_complet_salaires.json')
            print(f"📄 Rapport complet exporté: {filename}")
            
        else:
            print("❌ Aucun employé trouvé ou erreur de calcul")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def example_custom_period():
    """
    Exemple: Calcul pour une période spécifique
    """
    print("\n=== Exemple: Calcul pour une période spécifique ===")
    
    try:
        # Création du calculateur
        calculator = OdooSalaryCalculator(**ODOO_CONFIG)
        
        # Calcul pour janvier 2024
        month = 1
        year = 2024
        employee_id = 1
        
        result = calculator.calculate_gross_salary(employee_id, month, year)
        
        if 'error' not in result:
            print(f"✅ Période: {result['period']}")
            print(f"👤 Employé: {result['employee_name']}")
            print(f"💵 Salaire brut: {result['final_gross_salary']:.2f} €")
            
        else:
            print(f"❌ Erreur: {result['error']}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    """
    Fonction principale avec tous les exemples
    """
    print("🚀 Calculateur de Salaire Brut Odoo")
    print("=" * 50)
    
    # Vérification de la configuration
    if ODOO_CONFIG['db'] == 'your_database_name':
        print("⚠️  ATTENTION: Veuillez configurer vos paramètres de connexion dans config.py")
        print("   - Modifiez ODOO_CONFIG avec vos vraies valeurs")
        return
    
    # Exécution des exemples
    example_single_employee()
    example_all_employees()
    example_custom_period()
    
    print("\n✅ Tous les exemples terminés!")

if __name__ == "__main__":
    main()