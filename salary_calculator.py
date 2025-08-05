#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module de calcul de salaire total brut pour Odoo
SCEM-SARL - Système de gestion des salaires
"""

from datetime import datetime, date
from typing import Dict, List, Optional, Union
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SalaryCalculator:
    """
    Calculateur de salaire total brut pour Odoo
    Gère les différentes composantes du salaire et les calculs associés
    """
    
    def __init__(self):
        """Initialisation du calculateur de salaire"""
        self.salary_components = {
            'base_salary': 0.0,
            'overtime_hours': 0.0,
            'overtime_rate': 1.5,
            'bonuses': [],
            'allowances': [],
            'commissions': 0.0,
            'benefits': []
        }
        
        # Taux horaires par défaut
        self.default_hourly_rates = {
            'normal': 15.0,  # SMIC horaire approximatif
            'overtime': 22.5  # 1.5 * taux normal
        }
        
        # Heures de travail standards
        self.standard_work_hours = {
            'weekly': 35,
            'monthly': 151.67,  # 35h * 52 semaines / 12 mois
            'daily': 7
        }
    
    def set_base_salary(self, amount: float) -> None:
        """
        Définir le salaire de base
        
        Args:
            amount (float): Montant du salaire de base
        """
        if amount < 0:
            raise ValueError("Le salaire de base ne peut pas être négatif")
        
        self.salary_components['base_salary'] = amount
        logger.info(f"Salaire de base défini: {amount}€")
    
    def add_overtime(self, hours: float, rate: Optional[float] = None) -> None:
        """
        Ajouter des heures supplémentaires
        
        Args:
            hours (float): Nombre d'heures supplémentaires
            rate (float, optional): Taux majoré (défaut: 1.5)
        """
        if hours < 0:
            raise ValueError("Les heures supplémentaires ne peuvent pas être négatives")
        
        if rate is None:
            rate = self.salary_components['overtime_rate']
        
        self.salary_components['overtime_hours'] = hours
        self.salary_components['overtime_rate'] = rate
        logger.info(f"Heures supplémentaires ajoutées: {hours}h à {rate}x")
    
    def add_bonus(self, amount: float, description: str = "Prime") -> None:
        """
        Ajouter une prime
        
        Args:
            amount (float): Montant de la prime
            description (str): Description de la prime
        """
        if amount < 0:
            raise ValueError("Le montant de la prime ne peut pas être négatif")
        
        bonus = {
            'amount': amount,
            'description': description,
            'date': datetime.now().isoformat()
        }
        
        self.salary_components['bonuses'].append(bonus)
        logger.info(f"Prime ajoutée: {description} - {amount}€")
    
    def add_allowance(self, amount: float, type_allowance: str = "Indemnité") -> None:
        """
        Ajouter une indemnité
        
        Args:
            amount (float): Montant de l'indemnité
            type_allowance (str): Type d'indemnité
        """
        if amount < 0:
            raise ValueError("Le montant de l'indemnité ne peut pas être négatif")
        
        allowance = {
            'amount': amount,
            'type': type_allowance,
            'date': datetime.now().isoformat()
        }
        
        self.salary_components['allowances'].append(allowance)
        logger.info(f"Indemnité ajoutée: {type_allowance} - {amount}€")
    
    def set_commission(self, amount: float) -> None:
        """
        Définir les commissions
        
        Args:
            amount (float): Montant des commissions
        """
        if amount < 0:
            raise ValueError("Les commissions ne peuvent pas être négatives")
        
        self.salary_components['commissions'] = amount
        logger.info(f"Commissions définies: {amount}€")
    
    def add_benefit(self, value: float, description: str = "Avantage") -> None:
        """
        Ajouter un avantage en nature
        
        Args:
            value (float): Valeur de l'avantage
            description (str): Description de l'avantage
        """
        if value < 0:
            raise ValueError("La valeur de l'avantage ne peut pas être négative")
        
        benefit = {
            'value': value,
            'description': description,
            'date': datetime.now().isoformat()
        }
        
        self.salary_components['benefits'].append(benefit)
        logger.info(f"Avantage ajouté: {description} - {value}€")
    
    def calculate_overtime_amount(self, hourly_rate: Optional[float] = None) -> float:
        """
        Calculer le montant des heures supplémentaires
        
        Args:
            hourly_rate (float, optional): Taux horaire de base
            
        Returns:
            float: Montant des heures supplémentaires
        """
        if hourly_rate is None:
            hourly_rate = self.default_hourly_rates['normal']
        
        overtime_hours = self.salary_components['overtime_hours']
        overtime_rate = self.salary_components['overtime_rate']
        
        # Calcul: heures_sup * taux_horaire * majoration
        overtime_amount = overtime_hours * hourly_rate * overtime_rate
        
        return round(overtime_amount, 2)
    
    def calculate_total_bonuses(self) -> float:
        """
        Calculer le total des primes
        
        Returns:
            float: Total des primes
        """
        total = sum(bonus['amount'] for bonus in self.salary_components['bonuses'])
        return round(total, 2)
    
    def calculate_total_allowances(self) -> float:
        """
        Calculer le total des indemnités
        
        Returns:
            float: Total des indemnités
        """
        total = sum(allowance['amount'] for allowance in self.salary_components['allowances'])
        return round(total, 2)
    
    def calculate_total_benefits(self) -> float:
        """
        Calculer le total des avantages en nature
        
        Returns:
            float: Total des avantages
        """
        total = sum(benefit['value'] for benefit in self.salary_components['benefits'])
        return round(total, 2)
    
    def calculate_gross_salary(self, hourly_rate: Optional[float] = None) -> Dict[str, Union[float, Dict]]:
        """
        Calculer le salaire total brut
        
        Args:
            hourly_rate (float, optional): Taux horaire pour le calcul des heures sup
            
        Returns:
            Dict: Détail du calcul du salaire brut
        """
        # Composantes du salaire
        base_salary = self.salary_components['base_salary']
        overtime_amount = self.calculate_overtime_amount(hourly_rate)
        total_bonuses = self.calculate_total_bonuses()
        total_allowances = self.calculate_total_allowances()
        commissions = self.salary_components['commissions']
        total_benefits = self.calculate_total_benefits()
        
        # Calcul du salaire brut total
        gross_salary = (
            base_salary +
            overtime_amount +
            total_bonuses +
            total_allowances +
            commissions +
            total_benefits
        )
        
        # Détail du calcul
        calculation_detail = {
            'base_salary': base_salary,
            'overtime_amount': overtime_amount,
            'total_bonuses': total_bonuses,
            'total_allowances': total_allowances,
            'commissions': commissions,
            'total_benefits': total_benefits,
            'gross_salary_total': round(gross_salary, 2)
        }
        
        # Informations complémentaires
        calculation_detail['breakdown'] = {
            'bonuses_detail': self.salary_components['bonuses'],
            'allowances_detail': self.salary_components['allowances'],
            'benefits_detail': self.salary_components['benefits'],
            'overtime_hours': self.salary_components['overtime_hours'],
            'overtime_rate': self.salary_components['overtime_rate']
        }
        
        calculation_detail['calculation_date'] = datetime.now().isoformat()
        
        logger.info(f"Salaire brut total calculé: {gross_salary:.2f}€")
        
        return calculation_detail
    
    def reset_components(self) -> None:
        """Réinitialiser tous les composants du salaire"""
        self.salary_components = {
            'base_salary': 0.0,
            'overtime_hours': 0.0,
            'overtime_rate': 1.5,
            'bonuses': [],
            'allowances': [],
            'commissions': 0.0,
            'benefits': []
        }
        logger.info("Composants du salaire réinitialisés")
    
    def get_salary_summary(self) -> Dict:
        """
        Obtenir un résumé des composants du salaire
        
        Returns:
            Dict: Résumé des composants
        """
        return {
            'base_salary': self.salary_components['base_salary'],
            'overtime_hours': self.salary_components['overtime_hours'],
            'bonuses_count': len(self.salary_components['bonuses']),
            'allowances_count': len(self.salary_components['allowances']),
            'commissions': self.salary_components['commissions'],
            'benefits_count': len(self.salary_components['benefits'])
        }


class OdooSalaryIntegration:
    """
    Classe d'intégration avec Odoo pour les calculs de salaire
    Simule les interactions avec les modèles Odoo
    """
    
    def __init__(self):
        self.calculator = SalaryCalculator()
    
    def create_salary_record(self, employee_data: Dict) -> Dict:
        """
        Créer un enregistrement de salaire (simulation Odoo)
        
        Args:
            employee_data (Dict): Données de l'employé
            
        Returns:
            Dict: Enregistrement de salaire créé
        """
        # Simulation d'un modèle Odoo hr.payslip
        salary_record = {
            'employee_id': employee_data.get('id'),
            'employee_name': employee_data.get('name'),
            'period_start': employee_data.get('period_start'),
            'period_end': employee_data.get('period_end'),
            'salary_calculation': self.calculator.calculate_gross_salary(),
            'state': 'draft',
            'create_date': datetime.now().isoformat()
        }
        
        return salary_record
    
    def update_salary_components_from_contract(self, contract_data: Dict) -> None:
        """
        Mettre à jour les composants de salaire depuis un contrat
        
        Args:
            contract_data (Dict): Données du contrat
        """
        if 'wage' in contract_data:
            self.calculator.set_base_salary(contract_data['wage'])
        
        if 'overtime_hours' in contract_data:
            self.calculator.add_overtime(contract_data['overtime_hours'])
        
        if 'bonuses' in contract_data:
            for bonus in contract_data['bonuses']:
                self.calculator.add_bonus(bonus['amount'], bonus.get('description', 'Prime'))


def main():
    """Fonction principale de démonstration"""
    print("=== CALCULATEUR DE SALAIRE BRUT - SCEM SARL ===\n")
    
    # Créer une instance du calculateur
    calc = SalaryCalculator()
    
    # Exemple de calcul de salaire
    print("1. Configuration du salaire de base")
    calc.set_base_salary(2500.0)  # Salaire de base: 2500€
    
    print("\n2. Ajout d'heures supplémentaires")
    calc.add_overtime(10, 1.5)  # 10h supplémentaires à 150%
    
    print("\n3. Ajout de primes")
    calc.add_bonus(300.0, "Prime de performance")
    calc.add_bonus(150.0, "Prime d'ancienneté")
    
    print("\n4. Ajout d'indemnités")
    calc.add_allowance(200.0, "Indemnité transport")
    calc.add_allowance(100.0, "Indemnité repas")
    
    print("\n5. Ajout de commissions")
    calc.set_commission(500.0)
    
    print("\n6. Ajout d'avantages en nature")
    calc.add_benefit(200.0, "Véhicule de fonction")
    calc.add_benefit(50.0, "Téléphone portable")
    
    print("\n7. Calcul du salaire brut total")
    result = calc.calculate_gross_salary(hourly_rate=16.0)
    
    print("\n=== RÉSULTAT DU CALCUL ===")
    print(f"Salaire de base: {result['base_salary']:.2f}€")
    print(f"Heures supplémentaires: {result['overtime_amount']:.2f}€")
    print(f"Total primes: {result['total_bonuses']:.2f}€")
    print(f"Total indemnités: {result['total_allowances']:.2f}€")
    print(f"Commissions: {result['commissions']:.2f}€")
    print(f"Avantages en nature: {result['total_benefits']:.2f}€")
    print(f"\n*** SALAIRE BRUT TOTAL: {result['gross_salary_total']:.2f}€ ***")
    
    print(f"\nCalcul effectué le: {result['calculation_date']}")
    
    # Démonstration de l'intégration Odoo
    print("\n=== INTÉGRATION ODOO ===")
    odoo_integration = OdooSalaryIntegration()
    odoo_integration.calculator = calc
    
    employee_data = {
        'id': 1,
        'name': 'Jean Dupont',
        'period_start': '2024-01-01',
        'period_end': '2024-01-31'
    }
    
    salary_record = odoo_integration.create_salary_record(employee_data)
    print(f"Enregistrement créé pour: {salary_record['employee_name']}")
    print(f"Salaire brut: {salary_record['salary_calculation']['gross_salary_total']:.2f}€")


if __name__ == "__main__":
    main()