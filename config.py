# config.py
# Configuration du dashboard

COLORS = {
    'blue': '#1E88E5',
    'dark_blue': '#0D47A1',
    'orange': '#FF8F00',
    'green': '#00A86B',
    'red': '#D32F2F',
    'purple': '#6A1B9A',
    'teal': '#00897B',
    'gold': '#FFB300',
    'light_grey': '#E8ECEF',
    'dark_grey': '#0A2540'
}

PAGE_TITLE = "SRM-PREDICTION-AI"
PAGE_ICON = "💧⚡"
LAYOUT = "wide"
# Noms des colonnes possibles
CONSOMMATION_COLS = ['Consommation', 'consommation', 'CONSOMMATION']
MONTANT_COLS = ['Montant_Tete_Facture', 'Montant Tete Facture', 'montant_tete_facture']
UNITE_COLS = ['Unite_Consommation', 'unite_consommation', 'Unite_Conso']

# Unités de consommation
UNITE_EAU = ['m³', 'm3', 'M3', 'm3', 'm^3']
UNITE_ELECTRICITE = ['kWh', 'KWH', 'kwh', 'Kwh']

# Couleurs par type
COLORS_EAU = '#00897B'
COLORS_ELECTRICITE = '#1E88E5'