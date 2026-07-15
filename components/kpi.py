# components/kpi.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from config import COLORS, CONSOMMATION_COLS, MONTANT_COLS, UNITE_COLS, UNITE_EAU, UNITE_ELECTRICITE

# ============================================================
# FONCTIONS DE FORMATAGE DES NOMBRES
# ============================================================

def format_number(value):
    """
    Formate un nombre selon les règles :
    - Entier : affiché sans décimales (ex: 12060)
    - Décimal : affiché avec max 2 décimales (ex: 15.25)
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
    """Formate un nombre en entier (sans décimales)"""
    if value is None or value == "":
        return ""
    try:
        num = float(value)
        return str(int(num))
    except (ValueError, TypeError):
        return str(value)

# ============================================================
# STYLE CSS
# ============================================================

def apply_kpi_style():
    st.markdown("""
    <style>
        /* Titres généraux */
        .section-title {
            font-size: 1.4rem !important;
            font-weight: 700 !important;
            color: #FF8F00 !important;
            margin: 1.8rem 0 1rem 0 !important;
            padding: 0 !important;
            background: none !important;
            border: none !important;
        }
        .graph-title {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #6A1B9A !important;
            text-align: center !important;
            margin-bottom: 0.5rem !important;
        }
        /* === CARTES KPI MÉTIER : ORANGE === */
        .kpi-card {
            background: linear-gradient(135deg, #173B63, #1A4A7A);
            border-radius: 15px;
            padding: 1.2rem 1rem;
            border: 2px solid #FF8F00;  /* ORANGE */
            box-shadow: 0 4px 16px rgba(255, 143, 0, 0.15);
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
            box-shadow: 0 8px 32px rgba(255, 143, 0, 0.25);
        }
        .kpi-card .kpi-label {
            font-size: 11px;
            font-weight: 600;
            color: #FFB74D;  /* orange clair */
            margin-bottom: 0.2rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .kpi-card .kpi-value {
            font-size: 28px;
            font-weight: 700;
            color: #FF8F00;  /* orange */
            line-height: 1.1;
        }
        .kpi-card .kpi-sub {
            font-size: 13px;
            color: #B0D4F1;
        }
        /* === FIN CARTES ORANGE === */

        .info-note {
            background: #1E293B;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            border: 1px solid #2A3441;
            text-align: center;
            color: #94A3B8;
            font-size: 14px;
        }
        .divider {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #2EA8FF, transparent);
            margin: 1.5rem 0;
            opacity: 0.3;
        }
        .section-divider {
            border: none;
            height: 3px;
            background: linear-gradient(90deg, #1E88E5, #FF8F00, #1E88E5);
            margin: 2rem 0;
            border-radius: 5px;
            opacity: 0.5;
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
        /* === TITRES CONSOMMATION : ROUGE / BLEU (inchangés) === */
        .section-title-electricite {
            color: #FFFFFF !important;
            font-size: 1.6rem !important;
            font-weight: 700 !important;
            margin: 1.5rem 0 1rem 0 !important;
            padding: 0.5rem 1.2rem !important;
            background: linear-gradient(135deg, #B71C1C 0%, #D32F2F 100%) !important;
            border-radius: 10px !important;
            display: inline-block !important;
            box-shadow: 0 4px 12px rgba(183, 28, 28, 0.3) !important;
        }
        .section-title-eau {
            color: #FFFFFF !important;
            font-size: 1.6rem !important;
            font-weight: 700 !important;
            margin: 1.5rem 0 1rem 0 !important;
            padding: 0.5rem 1.2rem !important;
            background: linear-gradient(135deg, #0D47A1 0%, #1E88E5 100%) !important;
            border-radius: 10px !important;
            display: inline-block !important;
            box-shadow: 0 4px 12px rgba(13, 71, 161, 0.3) !important;
        }
        /* ============================================ */

        .stSelectbox label, .stNumberInput label {
            font-size: 1rem !important;
            font-weight: 600 !important;
            color: #B0D4F1 !important;
        }
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
            border: 1px solid rgba(0,0,0,0.04);
        }
        .stDataFrame thead tr th {
            background: linear-gradient(135deg, #0A2540 0%, #1A3A5C 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            padding: 0.8rem 1rem !important;
        }
        .stCaption {
            color: #94A3B8 !important;
            font-size: 0.9rem !important;
        }
        .filter-label {
            font-weight: 600;
            color: #B0D4F1;
            font-size: 1rem;
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
        .stSubheader {
            color: #B0D4F1 !important;
            font-size: 1.3rem !important;
            font-weight: 600 !important;
            margin-top: 1.5rem !important;
        }
        .stAlert {
            background-color: #1E293B !important;
            color: #B0D4F1 !important;
            border-left: 4px solid #2EA8FF !important;
        }
        .stAlert .stMarkdown {
            color: #B0D4F1 !important;
        }
        .stWarning {
            background-color: #2A1A1A !important;
            border-left: 4px solid #EF5350 !important;
        }
        .stInfo {
            background-color: #1A2A3A !important;
            border-left: 4px solid #1E88E5 !important;
        }
        .stSuccess {
            background-color: #1A2A1A !important;
            border-left: 4px solid #00E676 !important;
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
        .stRadio label {
            color: #B0D4F1 !important;
            font-weight: 500 !important;
        }
        .stRadio [data-testid="stMarkdownContainer"] {
            color: #B0D4F1 !important;
        }
        .stMetric {
            background: linear-gradient(135deg, #0D2B4A, #1A4A7A) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            border: 1px solid rgba(46, 168, 255, 0.1) !important;
        }
        .stMetric .stMetricValue {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }
        .stMetric .stMetricLabel {
            color: #B0D4F1 !important;
            font-weight: 500 !important;
        }
        .stMetric .stMetricDelta {
            color: #00E676 !important;
        }
        .category-title {
            color: #FF8F00 !important;
            font-size: 1.4rem !important;
            font-weight: 700 !important;
            margin: 1rem 0 0.5rem 0 !important;
            padding-bottom: 0.2rem !important;
            border-bottom: 3px solid #FF8F00 !important;
            display: inline-block !important;
        }
        .category-icon {
            font-size: 1.3rem !important;
            margin-right: 0.3rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def filtrer_par_gerance(df, col_unite, choix):
    if col_unite is None or col_unite not in df.columns:
        return df, False
    if choix == "⚡ Électricité":
        mask = df[col_unite].astype(str).str.lower().isin([u.lower() for u in UNITE_ELECTRICITE])
    else:
        mask = df[col_unite].astype(str).str.lower().isin([u.lower() for u in UNITE_EAU])
    df_filtre = df[mask].copy()
    return df_filtre, df_filtre.empty

def apply_graph_style(fig, title, x_title="", y_title="", height=400, bargap=0.3):
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=14, color='#B0D4F1', family='Arial, sans-serif', weight='bold')),
            tickfont=dict(size=12, color='#B0D4F1', family='Arial, sans-serif'),
            gridcolor='rgba(255,255,255,0.05)',
            gridwidth=0.5,
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=14, color='#B0D4F1', family='Arial, sans-serif', weight='bold')),
            tickfont=dict(size=12, color='#B0D4F1', family='Arial, sans-serif'),
            gridcolor='rgba(255,255,255,0.05)',
            gridwidth=0.5,
            showgrid=True,
            zeroline=True,
            zerolinecolor='rgba(255,255,255,0.1)',
            zerolinewidth=1
        ),
        plot_bgcolor='#111827',
        paper_bgcolor='#111827',
        height=height,
        margin=dict(l=60, r=40, t=60, b=60),
        bargap=bargap
    )
    return fig

# ============================================================
# FONCTION PRINCIPALE
# ============================================================

def render_kpi(df):
    apply_kpi_style()
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.2rem; font-weight: 700; color: #FFFFFF; margin: 0; padding: 0;">📈 KPI Actuels</h1>
        <p style="font-size: 1.1rem; color: #94A3B8; margin: 0.2rem 0 0 0;">
            Indicateurs clés de performance sur les données réelles
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if df is None:
        st.warning("⚠️ Veuillez d'abord importer un fichier dans la barre latérale.")
        st.stop()
    
    if st.session_state.df_clean is None:
        st.markdown("""
        <div class="block-message">
            <div class="icon">🚨</div>
            <h2>Données non nettoyées</h2>
            <p>
                Vous devez <strong>obligatoirement</strong> passer par la page <br>
                <strong style="color:#0D47A1; font-size:1.2rem;">'Nettoyage des données'</strong> <br>
                avant d'accéder aux KPI.
            </p>
            <p style="font-size:0.95rem; color:#5A6C7D;">
                ⚠️ Les données brutes contiennent des valeurs manquantes, des doublons et des incohérences.<br>
                Les KPI ne seront pas fiables sans un nettoyage préalable.
            </p>
            <div class="btn-container">
        """, unsafe_allow_html=True)
        if st.button("🧹 Aller au nettoyage des données", type="primary"):
            st.session_state.page = "🧹 Nettoyage des données"
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)
        st.stop()
    
    df = st.session_state.df_clean
    st.success("✅ Utilisation des données nettoyées")
    
    # Identification des colonnes
    col_consommation = None
    for col in ['Consommation', 'consommation', 'CONSOMMATION']:
        if col in df.columns:
            col_consommation = col
            break
    
    col_montant = None
    for col in ['Montant_Tete_Facture', 'Montant Tete Facture', 'montant_tete_facture']:
        if col in df.columns:
            col_montant = col
            break
    
    col_unite = None
    for col in ['Unite_Consommation', 'unite_consommation']:
        if col in df.columns:
            col_unite = col
            break
    
    col_ht = None
    for col in ['Hors_Taxe', 'Hors Taxe', 'HT']:
        if col in df.columns:
            col_ht = col
            break
    col_tva = 'TVA' if 'TVA' in df.columns else None
    col_ttc = 'TTC' if 'TTC' in df.columns else None
    
    # ============================================================
    # FILTRE GÉRANCE POUR KPI MÉTIER ET FINANCIERS
    # ============================================================
    st.markdown('<p style="color: #FF8F00; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.5rem;">⚙️ Sélection de la gérance pour les KPI Métier et Financiers</p>', unsafe_allow_html=True)
    
    choix_gerance = st.radio(
        "Choisissez la gérance :",
        ["⚡ Électricité", "💧 Eau"],
        index=0,
        key="gerance_metier_financier",
        horizontal=True
    )
    
    df_metier_financier, vide = filtrer_par_gerance(df, col_unite, choix_gerance)
    if vide:
        st.warning(f"⚠️ Aucune donnée trouvée pour {choix_gerance}. Utilisation de toutes les données.")
        df_metier_financier = df
    
    st.info(f"📊 Affichage des KPI Métier et Financiers pour **{choix_gerance}** ({format_number_int(df_metier_financier.shape[0])} lignes)")
    
    # ============================================================
    # SECTION 1 : KPI MÉTIER (cartes orange)
    # ============================================================
    st.markdown('<div class="category-title"><span class="category-icon">📊</span>KPI Métier</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        nb_clients = df_metier_financier['ID_Client'].nunique() if 'ID_Client' in df_metier_financier.columns else df_metier_financier.shape[0]
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">👤 CLIENTS</div>
            <div class="kpi-value">{format_number_int(nb_clients)}</div>
            <div class="kpi-sub">clients</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📄 FACTURES</div>
            <div class="kpi-value">{format_number_int(df_metier_financier.shape[0])}</div>
            <div class="kpi-sub">factures</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        nb_agences = df_metier_financier['Agence'].nunique() if 'Agence' in df_metier_financier.columns else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📍 AGENCES</div>
            <div class="kpi-value">{format_number_int(nb_agences)}</div>
            <div class="kpi-sub">agences</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        nb_gerances = df_metier_financier['Gerance'].nunique() if 'Gerance' in df_metier_financier.columns else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">🏢 GÉRANCES</div>
            <div class="kpi-value">{format_number_int(nb_gerances)}</div>
            <div class="kpi-sub">gérances</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        nb_types = df_metier_financier['Type_Client'].nunique() if 'Type_Client' in df_metier_financier.columns else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">👥 TYPES</div>
            <div class="kpi-value">{format_number_int(nb_types)}</div>
            <div class="kpi-sub">types</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============================================================
    # SÉPARATION EAU / ÉLECTRICITÉ POUR LES CONSOMMATIONS
    # ============================================================
    if col_unite is not None:
        df_eau, _ = filtrer_par_gerance(df, col_unite, "💧 Eau")
        df_elec, _ = filtrer_par_gerance(df, col_unite, "⚡ Électricité")
    else:
        df_eau, df_elec = df, df
    
    df_elec_clean = df_elec.dropna(subset=[col_consommation]) if col_consommation is not None else pd.DataFrame()
    df_eau_clean = df_eau.dropna(subset=[col_consommation]) if col_consommation is not None else pd.DataFrame()
    
    # ============================================================
    # SECTION 2 : KPI CONSOMMATION ÉLECTRICITÉ (titre inchangé)
    # ============================================================
    if col_consommation:
        st.markdown('<h2 class="section-title-electricite">⚡ Consommation Électrique</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color:#94A3B8; font-size:0.85rem;">Unités : kilowattheures (kWh)</p>', unsafe_allow_html=True)
        
        if not df_elec_clean.empty:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("⚡ Totale", f"{format_number(df_elec_clean[col_consommation].sum())} kWh")
            col2.metric("📊 Moyenne", f"{format_number(df_elec_clean[col_consommation].mean())} kWh")
            col3.metric("📈 Max", f"{format_number(df_elec_clean[col_consommation].max())} kWh")
            col4.metric("📉 Min", f"{format_number(df_elec_clean[col_consommation].min())} kWh")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("🎯 Médiane", f"{format_number(df_elec_clean[col_consommation].median())} kWh")
            col2.metric("📊 Écart-type", f"{format_number(df_elec_clean[col_consommation].std())} kWh")
            if df_elec_clean[col_consommation].max() > 0:
                coeff = (df_elec_clean[col_consommation].mean() / df_elec_clean[col_consommation].max()) * 100
            else:
                coeff = 0
            col3.metric("📈 Coeff. utilisation", f"{format_number(coeff)}%")
        else:
            st.info("💡 Aucune donnée de consommation électrique trouvée")
    
    # ============================================================
    # SECTION 3 : KPI CONSOMMATION EAU (titre inchangé)
    # ============================================================
    if col_consommation:
        st.markdown('<h2 class="section-title-eau">💧 Consommation d\'Eau</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color:#94A3B8; font-size:0.85rem;">Unités : mètres cubes (m³)</p>', unsafe_allow_html=True)
        
        if not df_eau_clean.empty:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("💧 Totale", f"{format_number(df_eau_clean[col_consommation].sum())} m³")
            col2.metric("📊 Moyenne", f"{format_number(df_eau_clean[col_consommation].mean())} m³")
            col3.metric("📈 Max", f"{format_number(df_eau_clean[col_consommation].max())} m³")
            col4.metric("📉 Min", f"{format_number(df_eau_clean[col_consommation].min())} m³")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("🎯 Médiane", f"{format_number(df_eau_clean[col_consommation].median())} m³")
            col2.metric("📊 Écart-type", f"{format_number(df_eau_clean[col_consommation].std())} m³")
            if df_eau_clean[col_consommation].max() > 0:
                coeff = (df_eau_clean[col_consommation].mean() / df_eau_clean[col_consommation].max()) * 100
            else:
                coeff = 0
            col3.metric("📈 Coeff. utilisation", f"{format_number(coeff)}%")
        else:
            st.info("💡 Aucune donnée de consommation d'eau trouvée")
    
    st.markdown("---")
    
    # ============================================================
    # SECTION 4 : KPI FINANCIERS (filtré)
    # ============================================================
    with st.expander("💰 KPI Financiers", expanded=True):
        if col_ht is not None and col_ttc is not None:
            col1, col2, col3 = st.columns(3)
            col1.metric("💰 HT", f"{format_number(df_metier_financier[col_ht].sum())} MAD")
            col2.metric("📊 TVA", f"{format_number(df_metier_financier[col_tva].sum())} MAD" if col_tva else "-")
            col3.metric("💰 TTC", f"{format_number(df_metier_financier[col_ttc].sum())} MAD")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("📊 Facture moyenne", f"{format_number(df_metier_financier[col_ttc].mean())} MAD")
            col2.metric("📈 Facture max", f"{format_number(df_metier_financier[col_ttc].max())} MAD")
            col3.metric("📉 Facture min", f"{format_number(df_metier_financier[col_ttc].min())} MAD")
        elif col_montant is not None:
            col1, col2, col3 = st.columns(3)
            col1.metric("💰 Montant total", f"{format_number(df_metier_financier[col_montant].sum())} MAD")
            col2.metric("📊 Facture moyenne", f"{format_number(df_metier_financier[col_montant].mean())} MAD")
            col3.metric("📈 Facture max", f"{format_number(df_metier_financier[col_montant].max())} MAD")
            
            col1, col2 = st.columns(2)
            col1.metric("📉 Facture min", f"{format_number(df_metier_financier[col_montant].min())} MAD")
            col2.metric("📊 Écart-type", f"{format_number(df_metier_financier[col_montant].std())} MAD")
        else:
            st.warning("⚠️ Colonne de montant non trouvée")
    
    # ============================================================
    # SECTION 5 : ÉVOLUTION ANNUELLE (couleur des barres modifiée)
    # ============================================================
    with st.expander("📈 Évolution Annuelle", expanded=True):
        if col_consommation and 'Annee_Facture' in df.columns:
            st.markdown('<p style="color: #FF8F00; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">⚙️ Sélection de la gérance pour l\'évolution</p>', unsafe_allow_html=True)
            
            choix_evo = st.radio(
                "Choisissez la gérance :",
                ["⚡ Électricité", "💧 Eau"],
                index=0,
                key="gerance_evolution",
                horizontal=True
            )
            
            df_evo, vide_evo = filtrer_par_gerance(df, col_unite, choix_evo)
            if vide_evo:
                st.warning(f"⚠️ Aucune donnée pour {choix_evo}.")
            else:
                df_evo_clean = df_evo.dropna(subset=[col_consommation])
                if not df_evo_clean.empty:
                    unite = "kWh" if choix_evo == "⚡ Électricité" else "m³"
                    # COULEUR MODIFIÉE ICI
                    couleur = '#811F1F' if choix_evo == "⚡ Électricité" else '#2E6494'
                    prefix = "électrique" if choix_evo == "⚡ Électricité" else "d'eau"
                    
                    df_hist = df_evo_clean.groupby('Annee_Facture')[col_consommation].sum().reset_index()
                    df_hist = df_hist.sort_values('Annee_Facture')
                    df_hist['Evolution'] = df_hist[col_consommation].pct_change() * 100
                    df_hist['Evolution'] = df_hist['Evolution'].fillna(0)
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=df_hist['Annee_Facture'],
                        y=df_hist[col_consommation],
                        marker_color=couleur,
                        text=df_hist[col_consommation].apply(lambda x: f"{format_number(x)} {unite}"),
                        textposition='outside',
                        textfont=dict(size=12, color='#FFFFFF', weight='bold')
                    ))
                    fig = apply_graph_style(
                        fig,
                        title=f'Consommation {prefix} par année',
                        x_title='Année',
                        y_title=f'Consommation ({unite})',
                        height=300
                    )
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("💡 Aucune donnée disponible pour cette gérance")
        else:
            st.warning("⚠️ Données insuffisantes pour l'évolution annuelle")
    
    # ============================================================
    # SECTION 6 : TAUX D'ÉVOLUTION PAR AGENCE (couleur modifiée)
    # ============================================================
    with st.expander("📈 Taux d'évolution par agence et gérance", expanded=True):
        if col_consommation and 'Annee_Facture' in df.columns and 'Agence' in df.columns:
            
            st.markdown('<p style="color: #FF8F00; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">🔍 Filtres d\'analyse</p>', unsafe_allow_html=True)
            
            type_energie_local = st.selectbox(
                "⚡ Énergie",
                ["Électricité", "Eau"],
                index=0,
                key="kpi_type_energie_evo"
            )
            
            df_filtre_type, vide = filtrer_par_gerance(df, col_unite, "⚡ " + type_energie_local if type_energie_local == "Électricité" else "💧 " + type_energie_local)
            if vide:
                st.warning(f"⚠️ Aucune donnée trouvée pour {type_energie_local}.")
            else:
                if type_energie_local == "Électricité":
                    unite_label = "kWh"
                    # COULEUR MODIFIÉE ICI
                    color_theme = '#811F1F'
                else:
                    unite_label = "m³"
                    # COULEUR MODIFIÉE ICI
                    color_theme = '#2E6494'
                
                col_f1, col_f2, col_f3 = st.columns(3)
                
                with col_f1:
                    agences_list = ['Toutes les agences'] + sorted([str(x) for x in df_filtre_type['Agence'].unique().tolist() if pd.notna(x)])
                    agence_selected = st.selectbox("📍 Agence", agences_list, key="kpi_agence_evo")
                
                with col_f2:
                    periode_type = st.selectbox(
                        "📊 Période",
                        ["Annuelle", "Mensuelle"],
                        key="kpi_periode_evo"
                    )
                
                with col_f3:
                    if periode_type == "Mensuelle":
                        annees_dispo = sorted([str(x) for x in df_filtre_type['Annee_Facture'].unique().tolist() if pd.notna(x)])
                        annee_selected = st.selectbox("📅 Année", annees_dispo, key="kpi_annee_evo")
                    else:
                        annee_selected = None
                
                st.markdown("---")
                
                df_evo = df_filtre_type.copy()
                
                if agence_selected != "Toutes les agences":
                    df_evo = df_evo[df_evo['Agence'].astype(str) == agence_selected]
                
                if col_unite is not None:
                    if type_energie_local == "Électricité":
                        df_evo = df_evo[df_evo[col_unite].astype(str).str.lower().isin([u.lower() for u in UNITE_ELECTRICITE])]
                    else:
                        df_evo = df_evo[df_evo[col_unite].astype(str).str.lower().isin([u.lower() for u in UNITE_EAU])]
                
                if df_evo.empty:
                    st.warning(f"⚠️ Aucune donnée pour les filtres sélectionnés ({type_energie_local}).")
                else:
                    if periode_type == "Annuelle":
                        st.markdown(f'<p style="color: #6A1B9A; font-size: 1.1rem; font-weight: 600; text-align: center;">📊 Taux d\'évolution annuel – {type_energie_local}</p>', unsafe_allow_html=True)
                        
                        if agence_selected == "Toutes les agences":
                            df_hist = df_evo.groupby(['Annee_Facture', 'Agence'])[col_consommation].sum().reset_index()
                            df_hist = df_hist.sort_values(['Agence', 'Annee_Facture'])
                            df_hist['Evolution'] = df_hist.groupby('Agence')[col_consommation].pct_change() * 100
                            df_hist['Evolution'] = df_hist['Evolution'].fillna(0)
                            
                            fig = go.Figure()
                            if type_energie_local == "Électricité":
                                palette = ['#D32F2F', '#EF5350', '#FF1744', '#B71C1C', '#C62828', '#D50000', '#F44336', '#E53935']
                            else:
                                palette = ['#0D47A1', '#1E88E5', '#42A5F5', '#1565C0', '#1976D2', '#0D47A1', '#2196F3', '#64B5F6']
                            
                            for i, agence in enumerate(df_hist['Agence'].unique()):
                                temp = df_hist[df_hist['Agence'] == agence]
                                fig.add_trace(go.Scatter(
                                    x=temp['Annee_Facture'],
                                    y=temp['Evolution'],
                                    mode='lines+markers',
                                    name=str(agence),
                                    line=dict(color=palette[i % len(palette)], width=2.5),
                                    marker=dict(size=10)
                                ))
                            
                            fig = apply_graph_style(
                                fig,
                                title=f"Taux d'évolution annuel par agence – {type_energie_local}",
                                x_title="Année",
                                y_title="Taux d'évolution (%)",
                                height=400
                            )
                            fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5, font=dict(color='#E2E8F0')))
                            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                        
                        else:
                            df_hist = df_evo.groupby('Annee_Facture')[col_consommation].sum().reset_index()
                            df_hist = df_hist.sort_values('Annee_Facture')
                            df_hist['Evolution'] = df_hist[col_consommation].pct_change() * 100
                            df_hist['Evolution'] = df_hist['Evolution'].fillna(0)
                            
                            colors_evo = ['#00E676' if x >= 0 else '#EF5350' for x in df_hist['Evolution']]
                            fig = go.Figure()
                            fig.add_trace(go.Bar(
                                x=df_hist['Annee_Facture'],
                                y=df_hist['Evolution'],
                                marker_color=colors_evo,
                                text=df_hist['Evolution'].apply(lambda x: f"{format_number(x)}%"),
                                textposition='outside',
                                textfont=dict(size=12, color='#FFFFFF', weight='bold')
                            ))
                            
                            fig = apply_graph_style(
                                fig,
                                title=f"Taux d'évolution annuel – {agence_selected} ({type_energie_local})",
                                x_title="Année",
                                y_title="Taux d'évolution (%)",
                                height=400,
                                bargap=0.3
                            )
                            fig.update_layout(showlegend=False)
                            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                            
                            df_hist_formatted = df_hist[['Annee_Facture', col_consommation, 'Evolution']].copy()
                            df_hist_formatted[col_consommation] = df_hist_formatted[col_consommation].apply(lambda x: format_number(x))
                            df_hist_formatted['Evolution'] = df_hist_formatted['Evolution'].apply(lambda x: f"{x:+.1f}%")
                            
                            st.dataframe(
                                df_hist_formatted.rename(columns={col_consommation: 'Consommation', 'Evolution': "Taux d'évolution (%)"})
                                .style.set_properties(**{'background-color': '#0D2B4A', 'color': '#E2E8F0'})
                                .set_table_styles([{'selector': 'thead th', 'props': [('background-color', '#1A4A7A'), ('color', 'white'), ('font-weight', 'bold')]}])
                            )
                    
                    else:  # Mensuelle
                        if 'Mois' not in df_evo.columns:
                            st.warning("⚠️ Colonne 'Mois' non trouvée pour l'analyse mensuelle.")
                        else:
                            st.markdown(f'<p style="color: #6A1B9A; font-size: 1.1rem; font-weight: 600; text-align: center;">📊 Consommation mensuelle – {annee_selected} ({type_energie_local})</p>', unsafe_allow_html=True)
                            df_annee = df_evo[df_evo['Annee_Facture'].astype(str) == annee_selected]
                            if df_annee.empty:
                                st.warning(f"⚠️ Aucune donnée pour l'année {annee_selected}.")
                            else:
                                if agence_selected == "Toutes les agences":
                                    df_mois = df_annee.groupby(['Mois', 'Agence'])[col_consommation].sum().reset_index()
                                    df_mois = df_mois.sort_values(['Agence', 'Mois'])
                                    fig = go.Figure()
                                    if type_energie_local == "Électricité":
                                        palette = ['#D32F2F', '#EF5350', '#FF1744', '#B71C1C', '#C62828', '#D50000', '#F44336', '#E53935']
                                    else:
                                        palette = ['#0D47A1', '#1E88E5', '#42A5F5', '#1565C0', '#1976D2', '#0D47A1', '#2196F3', '#64B5F6']
                                    
                                    for i, agence in enumerate(df_mois['Agence'].unique()):
                                        temp = df_mois[df_mois['Agence'] == agence]
                                        fig.add_trace(go.Scatter(
                                            x=temp['Mois'],
                                            y=temp[col_consommation],
                                            mode='lines+markers',
                                            name=str(agence),
                                            line=dict(color=palette[i % len(palette)], width=2.5),
                                            marker=dict(size=8)
                                        ))
                                    
                                    fig = apply_graph_style(
                                        fig,
                                        title=f"Consommation mensuelle par agence – {annee_selected} ({type_energie_local})",
                                        x_title="Mois",
                                        y_title=f"Consommation ({unite_label})",
                                        height=450
                                    )
                                    fig.update_xaxes(
                                        tickmode='linear',
                                        dtick=1,
                                        tickvals=list(range(1, 13)),
                                        ticktext=['Jan','Fév','Mar','Avr','Mai','Juin','Juil','Août','Sep','Oct','Nov','Déc']
                                    )
                                    fig.update_layout(
                                        legend=dict(
                                            orientation='h',
                                            yanchor='bottom',
                                            y=-0.35,
                                            xanchor='center',
                                            x=0.5,
                                            font=dict(size=11, color='#E2E8F0'),
                                            bgcolor='rgba(17, 24, 39, 0.9)',
                                            bordercolor='rgba(255,255,255,0.05)',
                                            borderwidth=1,
                                            itemclick='toggle',
                                            itemdoubleclick='toggleothers'
                                        ),
                                        margin=dict(l=60, r=40, t=60, b=100)
                                    )
                                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                                
                                else:
                                    df_mois = df_annee[df_annee['Agence'].astype(str) == agence_selected].groupby('Mois')[col_consommation].sum().reset_index()
                                    df_mois = df_mois.sort_values('Mois')
                                    fig = go.Figure()
                                    fig.add_trace(go.Bar(
                                        x=df_mois['Mois'],
                                        y=df_mois[col_consommation],
                                        marker_color=color_theme,  # couleur modifiée ici
                                        text=df_mois[col_consommation].apply(lambda x: f"{format_number(x)} {unite_label}"),
                                        textposition='outside',
                                        textfont=dict(size=12, color='#FFFFFF', weight='bold')
                                    ))
                                    
                                    fig = apply_graph_style(
                                        fig,
                                        title=f"Consommation mensuelle – {agence_selected} ({annee_selected}) – {type_energie_local}",
                                        x_title="Mois",
                                        y_title=f"Consommation ({unite_label})",
                                        height=400,
                                        bargap=0.3
                                    )
                                    fig.update_xaxes(
                                        tickmode='linear',
                                        dtick=1,
                                        tickvals=list(range(1, 13)),
                                        ticktext=['Jan','Fév','Mar','Avr','Mai','Juin','Juil','Août','Sep','Oct','Nov','Déc']
                                    )
                                    fig.update_layout(showlegend=False)
                                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                                    
                                    df_mois_formatted = df_mois.copy()
                                    df_mois_formatted[col_consommation] = df_mois_formatted[col_consommation].apply(lambda x: format_number(x))
                                    
                                    st.dataframe(
                                        df_mois_formatted.rename(columns={col_consommation: 'Consommation'})
                                        .style.set_properties(**{'background-color': '#0D2B4A', 'color': '#E2E8F0'})
                                        .set_table_styles([{'selector': 'thead th', 'props': [('background-color', '#1A4A7A'), ('color', 'white'), ('font-weight', 'bold')]}])
                                    )
        else:
            st.warning("⚠️ Données insuffisantes pour le taux d'évolution par agence.")
    
    # ============================================================
    # SECTION 7 : KPI D'ANALYSE (couleur des barres modifiée)
    # ============================================================
    with st.expander("📊 KPI d'Analyse", expanded=True):
        if col_consommation:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<p style="text-align:center; font-weight:700; color:#EF5350; font-size:1.1rem; background:#2A0A0A; padding:0.3rem; border-radius:8px;">⚡ Électricité par agence</p>', unsafe_allow_html=True)
                if 'Agence' in df_elec_clean.columns and not df_elec_clean.empty:
                    df_ag = df_elec_clean.groupby('Agence')[col_consommation].sum().reset_index().sort_values(col_consommation, ascending=False)
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=df_ag['Agence'],
                        y=df_ag[col_consommation],
                        marker_color='#811F1F',  # COULEUR MODIFIÉE
                        text=df_ag[col_consommation].apply(lambda x: format_number(x)),
                        textposition='outside',
                        textfont=dict(size=11, color='#FFFFFF', weight='bold')
                    ))
                    fig = apply_graph_style(
                        fig,
                        title='Consommation électrique par agence',
                        x_title='Agence',
                        y_title='kWh',
                        height=280,
                        bargap=0.3
                    )
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("Aucune donnée électrique")
            
            with col2:
                st.markdown('<p style="text-align:center; font-weight:700; color:#42A5F5; font-size:1.1rem; background:#0A1A2A; padding:0.3rem; border-radius:8px;">💧 Eau par agence</p>', unsafe_allow_html=True)
                if 'Agence' in df_eau_clean.columns and not df_eau_clean.empty:
                    df_ag = df_eau_clean.groupby('Agence')[col_consommation].sum().reset_index().sort_values(col_consommation, ascending=False)
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=df_ag['Agence'],
                        y=df_ag[col_consommation],
                        marker_color='#2E6494',  # COULEUR MODIFIÉE
                        text=df_ag[col_consommation].apply(lambda x: format_number(x)),
                        textposition='outside',
                        textfont=dict(size=11, color='#FFFFFF', weight='bold')
                    ))
                    fig = apply_graph_style(
                        fig,
                        title="Consommation d'eau par agence",
                        x_title='Agence',
                        y_title='m³',
                        height=280,
                        bargap=0.3
                    )
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("Aucune donnée eau")
            
            with col3:
                st.markdown('<p style="text-align:center; font-weight:700; color:#FFD600; font-size:1.1rem; background:#1A1A0A; padding:0.3rem; border-radius:8px;">👤 Par type de client</p>', unsafe_allow_html=True)
                if 'Type_Client' in df.columns and col_consommation:
                    df_type = df.groupby('Type_Client')[col_consommation].sum().reset_index()
                    df_type = df_type[df_type[col_consommation] > 0]
                    if not df_type.empty:
                        colors_pie = ['#D32F2F', '#1E88E5', '#FF8F00', '#6A1B9A', '#00A86B', '#00897B']
                        fig = go.Figure()
                        fig.add_trace(go.Pie(
                            labels=df_type['Type_Client'],
                            values=df_type[col_consommation],
                            hole=0.3,
                            marker=dict(colors=colors_pie[:len(df_type)]),
                            textinfo='label+percent',
                            textposition='inside',
                            textfont=dict(size=13, color='#FFFFFF', weight='bold'),
                            insidetextorientation='radial'
                        ))
                        fig.update_layout(
                            title=dict(text='Répartition par type de client', font=dict(size=16, color='#FFFFFF'), x=0.5, xanchor='center'),
                            plot_bgcolor='#111827',
                            paper_bgcolor='#111827',
                            height=280,
                            margin=dict(l=20, r=20, t=40, b=50),
                            legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5, font=dict(size=11, color='#E2E8F0'))
                        )
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                    else:
                        st.info("Aucune donnée par type de client")
                else:
                    st.info("Colonne 'Type_Client' non trouvée")
        else:
            st.warning("⚠️ Colonne de consommation non trouvée")
    
    st.markdown("---")
    with st.expander("📋 Voir les données utilisées", expanded=False):
        st.dataframe(
            df.style.set_properties(**{
                'background-color': '#0D2B4A',
                'color': '#E2E8F0'
            }).set_table_styles([
                {'selector': 'thead th', 'props': [
                    ('background-color', '#1A4A7A'),
                    ('color', 'white'),
                    ('font-weight', 'bold'),
                    ('padding', '10px')
                ]}
            ]),
            use_container_width=True
        )