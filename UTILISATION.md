# Guide d'utilisation rapide - Calculateur de Salaire Brut

## 🚀 Démarrage rapide

### Utilisation simple
```python
from salary_calculator import SalaryCalculator

calc = SalaryCalculator()
calc.set_base_salary(2500.0)
calc.add_bonus(300.0, "Prime mensuelle")
result = calc.calculate_gross_salary()
print(f"Salaire brut: {result['gross_salary_total']}€")
```

### Utilisation avancée (recommandée)
```python
from calculateur_pratique import CalculateurPratique

calc = CalculateurPratique()
result = (calc
    .nouveau_calcul("Jean Dupont", "Janvier 2024")
    .salaire_base(2800.0)
    .heures_supplementaires(10)
    .prime(400.0, 'performance')
    .indemnite(150.0, 'transport')
    .commission(300.0)
    .avantage(200.0, 'vehicule')
    .calculer())
```

## 📁 Fichiers principaux

1. **`salary_calculator.py`** - Module de base complet
2. **`calculateur_pratique.py`** - Interface simplifiée (recommandé)
3. **`config_salaire.py`** - Configuration et paramètres
4. **`demo_final.py`** - Démonstration complète

## 🧮 Composants de salaire supportés

- ✅ Salaire de base
- ✅ Heures supplémentaires (avec majoration automatique)
- ✅ Primes (performance, ancienneté, etc.)
- ✅ Indemnités (transport, repas, kilométrique, etc.)
- ✅ Commissions
- ✅ Avantages en nature (véhicule, téléphone, etc.)

## 🎯 Exemples d'usage

### Employé standard
```python
calc = CalculateurPratique()
calc.nouveau_calcul("Marie Dupont", "Janvier 2024")
calc.salaire_base(2400.0)
calc.heures_supplementaires(8)
calc.prime(200.0, 'performance')
calc.indemnite(120.0, 'transport')
result = calc.calculer()
```

### Commercial
```python
calc = CalculateurPratique()
calc.nouveau_calcul("Pierre Martin", "Janvier 2024")
calc.salaire_base(2000.0)
calc.commission(800.0)
calc.prime(300.0, 'objectifs')
calc.avantage(250.0, 'vehicule')
result = calc.calculer()
```

## 🔧 Tests

```bash
# Test simple
python3 test_simple.py

# Test calculateur pratique
python3 test_calculateur.py

# Démonstration complète
python3 demo_final.py
```

## 📊 Résultat type

```python
{
    'base_salary': 2800.0,
    'overtime_amount': 225.0,
    'total_bonuses': 400.0,
    'total_allowances': 150.0,
    'commissions': 300.0,
    'total_benefits': 200.0,
    'gross_salary_total': 4075.0,
    'calculation_date': '2024-01-15T10:30:00'
}
```

## ⚡ Commandes utiles

```bash
# Lancer la démonstration
python3 demo_final.py

# Lancer les exemples
python3 exemple_utilisation.py

# Voir la configuration
python3 config_salaire.py

# Tests rapides
python3 test_simple.py
```

## 🎨 Interface fluide

Le `CalculateurPratique` permet un chaînage des méthodes :

```python
result = (CalculateurPratique()
    .nouveau_calcul("Employé", "Période")
    .salaire_base(2500)
    .prime(300, 'performance')
    .calculer())
```

## 📈 Fonctionnalités avancées

- Validation automatique des montants
- Calcul automatique des majorations d'heures sup
- Types prédéfinis de primes/indemnités/avantages
- Logging des opérations
- Estimation du salaire net
- Intégration Odoo simulée

## 🏢 Pour SCEM SARL

Le système est configuré avec :
- SMIC 2024 : 11.65€/h
- Taux standard : 15€/h
- Majorations légales : 125% et 150%
- Types de primes français
- Validation des montants

---

**Système opérationnel et prêt pour la production !** 🎉