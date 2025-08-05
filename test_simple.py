#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test simple du calculateur de salaire
"""

from salary_calculator import SalaryCalculator

def test_calcul_simple():
    """Test de calcul simple"""
    print("=== TEST SIMPLE ===")
    
    calc = SalaryCalculator()
    calc.set_base_salary(2000.0)
    calc.add_bonus(300.0, "Prime test")
    
    result = calc.calculate_gross_salary()
    
    print(f"Salaire de base: {result['base_salary']}€")
    print(f"Prime: {result['total_bonuses']}€")
    print(f"Total brut: {result['gross_salary_total']}€")
    
    # Vérification
    expected = 2000.0 + 300.0
    assert result['gross_salary_total'] == expected, f"Erreur: attendu {expected}, obtenu {result['gross_salary_total']}"
    
    print("✅ Test réussi!")

if __name__ == "__main__":
    test_calcul_simple()