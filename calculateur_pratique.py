#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calculateur de salaire pratique avec interface simplifiée
SCEM SARL - Usage quotidien
"""

from salary_calculator import SalaryCalculator, OdooSalaryIntegration
from config_salaire import (
    TAUX_HORAIRES, TYPES_PRIMES, TYPES_INDEMNITES, TYPES_AVANTAGES,
    get_taux_horaire, calculer_majoration_heures_sup, valider_montant
)


class CalculateurPratique:
    """Calculateur simplifié pour usage quotidien"""
    
    def __init__(self):
        self.calc = SalaryCalculator()
        self.employee_name = ""
        self.period = ""
    
    def nouveau_calcul(self, nom_employe="", periode=""):
        """Commencer un nouveau calcul"""
        self.calc.reset_components()
        self.employee_name = nom_employe
        self.period = periode
        print(f"=== NOUVEAU CALCUL SALAIRE ===")
        if nom_employe:
            print(f"Employé: {nom_employe}")
        if periode:
            print(f"Période: {periode}")
        print()
        return self
    
    def salaire_base(self, montant):
        """Définir le salaire de base avec validation"""
        if not valider_montant(montant, 'salaire'):
            raise ValueError(f"Salaire invalide: {montant}€")
        
        self.calc.set_base_salary(montant)
        return self
    
    def heures_supplementaires(self, heures, taux_horaire=None):
        """Ajouter des heures supplémentaires avec calcul automatique de la majoration"""
        if not valider_montant(heures, 'heures_sup'):
            raise ValueError(f"Nombre d'heures invalide: {heures}h")
        
        if taux_horaire is None:
            taux_horaire = get_taux_horaire('normal')
        
        # Calcul automatique de la majoration selon les heures
        heures_hebdo = heures / 4.33  # Approximation mensuelle vers hebdomadaire
        majoration = calculer_majoration_heures_sup(heures_hebdo + 35)
        
        self.calc.add_overtime(heures, majoration)
        print(f"Heures supplémentaires: {heures}h à {majoration}x ({taux_horaire}€/h)")
        return self
    
    def prime(self, montant, type_prime='performance'):
        """Ajouter une prime avec type prédéfini"""
        description = TYPES_PRIMES.get(type_prime, f"Prime {type_prime}")
        self.calc.add_bonus(montant, description)
        return self
    
    def indemnite(self, montant, type_indemnite='transport'):
        """Ajouter une indemnité avec type prédéfini"""
        description = TYPES_INDEMNITES.get(type_indemnite, f"Indemnité {type_indemnite}")
        self.calc.add_allowance(montant, description)
        return self
    
    def commission(self, montant):
        """Définir les commissions"""
        self.calc.set_commission(montant)
        return self
    
    def avantage(self, valeur, type_avantage='vehicule'):
        """Ajouter un avantage en nature avec type prédéfini"""
        description = TYPES_AVANTAGES.get(type_avantage, f"Avantage {type_avantage}")
        self.calc.add_benefit(valeur, description)
        return self
    
    def calculer(self, taux_horaire=None, afficher=True):
        """Calculer le salaire avec affichage optionnel"""
        if taux_horaire is None:
            taux_horaire = get_taux_horaire('normal')
        
        result = self.calc.calculate_gross_salary(taux_horaire)
        
        if afficher:
            self.afficher_resultat(result)
        
        return result
    
    def afficher_resultat(self, result):
        """Afficher le résultat de manière claire"""
        print("\n" + "="*50)
        print("DÉTAIL DU CALCUL DE SALAIRE")
        print("="*50)
        
        if self.employee_name:
            print(f"Employé: {self.employee_name}")
        if self.period:
            print(f"Période: {self.period}")
        
        print(f"\nSalaire de base:           {result['base_salary']:>10.2f}€")
        
        if result['overtime_amount'] > 0:
            print(f"Heures supplémentaires:    {result['overtime_amount']:>10.2f}€")
        
        if result['total_bonuses'] > 0:
            print(f"Total primes:              {result['total_bonuses']:>10.2f}€")
        
        if result['total_allowances'] > 0:
            print(f"Total indemnités:          {result['total_allowances']:>10.2f}€")
        
        if result['commissions'] > 0:
            print(f"Commissions:               {result['commissions']:>10.2f}€")
        
        if result['total_benefits'] > 0:
            print(f"Avantages en nature:       {result['total_benefits']:>10.2f}€")
        
        print("-" * 50)
        print(f"SALAIRE BRUT TOTAL:        {result['gross_salary_total']:>10.2f}€")
        print("=" * 50)
        
        # Estimation du net (approximative)
        net_approximatif = result['gross_salary_total'] * 0.77  # ~23% de charges
        print(f"Salaire net approximatif:  {net_approximatif:>10.2f}€")
        print("(estimation à -23% de charges sociales)")
    
    def resume(self):
        """Afficher un résumé des composants"""
        summary = self.calc.get_salary_summary()
        print("\n=== RÉSUMÉ DES COMPOSANTS ===")
        print(f"Salaire de base: {summary['base_salary']}€")
        print(f"Heures supplémentaires: {summary['overtime_hours']}h")
        print(f"Nombre de primes: {summary['bonuses_count']}")
        print(f"Nombre d'indemnités: {summary['allowances_count']}")
        print(f"Commissions: {summary['commissions']}€")
        print(f"Nombre d'avantages: {summary['benefits_count']}")


def exemple_employe_standard():
    """Exemple pour un employé standard"""
    calc = CalculateurPratique()
    
    result = (calc
              .nouveau_calcul("Marie Dupont", "Janvier 2024")
              .salaire_base(2400.0)
              .heures_supplementaires(8)  # 8h sup dans le mois
              .prime(200.0, 'performance')
              .indemnite(120.0, 'transport')
              .calculer())
    
    return result


def exemple_commercial():
    """Exemple pour un commercial"""
    calc = CalculateurPratique()
    
    result = (calc
              .nouveau_calcul("Pierre Martin", "Janvier 2024")
              .salaire_base(2000.0)
              .commission(800.0)
              .prime(300.0, 'objectifs')
              .avantage(250.0, 'vehicule')
              .avantage(50.0, 'telephone')
              .calculer())
    
    return result


def exemple_cadre():
    """Exemple pour un cadre"""
    calc = CalculateurPratique()
    
    result = (calc
              .nouveau_calcul("Sophie Bernard", "Janvier 2024")
              .salaire_base(3500.0)
              .prime(500.0, 'treizieme_mois')
              .prime(200.0, 'anciennete')
              .indemnite(300.0, 'kilometrique')
              .avantage(300.0, 'vehicule')
              .avantage(100.0, 'mutuelle')
              .calculer())
    
    return result


def calculateur_interactif_avance():
    """Version avancée du calculateur interactif"""
    calc = CalculateurPratique()
    
    print("=== CALCULATEUR INTERACTIF AVANCÉ ===")
    
    try:
        # Informations de base
        nom = input("Nom de l'employé (optionnel): ").strip()
        periode = input("Période (ex: Janvier 2024): ").strip()
        
        calc.nouveau_calcul(nom, periode)
        
        # Salaire de base
        base = float(input("Salaire de base (€): "))
        calc.salaire_base(base)
        
        # Heures supplémentaires
        heures_sup = input("Heures supplémentaires (0 si aucune): ").strip()
        if heures_sup and float(heures_sup) > 0:
            calc.heures_supplementaires(float(heures_sup))
        
        # Primes
        print("\nTypes de primes disponibles:")
        for key, desc in TYPES_PRIMES.items():
            print(f"  {key}: {desc}")
        
        while True:
            prime_input = input("\nPrime (montant type ou 'fin'): ").strip()
            if prime_input.lower() == 'fin':
                break
            
            try:
                parts = prime_input.split()
                montant = float(parts[0])
                type_prime = parts[1] if len(parts) > 1 else 'performance'
                calc.prime(montant, type_prime)
            except (ValueError, IndexError):
                print("Format: montant [type] (ex: 300 performance)")
        
        # Commissions
        commission = input("Commission (0 si aucune): ").strip()
        if commission and float(commission) > 0:
            calc.commission(float(commission))
        
        # Calcul final
        result = calc.calculer()
        
        return result
        
    except (ValueError, KeyboardInterrupt):
        print("\nCalcul annulé ou erreur de saisie")
        return None


if __name__ == "__main__":
    print("=== CALCULATEUR PRATIQUE SCEM SARL ===\n")
    
    # Exemples prédéfinis
    print("1. Exemple employé standard:")
    exemple_employe_standard()
    
    print("\n\n2. Exemple commercial:")
    exemple_commercial()
    
    print("\n\n3. Exemple cadre:")
    exemple_cadre()
    
    # Proposer le calculateur interactif
    print("\n" + "="*60)
    response = input("Utiliser le calculateur interactif avancé? (o/n): ")
    if response.lower() in ['o', 'oui', 'y', 'yes']:
        calculateur_interactif_avance()