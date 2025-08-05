#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculateur de Salaire Total Brut pour Odoo
===========================================

Ce script permet de calculer le salaire total brut des employés dans Odoo
en prenant en compte tous les éléments de rémunération.
"""

import xmlrpc.client
import json
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class OdooSalaryCalculator:
    """
    Classe pour calculer le salaire total brut des employés dans Odoo
    """
    
    def __init__(self, url: str, db: str, username: str, password: str):
        """
        Initialise la connexion à Odoo
        
        Args:
            url: URL du serveur Odoo (ex: http://localhost:8069)
            db: Nom de la base de données
            username: Nom d'utilisateur
            password: Mot de passe
        """
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        
        # Connexion à Odoo
        self.common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        self.models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        # Authentification
        self.uid = self.common.authenticate(db, username, password, {})
        if not self.uid:
            raise Exception("Échec de l'authentification Odoo")
        
        logger.info(f"Connexion réussie à Odoo - UID: {self.uid}")
    
    def get_employee_salary_components(self, employee_id: int, payslip_id: Optional[int] = None) -> Dict:
        """
        Récupère tous les composants de salaire d'un employé
        
        Args:
            employee_id: ID de l'employé
            payslip_id: ID du bulletin de paie (optionnel)
            
        Returns:
            Dictionnaire contenant tous les composants de salaire
        """
        try:
            # Récupération des informations de l'employé
            employee = self.models.execute_kw(
                self.db, self.uid, self.password,
                'hr.employee', 'read',
                [employee_id], {'fields': ['name', 'contract_ids', 'department_id']}
            )[0]
            
            # Récupération du contrat actif
            active_contract = self.models.execute_kw(
                self.db, self.uid, self.password,
                'hr.contract', 'search_read',
                [[('employee_id', '=', employee_id), ('state', '=', 'open')]],
                {'fields': ['wage', 'name', 'date_start', 'date_end']}
            )
            
            if not active_contract:
                logger.warning(f"Aucun contrat actif trouvé pour l'employé {employee['name']}")
                return {}
            
            contract = active_contract[0]
            
            # Récupération des éléments de salaire
            salary_elements = self.models.execute_kw(
                self.db, self.uid, self.password,
                'hr.salary.rule', 'search_read',
                [[]],
                {'fields': ['name', 'category_id', 'amount_select', 'amount_fix', 'amount_percentage']}
            )
            
            # Récupération des allocations et déductions
            allowances = self.models.execute_kw(
                self.db, self.uid, self.password,
                'hr.salary.rule', 'search_read',
                [[('category_id.code', '=', 'ALW')]],
                {'fields': ['name', 'amount_fix', 'amount_percentage']}
            )
            
            deductions = self.models.execute_kw(
                self.db, self.uid, self.password,
                'hr.salary.rule', 'search_read',
                [[('category_id.code', '=', 'DED')]],
                {'fields': ['name', 'amount_fix', 'amount_percentage']}
            )
            
            return {
                'employee': employee,
                'contract': contract,
                'salary_elements': salary_elements,
                'allowances': allowances,
                'deductions': deductions
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des composants: {e}")
            return {}
    
    def calculate_gross_salary(self, employee_id: int, month: int = None, year: int = None) -> Dict:
        """
        Calcule le salaire total brut d'un employé
        
        Args:
            employee_id: ID de l'employé
            month: Mois (optionnel, par défaut mois actuel)
            year: Année (optionnel, par défaut année actuelle)
            
        Returns:
            Dictionnaire contenant le calcul détaillé du salaire brut
        """
        try:
            if month is None:
                month = datetime.now().month
            if year is None:
                year = datetime.now().year
            
            # Récupération des composants de salaire
            components = self.get_employee_salary_components(employee_id)
            
            if not components:
                return {'error': 'Impossible de récupérer les composants de salaire'}
            
            contract = components['contract']
            base_salary = contract['wage']
            
            # Calcul des allocations
            total_allowances = 0
            allowances_detail = []
            
            for allowance in components['allowances']:
                amount = allowance.get('amount_fix', 0)
                if allowance.get('amount_percentage'):
                    amount = base_salary * (allowance.get('amount_percentage', 0) / 100)
                
                total_allowances += amount
                allowances_detail.append({
                    'name': allowance['name'],
                    'amount': amount
                })
            
            # Calcul des déductions
            total_deductions = 0
            deductions_detail = []
            
            for deduction in components['deductions']:
                amount = deduction.get('amount_fix', 0)
                if deduction.get('amount_percentage'):
                    amount = base_salary * (deduction.get('amount_percentage', 0) / 100)
                
                total_deductions += amount
                deductions_detail.append({
                    'name': deduction['name'],
                    'amount': amount
                })
            
            # Calcul du salaire brut total
            gross_salary = base_salary + total_allowances - total_deductions
            
            # Récupération des primes et bonus
            bonuses = self.get_bonuses(employee_id, month, year)
            total_bonuses = sum(bonus['amount'] for bonus in bonuses)
            
            # Salaire brut final
            final_gross_salary = gross_salary + total_bonuses
            
            return {
                'employee_name': components['employee']['name'],
                'period': f"{month}/{year}",
                'base_salary': base_salary,
                'allowances': {
                    'total': total_allowances,
                    'details': allowances_detail
                },
                'deductions': {
                    'total': total_deductions,
                    'details': deductions_detail
                },
                'bonuses': {
                    'total': total_bonuses,
                    'details': bonuses
                },
                'gross_salary': gross_salary,
                'final_gross_salary': final_gross_salary,
                'calculation_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul du salaire brut: {e}")
            return {'error': str(e)}
    
    def get_bonuses(self, employee_id: int, month: int, year: int) -> List[Dict]:
        """
        Récupère les primes et bonus d'un employé pour une période donnée
        
        Args:
            employee_id: ID de l'employé
            month: Mois
            year: Année
            
        Returns:
            Liste des primes et bonus
        """
        try:
            # Recherche des primes dans les bulletins de paie
            payslips = self.models.execute_kw(
                self.db, self.uid, self.password,
                'hr.payslip', 'search_read',
                [[
                    ('employee_id', '=', employee_id),
                    ('date_from', '>=', f'{year}-{month:02d}-01'),
                    ('date_to', '<=', f'{year}-{month:02d}-31')
                ]],
                {'fields': ['id', 'date_from', 'date_to']}
            )
            
            bonuses = []
            for payslip in payslips:
                # Récupération des lignes de salaire avec des primes
                payslip_lines = self.models.execute_kw(
                    self.db, self.uid, self.password,
                    'hr.payslip.line', 'search_read',
                    [[('slip_id', '=', payslip['id']), ('category_id.code', '=', 'ALW')]],
                    {'fields': ['name', 'total']}
                )
                
                for line in payslip_lines:
                    if line['total'] > 0:
                        bonuses.append({
                            'name': line['name'],
                            'amount': line['total'],
                            'payslip_date': payslip['date_from']
                        })
            
            return bonuses
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des primes: {e}")
            return []
    
    def calculate_all_employees_gross_salary(self, month: int = None, year: int = None) -> List[Dict]:
        """
        Calcule le salaire brut total pour tous les employés
        
        Args:
            month: Mois (optionnel)
            year: Année (optionnel)
            
        Returns:
            Liste des calculs de salaire pour tous les employés
        """
        try:
            # Récupération de tous les employés actifs
            employees = self.models.execute_kw(
                self.db, self.uid, self.password,
                'hr.employee', 'search_read',
                [[('active', '=', True)]],
                {'fields': ['id', 'name', 'department_id']}
            )
            
            results = []
            for employee in employees:
                salary_calc = self.calculate_gross_salary(employee['id'], month, year)
                if 'error' not in salary_calc:
                    results.append(salary_calc)
                else:
                    logger.warning(f"Erreur pour l'employé {employee['name']}: {salary_calc['error']}")
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul pour tous les employés: {e}")
            return []
    
    def export_to_json(self, data: Dict, filename: str = None) -> str:
        """
        Exporte les données de salaire en JSON
        
        Args:
            data: Données à exporter
            filename: Nom du fichier (optionnel)
            
        Returns:
            Nom du fichier créé
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"salary_calculation_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            
            logger.info(f"Données exportées vers {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Erreur lors de l'export: {e}")
            return None


def main():
    """
    Fonction principale pour démontrer l'utilisation du calculateur
    """
    # Configuration de connexion (à adapter selon votre environnement)
    config = {
        'url': 'http://localhost:8069',
        'db': 'your_database',
        'username': 'your_username',
        'password': 'your_password'
    }
    
    try:
        # Création de l'instance du calculateur
        calculator = OdooSalaryCalculator(**config)
        
        # Exemple 1: Calcul pour un employé spécifique
        employee_id = 1  # Remplacer par l'ID de l'employé
        salary_result = calculator.calculate_gross_salary(employee_id)
        
        if 'error' not in salary_result:
            print("=== Calcul de Salaire Brut ===")
            print(f"Employé: {salary_result['employee_name']}")
            print(f"Période: {salary_result['period']}")
            print(f"Salaire de base: {salary_result['base_salary']:.2f}")
            print(f"Total allocations: {salary_result['allowances']['total']:.2f}")
            print(f"Total déductions: {salary_result['deductions']['total']:.2f}")
            print(f"Total primes: {salary_result['bonuses']['total']:.2f}")
            print(f"Salaire brut total: {salary_result['final_gross_salary']:.2f}")
            
            # Export en JSON
            calculator.export_to_json(salary_result)
        else:
            print(f"Erreur: {salary_result['error']}")
        
        # Exemple 2: Calcul pour tous les employés
        print("\n=== Calcul pour tous les employés ===")
        all_salaries = calculator.calculate_all_employees_gross_salary()
        
        total_payroll = sum(salary['final_gross_salary'] for salary in all_salaries)
        print(f"Nombre d'employés: {len(all_salaries)}")
        print(f"Masse salariale totale: {total_payroll:.2f}")
        
        # Export de tous les résultats
        calculator.export_to_json({
            'calculation_date': datetime.now().isoformat(),
            'total_employees': len(all_salaries),
            'total_payroll': total_payroll,
            'employees': all_salaries
        }, 'complete_salary_report.json')
        
    except Exception as e:
        print(f"Erreur de connexion: {e}")
        print("Vérifiez vos paramètres de connexion Odoo")


if __name__ == "__main__":
    main()