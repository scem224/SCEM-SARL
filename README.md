# Calculateur de Salaire Brut - SCEM SARL

## Description

Ce module Python permet de calculer le salaire total brut pour les employés dans un système compatible Odoo. Il prend en compte toutes les composantes du salaire : salaire de base, heures supplémentaires, primes, indemnités, commissions et avantages en nature.

## Fonctionnalités

### Composantes du salaire gérées :
- **Salaire de base** : Montant fixe mensuel
- **Heures supplémentaires** : Avec taux de majoration personnalisable
- **Primes** : Multiples primes avec descriptions
- **Indemnités** : Diverses indemnités (transport, repas, etc.)
- **Commissions** : Montant variable selon les performances
- **Avantages en nature** : Véhicule, téléphone, etc.

### Fonctionnalités avancées :
- Calcul automatique du total brut
- Historique détaillé des composantes
- Intégration simulée avec Odoo
- Validation des données saisies
- Logging des opérations

## Installation

Aucune dépendance externe requise. Le module utilise uniquement les bibliothèques Python standard.

```bash
# Cloner ou télécharger les fichiers
# Aucune installation supplémentaire nécessaire
```

## Utilisation

### Utilisation simple

```python
from salary_calculator import SalaryCalculator

# Créer le calculateur
calc = SalaryCalculator()

# Configurer le salaire
calc.set_base_salary(2500.0)  # Salaire de base
calc.add_overtime(10, 1.5)    # 10h supplémentaires à 150%
calc.add_bonus(300.0, "Prime mensuelle")
calc.set_commission(200.0)

# Calculer le salaire brut
result = calc.calculate_gross_salary(hourly_rate=16.0)
print(f"Salaire brut total: {result['gross_salary_total']:.2f}€")
```

### Utilisation avancée avec Odoo

```python
from salary_calculator import OdooSalaryIntegration

# Créer l'intégration Odoo
odoo = OdooSalaryIntegration()

# Configurer depuis un contrat
contract_data = {
    'wage': 2800.0,
    'overtime_hours': 8,
    'bonuses': [{'amount': 250.0, 'description': 'Prime performance'}]
}
odoo.update_salary_components_from_contract(contract_data)

# Créer un enregistrement de paie
employee_data = {
    'id': 1,
    'name': 'Jean Dupont',
    'period_start': '2024-01-01',
    'period_end': '2024-01-31'
}
salary_record = odoo.create_salary_record(employee_data)
```

## Exemples d'exécution

### Lancer les exemples
```bash
python salary_calculator.py
```

### Lancer les exemples d'utilisation
```bash
python exemple_utilisation.py
```

## Structure du résultat

Le calcul retourne un dictionnaire détaillé :

```python
{
    'base_salary': 2500.0,
    'overtime_amount': 240.0,
    'total_bonuses': 300.0,
    'total_allowances': 150.0,
    'commissions': 200.0,
    'total_benefits': 100.0,
    'gross_salary_total': 3490.0,
    'breakdown': {
        'bonuses_detail': [...],
        'allowances_detail': [...],
        'benefits_detail': [...],
        'overtime_hours': 10,
        'overtime_rate': 1.5
    },
    'calculation_date': '2024-01-15T10:30:00'
}
```

## API Principale

### Classe SalaryCalculator

#### Méthodes principales :
- `set_base_salary(amount)` : Définir le salaire de base
- `add_overtime(hours, rate)` : Ajouter des heures supplémentaires
- `add_bonus(amount, description)` : Ajouter une prime
- `add_allowance(amount, type)` : Ajouter une indemnité
- `set_commission(amount)` : Définir les commissions
- `add_benefit(value, description)` : Ajouter un avantage en nature
- `calculate_gross_salary(hourly_rate)` : Calculer le salaire brut total
- `reset_components()` : Réinitialiser tous les composants

### Classe OdooSalaryIntegration

#### Méthodes principales :
- `create_salary_record(employee_data)` : Créer un enregistrement de paie
- `update_salary_components_from_contract(contract_data)` : Mettre à jour depuis un contrat

## Exemples de calculs

### Exemple 1 : Employé standard
```
Salaire de base: 2500€
Heures supplémentaires: 10h à 150% (16€/h) = 240€
Prime mensuelle: 300€
Total brut: 3040€
```

### Exemple 2 : Commercial avec commission
```
Salaire de base: 2000€
Commission: 800€
Prime performance: 400€
Avantage véhicule: 200€
Total brut: 3400€
```

## Logs et débogage

Le module utilise le système de logging Python :

```python
import logging
logging.basicConfig(level=logging.INFO)
```

Les opérations importantes sont loggées automatiquement.

## Validation des données

- Tous les montants doivent être positifs
- Les heures supplémentaires ne peuvent pas être négatives
- Le taux de majoration doit être supérieur à 1.0
- Gestion des erreurs avec messages explicites

## Intégration Odoo

Le module simule l'intégration avec les modèles Odoo suivants :
- `hr.employee` : Données employé
- `hr.contract` : Contrat de travail
- `hr.payslip` : Bulletin de paie
- `hr.payslip.line` : Lignes de paie

## Personnalisation

### Modifier les taux par défaut :
```python
calc = SalaryCalculator()
calc.default_hourly_rates['normal'] = 18.0  # Nouveau SMIC
calc.standard_work_hours['weekly'] = 39     # 39h/semaine
```

### Ajouter de nouveaux types de composants :
Le système est extensible pour ajouter d'autres types de rémunération.

## Support

Pour toute question ou amélioration, contactez l'équipe SCEM SARL.

## Licence

Usage interne SCEM SARL - Tous droits réservés.