# SRM Dashboard - Plateforme d'analyse et de prédiction

# Plateforme intelligente d'analyse et d'aide à la décision — SRM-RSK

Application web développée pour la **Régie des Eaux et d'Électricité (SRM-RSK)**, permettant l'analyse, la prédiction et la génération de rapports intelligents autour de la consommation d'eau et d'électricité.

> De la donnée à la décision : analyses, prédictions et intelligence artificielle générative.

## Application en ligne

L'application est accessible directement ici, sans installation :

**[Accéder à l'application](https://srm-prediction-ai-rsk-eyuvrqfdzrwunkmmscoumb.streamlit.app)**

## Fonctionnalités

| Module | Description |
|---|---|
| Accueil | Page d'introduction à la plateforme |
| Nettoyage des données | Préparation et traitement des données brutes importées |
| Analyse des données historiques | Visualisation des tendances de consommation passées |
| KPI Actuels | Indicateurs de performance en temps réel |
| Prédiction de la consommation par agence | Modèle de machine learning prédisant la consommation future |
| KPI Prédictifs | Indicateurs basés sur les résultats des prédictions |
| Facteurs influençant la consommation prédite | Analyse des variables ayant le plus d'impact sur les prédictions |
| Rapport intelligent généré par IA | Génération automatique d'un rapport d'analyse via l'API Gemini |

## Technologies utilisées

- **Interface** : [Streamlit](https://streamlit.io/)
- **Traitement de données** : Pandas, NumPy, OpenPyXL
- **Visualisation** : Plotly
- **Machine Learning** : Scikit-learn, SHAP (interprétabilité des modèles)
- **Intelligence artificielle générative** : Google Gemini (google-genai)
- **Génération de documents** : python-docx, xhtml2pdf

## Installation en local

### Prérequis
- Python 3.10 ou supérieur
- Un compte Google AI Studio avec une clé API Gemini

### Étapes

1. Cloner le repository
```bash
git clone https://github.com/otmaniwiam8-tech/PROJET_SRM-RSK.git
cd PROJET_SRM-RSK
```

2. Installer les dépendances
```bash
pip install -r requirements.txt
```

3. Configurer la clé API

Créer un fichier `.env` à la racine du projet (voir `.env.example` pour le modèle) :
```
GEMINI_API_KEY=votre_cle_api_ici
```

4. Lancer l'application
```bash
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`.

## Structure du projet

```
SRM/
├── app.py                  # Point d'entrée de l'application
├── config.py                # Configuration générale
├── requirements.txt          # Dépendances Python
├── components/
│   ├── accueil.py            # Page d'accueil
│   ├── nettoyage.py          # Nettoyage des données
│   ├── analyse.py            # Analyse historique
│   ├── kpi.py                 # KPI actuels
│   ├── prediction.py          # Prédiction de consommation
│   ├── kpi_predictifs.py      # KPI prédictifs
│   ├── facteurs_influence.py  # Facteurs d'influence
│   ├── rapport_ia.py          # Rapport généré par IA
│   └── train_model.py         # Entraînement du modèle
├── assets/                  # Logos et ressources visuelles
└── charts.py                 # Fonctions de génération de graphiques
```

## Sécurité

Les clés API et informations sensibles sont gérées via des variables d'environnement (fichier `.env`, non versionné) et ne sont jamais exposées dans le code source.

## Auteur

Projet réalisé dans le cadre d'un stage à la SRM-RSK.