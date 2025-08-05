# Calculateur de Salaire Total Brut pour Odoo

Ce projet Python permet de calculer le salaire total brut des employés dans Odoo en prenant en compte tous les éléments de rémunération.

## 🚀 Fonctionnalités

- ✅ Calcul du salaire brut total par employé
- ✅ Prise en compte des allocations et déductions
- ✅ Calcul des primes et bonus
- ✅ Calcul pour tous les employés
- ✅ Export des résultats en JSON
- ✅ Support des périodes personnalisées
- ✅ Logging détaillé des opérations

## 📋 Prérequis

- Python 3.7+
- Accès à un serveur Odoo avec les modules RH activés
- Permissions d'accès aux données des employés et salaires

## 🛠️ Installation

1. **Cloner ou télécharger le projet**
```bash
git clone <votre-repo>
cd calculateur-salaire-odoo
```

2. **Installer les dépendances**
```bash
pip install xmlrpc-client
```

3. **Configurer la connexion Odoo**
Modifiez le fichier `config.py` avec vos paramètres :

```python
ODOO_CONFIG = {
    'url': 'http://votre-serveur-odoo:8069',
    'db': 'nom_de_votre_base',
    'username': 'votre_utilisateur',
    'password': 'votre_mot_de_passe'
}
```

## 📖 Utilisation

### Utilisation basique

```python
from odoo_salary_calculator import OdooSalaryCalculator
from config import ODOO_CONFIG

# Créer l'instance du calculateur
calculator = OdooSalaryCalculator(**ODOO_CONFIG)

# Calculer le salaire d'un employé
employee_id = 1
result = calculator.calculate_gross_salary(employee_id)

print(f"Salaire brut: {result['final_gross_salary']:.2f} €")
```

### Calcul pour tous les employés

```python
# Calculer pour tous les employés
all_salaries = calculator.calculate_all_employees_gross_salary()

total_payroll = sum(emp['final_gross_salary'] for emp in all_salaries)
print(f"Masse salariale totale: {total_payroll:.2f} €")
```

### Calcul pour une période spécifique

```python
# Calcul pour janvier 2024
result = calculator.calculate_gross_salary(employee_id, month=1, year=2024)
```

### Export des résultats

```python
# Export automatique avec timestamp
filename = calculator.export_to_json(result)

# Export avec nom personnalisé
filename = calculator.export_to_json(result, 'mon_rapport.json')
```

## 🏃‍♂️ Exemples d'exécution

### Exemple 1: Calcul simple
```bash
python example_usage.py
```

### Exemple 2: Utilisation directe
```python
python -c "
from odoo_salary_calculator import OdooSalaryCalculator
from config import ODOO_CONFIG

calc = OdooSalaryCalculator(**ODOO_CONFIG)
result = calc.calculate_gross_salary(1)
print(f'Salaire: {result[\"final_gross_salary\"]:.2f} €')
"
```

## 📊 Structure des données retournées

Le calculateur retourne un dictionnaire avec la structure suivante :

```json
{
  "employee_name": "Nom de l'employé",
  "period": "12/2024",
  "base_salary": 3000.00,
  "allowances": {
    "total": 500.00,
    "details": [
      {"name": "Indemnité transport", "amount": 300.00},
      {"name": "Prime de logement", "amount": 200.00}
    ]
  },
  "deductions": {
    "total": 200.00,
    "details": [
      {"name": "Cotisation sociale", "amount": 200.00}
    ]
  },
  "bonuses": {
    "total": 1000.00,
    "details": [
      {"name": "Prime de performance", "amount": 1000.00}
    ]
  },
  "gross_salary": 3300.00,
  "final_gross_salary": 4300.00,
  "calculation_date": "2024-12-19T10:30:00"
}
```

## 🔧 Configuration avancée

### Personnalisation des calculs

Vous pouvez modifier les règles de calcul en éditant la classe `OdooSalaryCalculator` :

```python
class CustomSalaryCalculator(OdooSalaryCalculator):
    def calculate_gross_salary(self, employee_id, month=None, year=None):
        # Votre logique personnalisée
        pass
```

### Ajout de nouveaux éléments de salaire

Pour ajouter de nouveaux éléments (ex: avantages en nature) :

```python
def get_additional_benefits(self, employee_id):
    # Récupération des avantages en nature
    benefits = self.models.execute_kw(
        self.db, self.uid, self.password,
        'hr.benefit', 'search_read',
        [[('employee_id', '=', employee_id)]],
        {'fields': ['name', 'value']}
    )
    return benefits
```

## 🐛 Dépannage

### Erreurs courantes

1. **Erreur d'authentification**
   - Vérifiez vos paramètres de connexion dans `config.py`
   - Assurez-vous que l'utilisateur a les permissions nécessaires

2. **Aucun contrat trouvé**
   - Vérifiez que l'employé a un contrat actif
   - Contrôlez les dates de début/fin du contrat

3. **Erreur de connexion réseau**
   - Vérifiez l'URL du serveur Odoo
   - Contrôlez que le serveur est accessible

### Logs et debugging

Le script génère des logs détaillés. Pour activer le mode debug :

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📁 Structure du projet

```
calculateur-salaire-odoo/
├── odoo_salary_calculator.py  # Script principal
├── config.py                  # Configuration
├── example_usage.py          # Exemples d'utilisation
├── README.md                 # Documentation
└── exports/                  # Dossier d'export (créé automatiquement)
    ├── salary_calculation_20241219_103000.json
    └── rapport_complet_salaires.json
```

## 🔒 Sécurité

- ⚠️ Ne stockez jamais les mots de passe en clair dans le code
- 🔐 Utilisez des variables d'environnement pour les secrets
- 🛡️ Limitez les permissions de l'utilisateur Odoo au minimum nécessaire

### Utilisation avec variables d'environnement

```python
import os

ODOO_CONFIG = {
    'url': os.getenv('ODOO_URL'),
    'db': os.getenv('ODOO_DB'),
    'username': os.getenv('ODOO_USERNAME'),
    'password': os.getenv('ODOO_PASSWORD')
}
```

## 🤝 Contribution

Pour contribuer au projet :

1. Fork le repository
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Créez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 📞 Support

Pour toute question ou problème :

- 📧 Email: support@votre-entreprise.com
- 🐛 Issues: Créez une issue sur GitHub
- 📖 Documentation: Consultez ce README

---

**Note**: Ce script est conçu pour fonctionner avec Odoo 12+ et les modules RH standard. Des adaptations peuvent être nécessaires selon votre configuration spécifique.