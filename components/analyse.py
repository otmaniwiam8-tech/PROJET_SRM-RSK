# components/analyse.py (avec couleurs : électricité rouge, eau bleue - version finale avec gérance séparée)
import sys
import os
import math

# Ajouter le dossier parent au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config import COLORS, CONSOMMATION_COLS, MONTANT_COLS, UNITE_COLS, UNITE_EAU, UNITE_ELECTRICITE
from data_loader import find_column

# Définir les couleurs pour l'électricité et l'eau
COLOR_ELEC = "#811F1F"      # Rouge
COLOR_EAU = "#2E6494"       # Bleu
# Couleur pour la facturation (gardée verte)
COLOR_FACT = "#368B6C"

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
    
    # Si c'est un entier (pas de partie décimale significative)
    if num == int(num):
        return str(int(num))
    
    # Sinon, afficher avec 2 décimales max (en supprimant les zéros inutiles)
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

def format_int_with_separator(value):
    """
    Formate un nombre en entier avec séparateur de milliers (espace).
    Arrondit à l'entier le plus proche.
    Ex: 12345.67 -> "12 346"
    """
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    try:
        num = float(value)
        rounded = int(round(num))
        # Utiliser un espace comme séparateur de milliers
        return f"{rounded:,}".replace(',', ' ')
    except (ValueError, TypeError):
        return str(value)

# ============================================================
# 1. STYLE CSS (compatible avec facteurs et kpi_predictifs)
# ============================================================

def apply_analyse_style():
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
        .graph-title {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #6A1B9A !important;
            text-align: center !important;
            margin-bottom: 0.5rem !important;
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
        .section-title-consommation {
            color: #FFFFFF !important;
            font-size: 1.6rem !important;
            font-weight: 700 !important;
            margin: 1.5rem 0 1rem 0 !important;
            padding: 0.5rem 1.2rem !important;
            background: linear-gradient(135deg, #0D47A1 0%, #1E88E5 100%) !important;
            border-radius: 10px !important;
            display: inline-block !important;
            box-shadow: 0 4px 12px rgba(13, 71, 161, 0.15) !important;
        }
        .section-title-facturation {
            color: #FFFFFF !important;
            font-size: 1.6rem !important;
            font-weight: 700 !important;
            margin: 1.5rem 0 1rem 0 !important;
            padding: 0.5rem 1.2rem !important;
            background: linear-gradient(135deg, #00695C 0%, #00A86B 100%) !important;
            border-radius: 10px !important;
            display: inline-block !important;
            box-shadow: 0 4px 12px rgba(0, 105, 92, 0.15) !important;
        }
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
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# 2. FONCTION D'APPLICATION DU STYLE AUX GRAPHIQUES
# ============================================================

def apply_graph_style(fig, title, x_title="", y_title="", height=400, bargap=0.3):
    """
    Applique un style avec axes et titres en blanc sur fond sombre,
    et impose un affichage entier sans décimales sur les axes (tickformat=',.0f')
    pour les axes numériques.
    """
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=16, color='#B0D4F1', family='Arial, sans-serif', weight='bold')),
            tickfont=dict(size=14, color='#B0D4F1', family='Arial, sans-serif'),
            gridcolor='rgba(255,255,255,0.05)',
            gridwidth=0.5,
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=16, color='#B0D4F1', family='Arial, sans-serif', weight='bold')),
            tickfont=dict(size=14, color='#B0D4F1', family='Arial, sans-serif'),
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
    
    # Appliquer le format d'affichage entier avec séparateur de milliers (virgule)
    # sur l'axe Y (toujours numérique)
    fig.update_yaxes(tickformat=',.0f')
    
    # Sur l'axe X, seulement si ce n'est pas une catégorie
    if fig.layout.xaxis.type != 'category':
        fig.update_xaxes(tickformat=',.0f')
    
    return fig

# ============================================================
# 3. PAGE PRINCIPALE
# ============================================================

def render_analyse(df_clean, df):
    """Affiche la page d'analyse des données historiques avec style sombre"""
    
    apply_analyse_style()
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.2rem; font-weight: 700; color: #FFFFFF; margin: 0; padding: 0;">📊 Analyse des données historiques</h1>
        <p style="font-size: 1.1rem; color: #94A3B8; margin: 0.2rem 0 0 0;">
            Visualisation et analyse de la consommation passée
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Vérification : forcer le passage par le nettoyage
    if df is None:
        st.warning("⚠️ Veuillez d'abord importer un fichier dans la barre latérale.")
        st.stop()
    
    if df_clean is None:
        st.markdown("""
        <div class="block-message">
            <div class="icon">🚨</div>
            <h2>Données non nettoyées</h2>
            <p>
                Vous devez <strong>obligatoirement</strong> passer par la page <br>
                <strong style="color:#0D47A1; font-size:1.2rem;">'Nettoyage des données'</strong> <br>
                avant d'accéder à l'analyse.
            </p>
            <p style="font-size:0.95rem; color:#5A6C7D;">
                ⚠️ Les données brutes contiennent des valeurs manquantes, des doublons et des incohérences.<br>
                L'analyse ne sera pas fiable sans un nettoyage préalable.
            </p>
            <div class="btn-container">
        """, unsafe_allow_html=True)
        
        if st.button("🧹 Aller au nettoyage des données", type="primary"):
            st.session_state.page = "🧹 Nettoyage des données"
            st.rerun()
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        st.stop()
    
    df = df_clean
    st.success("✅ Utilisation des données nettoyées")
    
    # --------------------------------------------------
    # TROUVER LA COLONNE D'UNITÉ
    # --------------------------------------------------
    col_unite = find_column(df, UNITE_COLS)
    
    # Séparer eau et électricité
    if col_unite is not None:
        df_eau = df[df[col_unite].astype(str).str.lower().isin([u.lower() for u in UNITE_EAU])]
        df_elec = df[df[col_unite].astype(str).str.lower().isin([u.lower() for u in UNITE_ELECTRICITE])]
    else:
        df_eau = pd.DataFrame()
        df_elec = df
    
    # --------------------------------------------------
    # FILTRES
    # --------------------------------------------------
    st.markdown('<p style="color: #FF8F00; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.5rem;">🔍 Filtres d\'analyse</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'Agence' in df.columns:
            agences = ['Toutes'] + sorted([str(x) for x in df['Agence'].unique().tolist() if pd.notna(x)])
            agence_selection = st.selectbox("📍 Agence", agences)
        else:
            agence_selection = "Toutes"
    
    with col2:
        if 'Annee_Facture' in df.columns:
            annees = ['Toutes'] + sorted([str(x) for x in df['Annee_Facture'].unique().tolist() if pd.notna(x)])
            annee_selection = st.selectbox("📅 Année de facturation", annees)
        else:
            annee_selection = "Toutes"
    
    with col3:
        if 'Type_Client' in df.columns:
            types = ['Tous'] + sorted([str(x) for x in df['Type_Client'].unique().tolist() if pd.notna(x)])
            type_selection = st.selectbox("👤 Type de client", types)
        else:
            type_selection = "Tous"
    
    with col4:
        if 'Mois' in df.columns:
            mois_list = ['Tous'] + sorted([str(x) for x in df['Mois'].unique().tolist() if pd.notna(x)])
            mois_selection = st.selectbox("📆 Mois", mois_list)
        else:
            mois_selection = "Tous"
    
    # --------------------------------------------------
    # FILTRAGE
    # --------------------------------------------------
    df_filtered = df.copy()
    
    if agence_selection != "Toutes":
        df_filtered = df_filtered[df_filtered['Agence'].astype(str) == agence_selection]
    if annee_selection != "Toutes":
        df_filtered = df_filtered[df_filtered['Annee_Facture'].astype(str) == annee_selection]
    if type_selection != "Tous":
        df_filtered = df_filtered[df_filtered['Type_Client'].astype(str) == type_selection]
    if mois_selection != "Tous":
        df_filtered = df_filtered[df_filtered['Mois'].astype(str) == mois_selection]
    
    if df_filtered.empty:
        st.warning("⚠️ Aucune donnée pour ces filtres. Veuillez modifier votre sélection.")
        st.stop()
    
    # Filtrer eau et électricité
    if col_unite is not None:
        df_filtered_eau = df_filtered[df_filtered[col_unite].astype(str).str.lower().isin([u.lower() for u in UNITE_EAU])]
        df_filtered_elec = df_filtered[df_filtered[col_unite].astype(str).str.lower().isin([u.lower() for u in UNITE_ELECTRICITE])]
    else:
        df_filtered_eau = pd.DataFrame()
        df_filtered_elec = df_filtered
    
    # Trouver la colonne de consommation
    col_consommation = find_column(df_filtered, CONSOMMATION_COLS)
    if col_consommation is None:
        st.error("❌ Colonne de consommation non trouvée")
        st.stop()
    
    col_montant = find_column(df_filtered, MONTANT_COLS)
    
    st.info(f"📊 {format_int_with_separator(df_filtered.shape[0])} lignes affichées")
    st.markdown("---")
    
    # ============================================================
    # KPI CARDS (style facteurs)
    # ============================================================
    st.markdown('<h2 class="section-title">📊 Indicateurs clés</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_elec = df_filtered_elec[col_consommation].sum() if not df_filtered_elec.empty else 0
        st.markdown(f"""
        <div class="kpi-card" style="border-color: #D32F2F;">
            <div class="kpi-label" style="color: #EF5350;">⚡ CONSO ÉLECTRICITÉ</div>
            <div class="kpi-value" style="color: #EF5350;">{format_int_with_separator(total_elec)}</div>
            <div class="kpi-sub">kWh</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_eau = df_filtered_eau[col_consommation].sum() if not df_filtered_eau.empty else 0
        st.markdown(f"""
        <div class="kpi-card" style="border-color: #1E88E5;">
            <div class="kpi-label" style="color: #42A5F5;">💧 CONSO EAU</div>
            <div class="kpi-value" style="color: #42A5F5;">{format_int_with_separator(total_eau)}</div>
            <div class="kpi-sub">m³</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        nb_factures = df_filtered.shape[0]
        st.markdown(f"""
        <div class="kpi-card" style="border-color: #FFD600;">
            <div class="kpi-label" style="color: #FFD600;">📄 NOMBRE FACTURES</div>
            <div class="kpi-value" style="color: #FFD600;">{format_int_with_separator(nb_factures)}</div>
            <div class="kpi-sub">factures</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        nb_agences = df_filtered['Agence'].nunique() if 'Agence' in df_filtered.columns else 0
        st.markdown(f"""
        <div class="kpi-card" style="border-color: #6A1B9A;">
            <div class="kpi-label" style="color: #CE93D8;">📍 AGENCES</div>
            <div class="kpi-value" style="color: #CE93D8;">{format_int_with_separator(nb_agences)}</div>
            <div class="kpi-sub">agences</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ================================================
    # SECTION 1 : ANALYSE DE LA CONSOMMATION
    # ================================================
    
    st.markdown('<h2 class="section-title-consommation">📊 Analyse de la Consommation</h2>', unsafe_allow_html=True)
    
    # --------------------------------------------------
    # GRAPHIQUE 1 : Consommation par mois (Électricité)
    # --------------------------------------------------
    if not df_filtered_elec.empty:
        st.markdown('<p class="graph-title">⚡ Consommation électrique par mois</p>', unsafe_allow_html=True)
        
        if 'Mois' in df_filtered_elec.columns:
            df_mois_elec = df_filtered_elec.groupby('Mois')[col_consommation].sum().reset_index()
            
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                x=df_mois_elec['Mois'],
                y=df_mois_elec[col_consommation],
                marker_color=COLOR_ELEC,
                marker_line_color='white',
                marker_line_width=2,
                text=df_mois_elec[col_consommation].apply(lambda x: f"{format_int_with_separator(x)} kWh"),
                textposition='outside',
                textfont=dict(size=13, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
                hovertemplate='<b>Mois %{x}</b><br>Consommation: %{text}<extra></extra>'
            ))
            fig1 = apply_graph_style(
                fig1,
                title='Consommation électrique totale par mois',
                x_title='Mois',
                y_title='Consommation (kWh)',
                height=400
            )
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
    
    # --------------------------------------------------
    # GRAPHIQUE 1bis : Consommation par mois (Eau)
    # --------------------------------------------------
    if not df_filtered_eau.empty:
        st.markdown('<p class="graph-title">💧 Consommation d\'eau par mois</p>', unsafe_allow_html=True)
        
        if 'Mois' in df_filtered_eau.columns:
            df_mois_eau = df_filtered_eau.groupby('Mois')[col_consommation].sum().reset_index()
            
            fig1_eau = go.Figure()
            fig1_eau.add_trace(go.Bar(
                x=df_mois_eau['Mois'],
                y=df_mois_eau[col_consommation],
                marker_color=COLOR_EAU,
                marker_line_color='white',
                marker_line_width=2,
                text=df_mois_eau[col_consommation].apply(lambda x: f"{format_int_with_separator(x)} m³"),
                textposition='outside',
                textfont=dict(size=13, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
                hovertemplate='<b>Mois %{x}</b><br>Consommation: %{text}<extra></extra>'
            ))
            fig1_eau = apply_graph_style(
                fig1_eau,
                title="Consommation d'eau totale par mois",
                x_title='Mois',
                y_title='Consommation (m³)',
                height=400
            )
            st.plotly_chart(fig1_eau, use_container_width=True, config={'displayModeBar': False})
    
    # --------------------------------------------------
    # GRAPHIQUE 2 : Consommation par saison
    # --------------------------------------------------
    st.markdown('<p class="graph-title">🌦️ Consommation par saison</p>', unsafe_allow_html=True)
    
    if not df_filtered_elec.empty and 'Saison' in df_filtered_elec.columns:
        df_saison_elec = df_filtered_elec.groupby('Saison')[col_consommation].sum().reset_index()
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=df_saison_elec['Saison'],
            y=df_saison_elec[col_consommation],
            marker_color=COLOR_ELEC,
            marker_line_color='white',
            marker_line_width=2,
            text=df_saison_elec[col_consommation].apply(lambda x: f"{format_int_with_separator(x)} kWh"),
            textposition='outside',
            textfont=dict(size=13, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
            hovertemplate='<b>%{x}</b><br>Consommation: %{text}<extra></extra>'
        ))
        fig2 = apply_graph_style(
            fig2,
            title='Consommation électrique par saison',
            x_title='Saison',
            y_title='Consommation (kWh)',
            height=350
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
    
    if not df_filtered_eau.empty and 'Saison' in df_filtered_eau.columns:
        df_saison_eau = df_filtered_eau.groupby('Saison')[col_consommation].sum().reset_index()
        
        fig2_eau = go.Figure()
        fig2_eau.add_trace(go.Bar(
            x=df_saison_eau['Saison'],
            y=df_saison_eau[col_consommation],
            marker_color=COLOR_EAU,
            marker_line_color='white',
            marker_line_width=2,
            text=df_saison_eau[col_consommation].apply(lambda x: f"{format_int_with_separator(x)} m³"),
            textposition='outside',
            textfont=dict(size=13, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
            hovertemplate='<b>%{x}</b><br>Consommation: %{text}<extra></extra>'
        ))
        fig2_eau = apply_graph_style(
            fig2_eau,
            title='Consommation d\'eau par saison',
            x_title='Saison',
            y_title='Consommation (m³)',
            height=350
        )
        st.plotly_chart(fig2_eau, use_container_width=True, config={'displayModeBar': False})
    
    # --------------------------------------------------
    # GRAPHIQUE 3 : Consommation par agence
    # --------------------------------------------------
    st.markdown('<p class="graph-title">📍 Consommation par agence</p>', unsafe_allow_html=True)
    
    # Électricité
    if not df_filtered_elec.empty and 'Agence' in df_filtered_elec.columns:
        df_agence_elec = df_filtered_elec.groupby('Agence')[col_consommation].sum().reset_index()
        df_agence_elec = df_agence_elec.sort_values(col_consommation, ascending=True)
        
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=df_agence_elec[col_consommation],
            y=df_agence_elec['Agence'],
            orientation='h',
            marker_color=COLOR_ELEC,
            marker_line_color='white',
            marker_line_width=2,
            text=df_agence_elec[col_consommation].apply(lambda x: f"{format_int_with_separator(x)} kWh"),
            textposition='outside',
            textfont=dict(size=12, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
            hovertemplate='<b>%{y}</b><br>Consommation: %{text}<extra></extra>'
        ))
        fig3 = apply_graph_style(
            fig3,
            title='Consommation électrique par agence',
            x_title='Consommation (kWh)',
            y_title='Agence',
            height=max(350, len(df_agence_elec) * 45)
        )
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
    
    # Eau
    if not df_filtered_eau.empty and 'Agence' in df_filtered_eau.columns:
        df_agence_eau = df_filtered_eau.groupby('Agence')[col_consommation].sum().reset_index()
        df_agence_eau = df_agence_eau.sort_values(col_consommation, ascending=True)
        
        fig3_eau = go.Figure()
        fig3_eau.add_trace(go.Bar(
            x=df_agence_eau[col_consommation],
            y=df_agence_eau['Agence'],
            orientation='h',
            marker_color=COLOR_EAU,
            marker_line_color='white',
            marker_line_width=2,
            text=df_agence_eau[col_consommation].apply(lambda x: f"{format_int_with_separator(x)} m³"),
            textposition='outside',
            textfont=dict(size=12, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
            hovertemplate='<b>%{y}</b><br>Consommation: %{text}<extra></extra>'
        ))
        fig3_eau = apply_graph_style(
            fig3_eau,
            title='Consommation d\'eau par agence',
            x_title='Consommation (m³)',
            y_title='Agence',
            height=max(350, len(df_agence_eau) * 45)
        )
        st.plotly_chart(fig3_eau, use_container_width=True, config={'displayModeBar': False})
    
    # --------------------------------------------------
    # GRAPHIQUE 4 : Consommation par gérance
    # --------------------------------------------------
    st.markdown('<p class="graph-title">🏢 Consommation par gérance</p>', unsafe_allow_html=True)
    
    if 'Gerance' in df_filtered.columns and col_consommation is not None:
        df_gerance_elec = df_filtered_elec.groupby('Gerance')[col_consommation].sum().reset_index()
        df_gerance_elec['Consommation'] = df_gerance_elec[col_consommation].round(0)
        df_gerance_elec = df_gerance_elec.sort_values('Consommation', ascending=True)
        
        df_gerance_eau = df_filtered_eau.groupby('Gerance')[col_consommation].sum().reset_index()
        df_gerance_eau['Consommation'] = df_gerance_eau[col_consommation].round(0)
        df_gerance_eau = df_gerance_eau.sort_values('Consommation', ascending=True)
        
        gerances = sorted(set(df_gerance_elec['Gerance'].tolist() + df_gerance_eau['Gerance'].tolist()))
        
        elec_dict = dict(zip(df_gerance_elec['Gerance'], df_gerance_elec['Consommation']))
        eau_dict = dict(zip(df_gerance_eau['Gerance'], df_gerance_eau['Consommation']))
        
        elec_vals = [elec_dict.get(g, 0) for g in gerances]
        eau_vals = [eau_dict.get(g, 0) for g in gerances]
        
        fig4 = go.Figure()
        
        fig4.add_trace(go.Bar(
            x=elec_vals,
            y=gerances,
            orientation='h',
            name='Électricité',
            marker_color=COLOR_ELEC,
            text=[format_int_with_separator(v) for v in elec_vals],
            textposition='outside',
            textfont=dict(size=14, color='#FFFFFF', weight='bold'),
            hovertemplate='<b>%{y}</b><br>Électricité: %{text} kWh<extra></extra>',
            texttemplate='%{text}',
            offsetgroup=0,
            width=0.35
        ))
        
        fig4.add_trace(go.Bar(
            x=eau_vals,
            y=gerances,
            orientation='h',
            name='Eau',
            marker_color=COLOR_EAU,
            text=[format_int_with_separator(v) for v in eau_vals],
            textposition='outside',
            textfont=dict(size=14, color='#FFFFFF', weight='bold'),
            hovertemplate='<b>%{y}</b><br>Eau: %{text} m³<extra></extra>',
            texttemplate='%{text}',
            offsetgroup=1,
            width=0.35
        ))
        
        fig4.update_layout(
            title=dict(
                text='Consommation par gérance',
                font=dict(size=22, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title=dict(text='Consommation', font=dict(size=16, color='#B0D4F1', family='Arial, sans-serif', weight='bold')),
                tickfont=dict(size=14, color='#B0D4F1', family='Arial, sans-serif'),
                gridcolor='rgba(255,255,255,0.05)',
                gridwidth=0.5,
                showgrid=True,
                tickformat=',.0f'  # entiers avec séparateur de milliers
            ),
            yaxis=dict(
                title=dict(text='Gérance', font=dict(size=16, color='#B0D4F1', family='Arial, sans-serif', weight='bold')),
                tickfont=dict(size=14, color='#B0D4F1', family='Arial, sans-serif'),
                showgrid=False,
                showticklabels=True
            ),
            plot_bgcolor='#111827',
            paper_bgcolor='#111827',
            height=max(400, len(gerances) * 70),
            margin=dict(l=120, r=120, t=60, b=80),
            bargap=0.3,
            bargroupgap=0.15,
            legend=dict(
                orientation='h',
                yanchor='top',
                y=-0.15,
                xanchor='center',
                x=0.5,
                font=dict(size=14, color='#E2E8F0', weight='bold'),
                bgcolor='rgba(17, 24, 39, 0.8)',
                bordercolor='rgba(255,255,255,0.05)',
                borderwidth=1
            )
        )
        st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})
    else:
        st.warning("Colonne 'Gerance' ou colonne de consommation non trouvée")
    
    # --------------------------------------------------
    # GRAPHIQUE 5 : Évolution par année (AMÉLIORÉ)
    # --------------------------------------------------
    st.markdown('<p class="graph-title">📈 Évolution de la consommation par année</p>', unsafe_allow_html=True)
    
    # Électricité
    if not df_filtered_elec.empty and 'Annee_Facture' in df_filtered_elec.columns:
        df_annee_elec = df_filtered_elec.groupby('Annee_Facture')[col_consommation].sum().reset_index()
        
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=df_annee_elec['Annee_Facture'],
            y=df_annee_elec[col_consommation],
            mode='lines+markers+text',
            line=dict(color=COLOR_ELEC, width=4),
            marker=dict(size=16, color=COLOR_ELEC, line=dict(color='white', width=3)),
            text=df_annee_elec[col_consommation].apply(lambda x: f"{format_int_with_separator(x)} kWh"),
            textposition='top center',
            textfont=dict(size=12, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
            hovertemplate='<b>Année %{x}</b><br>Consommation: %{text}<extra></extra>'
        ))
        fig5.update_layout(
            title=dict(
                text='Évolution de la consommation électrique',
                font=dict(size=20, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title=dict(text='Année', font=dict(size=16, color='#B0D4F1', family='Arial, sans-serif', weight='bold')),
                tickfont=dict(size=14, color='#B0D4F1', family='Arial, sans-serif'),
                gridcolor='rgba(255,255,255,0.05)',
                gridwidth=0.5,
                showgrid=True,
                tickmode='linear',
                tickformat=',.0f'  # années avec séparateur
            ),
            yaxis=dict(
                title=dict(text='Consommation (kWh)', font=dict(size=16, color='#B0D4F1', family='Arial, sans-serif', weight='bold')),
                tickfont=dict(size=14, color='#B0D4F1', family='Arial, sans-serif'),
                gridcolor='rgba(255,255,255,0.05)',
                gridwidth=0.5,
                showgrid=True,
                tickformat=',.0f'
            ),
            plot_bgcolor='#111827',
            paper_bgcolor='#111827',
            height=400,
            margin=dict(l=60, r=40, t=80, b=60),
            showlegend=False
        )
        st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})
    
    # Eau
    if not df_filtered_eau.empty and 'Annee_Facture' in df_filtered_eau.columns:
        df_annee_eau = df_filtered_eau.groupby('Annee_Facture')[col_consommation].sum().reset_index()
        
        fig5_eau = go.Figure()
        fig5_eau.add_trace(go.Scatter(
            x=df_annee_eau['Annee_Facture'],
            y=df_annee_eau[col_consommation],
            mode='lines+markers+text',
            line=dict(color=COLOR_EAU, width=4),
            marker=dict(size=16, color=COLOR_EAU, line=dict(color='white', width=3)),
            text=df_annee_eau[col_consommation].apply(lambda x: f"{format_int_with_separator(x)} m³"),
            textposition='top center',
            textfont=dict(size=12, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
            hovertemplate='<b>Année %{x}</b><br>Consommation: %{text}<extra></extra>'
        ))
        fig5_eau.update_layout(
            title=dict(
                text='Évolution de la consommation d\'eau',
                font=dict(size=20, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title=dict(text='Année', font=dict(size=16, color='#B0D4F1', family='Arial, sans-serif', weight='bold')),
                tickfont=dict(size=14, color='#B0D4F1', family='Arial, sans-serif'),
                gridcolor='rgba(255,255,255,0.05)',
                gridwidth=0.5,
                showgrid=True,
                tickmode='linear',
                tickformat=',.0f'
            ),
            yaxis=dict(
                title=dict(text='Consommation (m³)', font=dict(size=16, color='#B0D4F1', family='Arial, sans-serif', weight='bold')),
                tickfont=dict(size=14, color='#B0D4F1', family='Arial, sans-serif'),
                gridcolor='rgba(255,255,255,0.05)',
                gridwidth=0.5,
                showgrid=True,
                tickformat=',.0f'
            ),
            plot_bgcolor='#111827',
            paper_bgcolor='#111827',
            height=400,
            margin=dict(l=60, r=40, t=80, b=60),
            showlegend=False
        )
        st.plotly_chart(fig5_eau, use_container_width=True, config={'displayModeBar': False})
    
    # --------------------------------------------------
    # GRAPHIQUE 6 : Consommation par type de client
    # --------------------------------------------------
    st.markdown('<p class="graph-title">👤 Consommation par type de client</p>', unsafe_allow_html=True)
    
    # Électricité
    if not df_filtered_elec.empty and 'Type_Client' in df_filtered_elec.columns:
        df_type_elec = df_filtered_elec.groupby('Type_Client')[col_consommation].sum().reset_index()
        df_type_elec = df_type_elec.sort_values(col_consommation, ascending=True)
        
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(
            x=df_type_elec[col_consommation],
            y=df_type_elec['Type_Client'],
            orientation='h',
            marker_color=COLOR_ELEC,
            marker_line_color='white',
            marker_line_width=2,
            text=df_type_elec[col_consommation].apply(lambda x: f"{format_int_with_separator(x)} kWh"),
            textposition='outside',
            textfont=dict(size=12, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
            hovertemplate='<b>%{y}</b><br>Consommation: %{text}<extra></extra>'
        ))
        fig6 = apply_graph_style(
            fig6,
            title='Consommation électrique par type de client',
            x_title='Consommation (kWh)',
            y_title='Type de client',
            height=350
        )
        st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar': False})
    
    # Eau
    if not df_filtered_eau.empty and 'Type_Client' in df_filtered_eau.columns:
        df_type_eau = df_filtered_eau.groupby('Type_Client')[col_consommation].sum().reset_index()
        df_type_eau = df_type_eau.sort_values(col_consommation, ascending=True)
        
        fig6_eau = go.Figure()
        fig6_eau.add_trace(go.Bar(
            x=df_type_eau[col_consommation],
            y=df_type_eau['Type_Client'],
            orientation='h',
            marker_color=COLOR_EAU,
            marker_line_color='white',
            marker_line_width=2,
            text=df_type_eau[col_consommation].apply(lambda x: f"{format_int_with_separator(x)} m³"),
            textposition='outside',
            textfont=dict(size=12, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
            hovertemplate='<b>%{y}</b><br>Consommation: %{text}<extra></extra>'
        ))
        fig6_eau = apply_graph_style(
            fig6_eau,
            title='Consommation d\'eau par type de client',
            x_title='Consommation (m³)',
            y_title='Type de client',
            height=350
        )
        st.plotly_chart(fig6_eau, use_container_width=True, config={'displayModeBar': False})
    
    # ================================================
    # SECTION 2 : ANALYSE DE LA FACTURATION
    # ================================================
    
    if col_montant is not None:
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title-facturation">💰 Analyse de la Facturation</h2>', unsafe_allow_html=True)
        
        # --------------------------------------------------
        # GRAPHIQUE 7 : Facturation par mois
        # --------------------------------------------------
        st.markdown('<p class="graph-title">📊 Facturation par mois</p>', unsafe_allow_html=True)
        
        if 'Mois' in df_filtered.columns:
            df_fact_mois = df_filtered.groupby('Mois')[col_montant].sum().reset_index()
            
            fig7 = go.Figure()
            fig7.add_trace(go.Bar(
                x=df_fact_mois['Mois'],
                y=df_fact_mois[col_montant],
                marker_color=COLOR_FACT,
                marker_line_color='white',
                marker_line_width=2,
                text=df_fact_mois[col_montant].apply(lambda x: f"{format_int_with_separator(x)} MAD"),
                textposition='outside',
                textfont=dict(size=13, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
                hovertemplate='<b>Mois %{x}</b><br>Montant: %{text}<extra></extra>'
            ))
            fig7 = apply_graph_style(
                fig7,
                title='Facturation par mois',
                x_title='Mois',
                y_title='Montant (MAD)',
                height=400
            )
            st.plotly_chart(fig7, use_container_width=True, config={'displayModeBar': False})
        
        # --------------------------------------------------
        # GRAPHIQUE 8 : Facturation par agence
        # --------------------------------------------------
        st.markdown('<p class="graph-title">📍 Facturation par agence</p>', unsafe_allow_html=True)
        
        if 'Agence' in df_filtered.columns:
            df_fact_agence = df_filtered.groupby('Agence')[col_montant].sum().reset_index()
            df_fact_agence = df_fact_agence.sort_values(col_montant, ascending=True)
            
            fig8 = go.Figure()
            fig8.add_trace(go.Bar(
                x=df_fact_agence[col_montant],
                y=df_fact_agence['Agence'],
                orientation='h',
                marker_color=COLOR_FACT,
                marker_line_color='white',
                marker_line_width=2,
                text=df_fact_agence[col_montant].apply(lambda x: f"{format_int_with_separator(x)} MAD"),
                textposition='outside',
                textfont=dict(size=13, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
                hovertemplate='<b>%{y}</b><br>Montant: %{text}<extra></extra>'
            ))
            fig8 = apply_graph_style(
                fig8,
                title='Facturation par agence',
                x_title='Montant (MAD)',
                y_title='Agence',
                height=max(400, len(df_fact_agence) * 45)
            )
            st.plotly_chart(fig8, use_container_width=True, config={'displayModeBar': False})
        
        # --------------------------------------------------
        # GRAPHIQUE 9 : Évolution facturation par année (amélioré)
        # --------------------------------------------------
        st.markdown('<p class="graph-title">📈 Évolution de la facturation par année</p>', unsafe_allow_html=True)
        
        if 'Annee_Facture' in df_filtered.columns:
            df_fact_annee = df_filtered.groupby('Annee_Facture')[col_montant].sum().reset_index()
            
            fig9 = go.Figure()
            fig9.add_trace(go.Scatter(
                x=df_fact_annee['Annee_Facture'],
                y=df_fact_annee[col_montant],
                mode='lines+markers+text',
                line=dict(color=COLOR_FACT, width=4),
                marker=dict(size=16, color=COLOR_FACT, line=dict(color='white', width=3)),
                text=df_fact_annee[col_montant].apply(lambda x: f"{format_int_with_separator(x)} MAD"),
                textposition='top center',
                textfont=dict(size=13, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
                hovertemplate='<b>Année %{x}</b><br>Montant: %{text}<extra></extra>'
            ))
            fig9.update_layout(
                title=dict(
                    text='Évolution de la facturation par année',
                    font=dict(size=20, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title=dict(text='Année', font=dict(size=16, color='#B0D4F1', family='Arial, sans-serif', weight='bold')),
                    tickfont=dict(size=14, color='#B0D4F1', family='Arial, sans-serif'),
                    gridcolor='rgba(255,255,255,0.05)',
                    gridwidth=0.5,
                    showgrid=True,
                    tickmode='linear',
                    tickformat=',.0f'
                ),
                yaxis=dict(
                    title=dict(text='Montant (MAD)', font=dict(size=16, color='#B0D4F1', family='Arial, sans-serif', weight='bold')),
                    tickfont=dict(size=14, color='#B0D4F1', family='Arial, sans-serif'),
                    gridcolor='rgba(255,255,255,0.05)',
                    gridwidth=0.5,
                    showgrid=True,
                    tickformat=',.0f'
                ),
                plot_bgcolor='#111827',
                paper_bgcolor='#111827',
                height=400,
                margin=dict(l=60, r=40, t=80, b=60),
                showlegend=False
            )
            st.plotly_chart(fig9, use_container_width=True, config={'displayModeBar': False})
        
        # --------------------------------------------------
        # GRAPHIQUE 10 : Facturation par saison
        # --------------------------------------------------
        st.markdown('<p class="graph-title">🌦️ Facturation par saison</p>', unsafe_allow_html=True)
        
        if 'Saison' in df_filtered.columns:
            df_fact_saison = df_filtered.groupby('Saison')[col_montant].sum().reset_index()
            
            fig10 = go.Figure()
            fig10.add_trace(go.Bar(
                x=df_fact_saison['Saison'],
                y=df_fact_saison[col_montant],
                marker_color=COLOR_FACT,
                marker_line_color='white',
                marker_line_width=2,
                text=df_fact_saison[col_montant].apply(lambda x: f"{format_int_with_separator(x)} MAD"),
                textposition='outside',
                textfont=dict(size=13, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
                hovertemplate='<b>%{x}</b><br>Montant: %{text}<extra></extra>'
            ))
            fig10 = apply_graph_style(
                fig10,
                title='Facturation par saison',
                x_title='Saison',
                y_title='Montant (MAD)',
                height=400
            )
            st.plotly_chart(fig10, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    
    with st.expander("📋 Voir les données filtrées", expanded=False):
        st.dataframe(
            df_filtered.style.set_properties(**{
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