# components/nettoyage.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# FONCTION DE FORMATAGE DES NOMBRES
# ============================================================

def format_number(value):
    """Formate un nombre selon les règles :
    - Entier : sans décimales (ex: 12060)
    - Décimal : avec max 2 décimales (ex: 15.25)
    - Pas de séparateur de milliers
    """
    if value is None or value == "":
        return ""
    
    try:
        num = float(value)
    except (ValueError, TypeError):
        return str(value)
    
    if num == int(num):
        return str(int(num))
    
    formatted = f"{num:.2f}".rstrip('0').rstrip('.')
    return formatted

def format_number_int(value):
    """Formate un nombre en entier sans décimales"""
    if value is None or value == "":
        return ""
    
    try:
        num = float(value)
        return str(int(num))
    except (ValueError, TypeError):
        return str(value)

# ============================================================
# STYLE CSS (compatible avec les autres pages)
# ============================================================

def apply_nettoyage_style():
    st.markdown("""
    <style>
        .section-title {
            font-size: 1.4rem !important;
            font-weight: 700 !important;
            color: #FF8F00 !important;
            margin: 1.8rem 0 1rem 0 !important;
            padding: 0 !important;
            background: none !important;
            border: none !important;
        }
        .kpi-card {
            background: linear-gradient(135deg, #173B63, #1A4A7A);
            border-radius: 15px;
            padding: 1.2rem 1rem;
            border: 2px solid #2EA8FF;
            box-shadow: 0 4px 16px rgba(46, 168, 255, 0.15);
            text-align: left;
            height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            margin-bottom: 0.8rem;
        }
        .kpi-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 32px rgba(46, 168, 255, 0.25);
        }
        .kpi-card .kpi-label {
            font-size: 11px;
            font-weight: 600;
            color: #B0D4F1;
            margin-bottom: 0.2rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .kpi-card .kpi-value {
            font-size: 28px;
            font-weight: 700;
            color: #FFFFFF;
            line-height: 1.1;
        }
        .kpi-card .kpi-sub {
            font-size: 13px;
            color: #B0D4F1;
        }
        .divider {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #2EA8FF, transparent);
            margin: 1.5rem 0;
            opacity: 0.3;
        }
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
        }
        .stDataFrame thead tr th {
            background: linear-gradient(135deg, #0A2540 0%, #1A3A5C 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            padding: 0.8rem 1rem !important;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        .stDataFrame tbody td {
            background-color: #0D2B4A !important;
            color: #E2E8F0 !important;
            padding: 6px 8px !important;
            font-size: 13px !important;
        }
        .stDataFrame tbody tr:hover td {
            background-color: #1A4A7A !important;
        }
        .stButton button {
            background: linear-gradient(135deg, #1E88E5, #1565C0) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.7rem 2rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 16px rgba(30, 136, 229, 0.3) !important;
        }
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 32px rgba(30, 136, 229, 0.4) !important;
        }
        .stDownloadButton button {
            background: linear-gradient(135deg, #00A86B, #00897B) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.7rem 2rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 16px rgba(0, 168, 107, 0.3) !important;
        }
        .stDownloadButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 32px rgba(0, 168, 107, 0.4) !important;
        }
        .stSuccess {
            background-color: #1A2A1A !important;
            border-left: 4px solid #00E676 !important;
        }
        .stWarning {
            background-color: #2A1A1A !important;
            border-left: 4px solid #EF5350 !important;
        }
        .stExpander {
            background-color: #0D2B4A !important;
            border-radius: 12px !important;
            border: 1px solid rgba(46, 168, 255, 0.1) !important;
        }
        .stExpander summary {
            color: #B0D4F1 !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
        }
        .block-message {
            background: linear-gradient(135deg, #FFEBEE, #FFCDD2);
            border-radius: 16px;
            padding: 2rem 2.5rem;
            border-left: 6px solid #D32F2F;
            box-shadow: 0 4px 20px rgba(211, 47, 47, 0.15);
            text-align: center;
            margin: 2rem 0;
        }
        .block-message h2 {
            color: #B71C1C !important;
            font-size: 1.8rem !important;
            font-weight: 800 !important;
            background: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            display: block !important;
        }
        .block-message p {
            color: #1A237E;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        .block-message .icon {
            font-size: 4rem;
            margin-bottom: 0.5rem;
        }
        .block-message .btn-container {
            margin-top: 1.5rem;
        }
        .stSpinner > div {
            border-color: #1E88E5 !important;
        }
        .stInfo {
            background-color: #1A2A3A !important;
            border-left: 4px solid #1E88E5 !important;
            color: #B0D4F1 !important;
        }
        .stInfo .stMarkdown {
            color: #B0D4F1 !important;
        }
        .card-orange {
            border-color: #FF8F00 !important;
        }
        .card-orange .kpi-label {
            color: #FFB74D !important;
        }
        .card-orange .kpi-value {
            color: #FFB74D !important;
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# FONCTIONS DE NETTOYAGE (avec cache)
# ============================================================

@st.cache_data
def clean_data(df):
    """Nettoie le dataset selon les règles définies (avec cache)"""
    if df is None or df.empty:
        return None
    
    df_clean = df.copy()
    
    # Renommage des colonnes
    standard_cols = {
        'Agence': ['Agence', 'agence', 'AGENCE'],
        'Gerance': ['Gerance', 'gerance', 'GERANCE', 'Gérance'],
        'Annee_Facture': ['Annee_Facture', 'Année_Facture', 'Annee', 'ANNEE', 'Year'],
        'Mois': ['Mois', 'mois', 'MOIS', 'Month', 'month'],
        'Consommation': ['Consommation', 'consommation', 'CONSOMMATION', 'Conso'],
        'Unite_Consommation': ['Unite_Consommation', 'Unite', 'unite', 'UNITE', 'Unit'],
        'Montant_Tete_Facture': ['Montant_Tete_Facture', 'Montant', 'montant', 'MONTANT'],
        'Hors_Taxe': ['Hors_Taxe', 'HT', 'Hors Taxe'],
        'TVA': ['TVA', 'Tva', 'tva'],
        'TTC': ['TTC', 'Ttc', 'ttc'],
        'Type_Client': ['Type_Client', 'Type', 'type', 'TYPE'],
        'ID_Client': ['ID_Client', 'Client_ID', 'id_client']
    }
    
    rename_map = {}
    for standard, variants in standard_cols.items():
        for variant in variants:
            if variant in df_clean.columns:
                rename_map[variant] = standard
                break
    if rename_map:
        df_clean = df_clean.rename(columns=rename_map)
    
    # Vérification des colonnes essentielles
    colonnes_essentielles = ['Agence', 'Gerance', 'Annee_Facture', 'Mois', 'Consommation']
    manquantes = [c for c in colonnes_essentielles if c not in df_clean.columns]
    if manquantes:
        return None
    
    # Conversion des types
    if 'Date_Facture' in df_clean.columns:
        df_clean['Date_Facture'] = pd.to_datetime(df_clean['Date_Facture'], errors='coerce')
    else:
        df_clean['Date_Facture'] = pd.to_datetime(
            df_clean['Annee_Facture'].astype(str) + '-' + df_clean['Mois'].astype(str) + '-01',
            errors='coerce'
        )
    
    numeric_cols = ['Annee_Facture', 'Mois', 'Consommation', 'Montant_Tete_Facture', 'Hors_Taxe', 'TVA', 'TTC']
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    cat_cols = ['Type_Client', 'Gerance', 'Agence', 'Unite_Consommation']
    for col in cat_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
    
    # Suppression des valeurs manquantes critiques
    cols_critiques = ['Agence', 'Annee_Facture', 'Consommation']
    cols_presentes = [c for c in cols_critiques if c in df_clean.columns]
    if cols_presentes:
        df_clean = df_clean.dropna(subset=cols_presentes)
    
    # Remplissage secondaire
    if 'Mois' in df_clean.columns:
        df_clean['Mois'] = df_clean['Mois'].fillna(df_clean['Mois'].median())
    
    for col in ['Montant_Tete_Facture', 'Hors_Taxe', 'TVA', 'TTC']:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    
    for col in ['Type_Client']:
        if col in df_clean.columns:
            mode_val = df_clean[col].mode()
            if not mode_val.empty:
                df_clean[col] = df_clean[col].fillna(mode_val[0])
    
    df_clean = df_clean.drop_duplicates()
    if 'Consommation' in df_clean.columns:
        df_clean = df_clean[df_clean['Consommation'] >= 0]
    
    df_clean = df_clean.reset_index(drop=True)
    return df_clean

# ============================================================
# PAGE PRINCIPALE
# ============================================================

def render_nettoyage(df):
    """Affiche la page de nettoyage avec style compatible"""
    
    apply_nettoyage_style()
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.2rem; font-weight: 700; color: #FFFFFF; margin: 0; padding: 0;">🧹 Nettoyage et préparation des données</h1>
        <p style="font-size: 1.1rem; color: #94A3B8; margin: 0.2rem 0 0 0;">
            Préparation des données avant analyse et entraînement du modèle
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if df is None:
        st.warning("⚠️ Veuillez d'abord importer un fichier dans la barre latérale.")
        st.stop()
    
    # ============================================================
    # STATISTIQUES RAPIDES
    # ============================================================
    st.markdown('<h2 class="section-title">📊 Statistiques du fichier</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card card-orange">
            <div class="kpi-label">📥 LIGNES</div>
            <div class="kpi-value">{format_number_int(df.shape[0])}</div>
            <div class="kpi-sub">lignes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card card-orange">
            <div class="kpi-label">📊 COLONNES</div>
            <div class="kpi-value">{format_number_int(df.shape[1])}</div>
            <div class="kpi-sub">colonnes</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============================================================
    # APERÇU DES DONNÉES AVANT NETTOYAGE (TOUTES LES LIGNES)
    # ============================================================
    with st.expander("📋 Aperçu des données avant nettoyage", expanded=False):
        st.caption(f"📌 Affichage de toutes les lignes ({format_number_int(df.shape[0])} lignes)")
        st.data_editor(
            df,
            use_container_width=True,
            height=500,
            disabled=True,
            hide_index=False,
            num_rows="fixed"
        )
    
    st.markdown("---")
    
    # ============================================================
    # BOUTON DE NETTOYAGE
    # ============================================================
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        nettoyer = st.button("🧹 Lancer le nettoyage", type="primary", use_container_width=True)
    
    if nettoyer:
        with st.spinner("🔄 Nettoyage en cours... Veuillez patienter..."):
            try:
                df_clean = clean_data(df)
                if df_clean is None:
                    st.error("❌ Le nettoyage a échoué. Vérifiez les colonnes.")
                    st.stop()
                
                st.markdown("---")
                
                # ============================================================
                # RÉSUMÉ DU NETTOYAGE
                # ============================================================
                st.markdown('<h2 class="section-title">📊 Résumé du nettoyage</h2>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="kpi-card" style="border-color: #EF5350;">
                        <div class="kpi-label" style="color: #EF5350;">📥 AVANT</div>
                        <div class="kpi-value" style="color: #EF5350;">{format_number_int(df.shape[0])}</div>
                        <div class="kpi-sub">lignes</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="kpi-card" style="border-color: #00E676;">
                        <div class="kpi-label" style="color: #00E676;">📤 APRÈS</div>
                        <div class="kpi-value" style="color: #00E676;">{format_number_int(df_clean.shape[0])}</div>
                        <div class="kpi-sub">lignes</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    supprimees = df.shape[0] - df_clean.shape[0]
                    st.markdown(f"""
                    <div class="kpi-card" style="border-color: #FF8F00;">
                        <div class="kpi-label" style="color: #FFB74D;">🗑️ SUPPRIMÉES</div>
                        <div class="kpi-value" style="color: #FFB74D;">{format_number_int(supprimees)}</div>
                        <div class="kpi-sub">lignes</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.session_state.df_clean = df_clean
                
                # ============================================================
                # ENTRAÎNEMENT AUTOMATIQUE DU MODÈLE (sans messages)
                # ============================================================
                try:
                    from components.train_model import entraîner_modele
                    with st.spinner("🔄 Entraînement du modèle en cours..."):
                        modele, encodeurs, colonnes, metrics = entraîner_modele(df_clean)
                        if modele is not None:
                            st.session_state.modele = modele
                            st.session_state.encodeurs = encodeurs
                            st.session_state.colonnes_modele = colonnes
                            st.session_state.modele_entraine = True
                            st.session_state.metriques_modele = metrics
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'entraînement : {e}")
                
                st.markdown("---")
                
                # ============================================================
                # APERÇU DES DONNÉES NETTOYÉES (TOUTES LES LIGNES)
                # ============================================================
                with st.expander("📊 Aperçu des données nettoyées", expanded=False):
                    st.caption(f"📌 Affichage de toutes les lignes ({format_number_int(df_clean.shape[0])} lignes)")
                    st.data_editor(
                        df_clean,
                        use_container_width=True,
                        height=500,
                        disabled=True,
                        hide_index=False,
                        num_rows="fixed"
                    )
                
                st.info(f"📊 **Total : {format_number_int(df_clean.shape[0])} lignes** sur {format_number_int(df_clean.shape[1])} colonnes")
                
                # ============================================================
                # TÉLÉCHARGEMENT
                # ============================================================
                csv = df_clean.to_csv(index=False).encode('utf-8')
                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                with col_btn2:
                    st.download_button(
                        label="📥 Télécharger les données nettoyées (CSV)",
                        data=csv,
                        file_name="donnees_nettoyees.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
            except Exception as e:
                st.error(f"❌ Erreur lors du nettoyage : {e}")