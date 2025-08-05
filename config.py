# Configuration pour la connexion Odoo
# Modifiez ces valeurs selon votre environnement

ODOO_CONFIG = {
    'url': 'http://localhost:8069',  # URL de votre serveur Odoo
    'db': 'your_database_name',      # Nom de votre base de données
    'username': 'your_username',     # Nom d'utilisateur Odoo
    'password': 'your_password'      # Mot de passe Odoo
}

# Configuration pour les calculs de salaire
SALARY_CONFIG = {
    'default_month': None,  # None = mois actuel
    'default_year': None,   # None = année actuelle
    'currency': 'EUR',      # Devise
    'decimal_places': 2     # Nombre de décimales pour les montants
}

# Configuration pour l'export
EXPORT_CONFIG = {
    'output_dir': './exports',  # Dossier d'export
    'format': 'json',           # Format d'export (json, csv, xlsx)
    'include_details': True     # Inclure les détails dans l'export
}