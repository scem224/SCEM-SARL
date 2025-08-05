#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration des paramètres de salaire pour SCEM SARL
"""

# Taux horaires par défaut (en euros)
TAUX_HORAIRES = {
    'smic': 11.65,  # SMIC horaire 2024
    'normal': 15.0,  # Taux horaire standard
    'overtime_125': 18.75,  # 125% du taux normal
    'overtime_150': 22.50,  # 150% du taux normal
    'overtime_200': 30.00   # 200% du taux normal (jours fériés)
}

# Heures de travail légales
HEURES_TRAVAIL = {
    'hebdomadaire': 35,
    'mensuelle': 151.67,  # 35h * 52 semaines / 12 mois
    'quotidienne': 7,
    'annuelle': 1607  # 35h * 52 semaines - 5 semaines de congés
}

# Seuils pour les heures supplémentaires
SEUILS_HEURES_SUP = {
    'hebdomadaire_125': 35,  # Au-delà de 35h/semaine à 125%
    'hebdomadaire_150': 43,  # Au-delà de 43h/semaine à 150%
    'quotidienne_150': 8     # Au-delà de 8h/jour à 150%
}

# Types de primes courantes
TYPES_PRIMES = {
    'performance': 'Prime de performance',
    'anciennete': 'Prime d\'ancienneté',
    'assiduité': 'Prime d\'assiduité',
    'transport': 'Prime de transport',
    'panier': 'Prime de panier',
    'treizieme_mois': '13ème mois',
    'vacances': 'Prime de vacances',
    'objectifs': 'Prime sur objectifs'
}

# Types d'indemnités
TYPES_INDEMNITES = {
    'transport': 'Indemnité de transport',
    'repas': 'Indemnité de repas',
    'kilometrique': 'Indemnité kilométrique',
    'logement': 'Indemnité de logement',
    'telephone': 'Indemnité téléphone',
    'formation': 'Indemnité de formation'
}

# Types d'avantages en nature
TYPES_AVANTAGES = {
    'vehicule': 'Véhicule de fonction',
    'telephone': 'Téléphone portable',
    'ordinateur': 'Ordinateur portable',
    'logement': 'Logement de fonction',
    'tickets_restaurant': 'Tickets restaurant',
    'mutuelle': 'Mutuelle entreprise',
    'ce': 'Comité d\'entreprise'
}

# Barèmes de cotisations sociales (approximatifs)
COTISATIONS_SOCIALES = {
    'securite_sociale': 0.078,   # 7.8%
    'chomage': 0.024,            # 2.4%
    'retraite_complementaire': 0.0787,  # 7.87%
    'csg_crds': 0.098,          # 9.8%
    'total_approximatif': 0.23   # ~23% du brut
}

# Plafond de la sécurité sociale 2024
PLAFOND_SS = 46368  # Plafond annuel

# Configuration par défaut pour les calculs
CONFIG_DEFAUT = {
    'taux_horaire_defaut': TAUX_HORAIRES['normal'],
    'majoration_heures_sup': 1.5,
    'heures_hebdo_standard': HEURES_TRAVAIL['hebdomadaire'],
    'precision_calcul': 2  # Nombre de décimales
}

# Messages d'information
MESSAGES = {
    'salaire_defini': "Salaire de base défini: {amount}€",
    'heures_sup_ajoutees': "Heures supplémentaires ajoutées: {hours}h à {rate}x",
    'prime_ajoutee': "Prime ajoutée: {description} - {amount}€",
    'indemnite_ajoutee': "Indemnité ajoutée: {type} - {amount}€",
    'commission_definie': "Commissions définies: {amount}€",
    'avantage_ajoute': "Avantage ajouté: {description} - {value}€",
    'calcul_termine': "Salaire brut total calculé: {total}€"
}

# Validation des données
VALIDATION = {
    'salaire_min': 0.0,
    'salaire_max': 100000.0,  # Limite raisonnable pour validation
    'heures_sup_max': 220.0,  # Maximum d'heures sup par mois
    'taux_majoration_min': 1.0,
    'taux_majoration_max': 3.0
}


def get_taux_horaire(type_taux='normal'):
    """
    Obtenir un taux horaire selon le type
    
    Args:
        type_taux (str): Type de taux ('normal', 'smic', 'overtime_125', etc.)
    
    Returns:
        float: Taux horaire correspondant
    """
    return TAUX_HORAIRES.get(type_taux, TAUX_HORAIRES['normal'])


def calculer_majoration_heures_sup(heures_hebdo):
    """
    Calculer la majoration selon le nombre d'heures hebdomadaires
    
    Args:
        heures_hebdo (float): Nombre d'heures hebdomadaires
    
    Returns:
        float: Taux de majoration à appliquer
    """
    if heures_hebdo <= SEUILS_HEURES_SUP['hebdomadaire_125']:
        return 1.0  # Pas de majoration
    elif heures_hebdo <= SEUILS_HEURES_SUP['hebdomadaire_150']:
        return 1.25  # 125%
    else:
        return 1.5   # 150%


def valider_montant(montant, type_validation='salaire'):
    """
    Valider un montant selon les critères définis
    
    Args:
        montant (float): Montant à valider
        type_validation (str): Type de validation à appliquer
    
    Returns:
        bool: True si valide, False sinon
    """
    if type_validation == 'salaire':
        return VALIDATION['salaire_min'] <= montant <= VALIDATION['salaire_max']
    elif type_validation == 'heures_sup':
        return 0 <= montant <= VALIDATION['heures_sup_max']
    elif type_validation == 'taux_majoration':
        return VALIDATION['taux_majoration_min'] <= montant <= VALIDATION['taux_majoration_max']
    
    return montant >= 0  # Par défaut, juste positif


if __name__ == "__main__":
    print("=== CONFIGURATION SALAIRE SCEM SARL ===")
    print(f"SMIC horaire: {TAUX_HORAIRES['smic']}€")
    print(f"Taux normal: {TAUX_HORAIRES['normal']}€")
    print(f"Heures hebdo standard: {HEURES_TRAVAIL['hebdomadaire']}h")
    print(f"Plafond SS: {PLAFOND_SS}€/an")
    
    # Test des fonctions
    print(f"\nTaux overtime 150%: {get_taux_horaire('overtime_150')}€")
    print(f"Majoration pour 40h: {calculer_majoration_heures_sup(40)}x")
    print(f"Validation 2500€: {valider_montant(2500.0, 'salaire')}")