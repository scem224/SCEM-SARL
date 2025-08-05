#!/usr/bin/env python3

from calculateur_pratique import CalculateurPratique

# Test simple
calc = CalculateurPratique()

result = (calc
          .nouveau_calcul("Test User", "Janvier 2024")
          .salaire_base(2500.0)
          .prime(300.0, 'performance')
          .calculer(afficher=False))

print(f"Test réussi - Salaire brut: {result['gross_salary_total']}€")