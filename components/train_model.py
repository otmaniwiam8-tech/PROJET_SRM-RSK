# components/train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def entraîner_modele(df):
    """
    Entraîne un modèle RandomForestRegressor optimisé sur les données nettoyées.
    Variables : Agence, Gerance, Annee_Facture, Mois
    """
    if df is None or df.empty:
        return None, None, None, None

    # Vérifier les colonnes nécessaires
    colonnes_requises = ['Agence', 'Gerance', 'Annee_Facture', 'Mois', 'Consommation']
    for col in colonnes_requises:
        if col not in df.columns:
            return None, None, None, None

    # Trier par année et mois (important pour TimeSeriesSplit)
    df = df.sort_values(['Annee_Facture', 'Mois']).reset_index(drop=True)

    # Séparer les features (X) et la cible (y)
    feature_cols = ['Agence', 'Gerance', 'Annee_Facture', 'Mois']
    X = df[feature_cols].copy()
    y = df['Consommation'].copy()

    # Encodage des variables catégorielles
    cat_cols = ['Agence', 'Gerance']
    encoders = {}
    for col in cat_cols:
        enc = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
        X[col] = enc.fit_transform(X[[col]])
        encoders[col] = enc

    # Validation croisée avec TimeSeriesSplit (3 splits)
    tscv = TimeSeriesSplit(n_splits=3)
    r2_scores = []
    mae_scores = []
    rmse_scores = []

    # ============================================================
    # MODÈLE RandomForest OPTIMISÉ
    # ============================================================
    for train_idx, test_idx in tscv.split(X):
        X_train = X.iloc[train_idx]
        X_test = X.iloc[test_idx]
        y_train = y.iloc[train_idx]
        y_test = y.iloc[test_idx]

        model = RandomForestRegressor(
            n_estimators=500,           # Plus d'arbres
            max_depth=15,               # Profondeur optimale
            min_samples_split=5,
            min_samples_leaf=3,
            max_features='sqrt',
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        r2_scores.append(r2_score(y_test, y_pred))
        mae_scores.append(mean_absolute_error(y_test, y_pred))
        rmse_scores.append(np.sqrt(mean_squared_error(y_test, y_pred)))

    # Métriques moyennes
    metrics = {
        'R2': round(np.mean(r2_scores), 6),
        'MAE': round(np.mean(mae_scores), 2),
        'RMSE': round(np.mean(rmse_scores), 2)
    }

    # Entraînement final sur toutes les données
    final_model = RandomForestRegressor(
        n_estimators=500,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=3,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1
    )
    final_model.fit(X, y)

    return final_model, encoders, feature_cols, metrics