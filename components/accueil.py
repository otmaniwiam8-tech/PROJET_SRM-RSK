# components/accueil.py
import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# STYLE CSS
# ============================================================

def apply_accueil_style():
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
        .divider {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #2EA8FF, transparent);
            margin: 1.5rem 0;
            opacity: 0.3;
        }
        .card {
            background: linear-gradient(135deg, #173B63, #1A4A7A);
            border-radius: 16px;
            padding: 1.8rem 2rem;
            border: 2px solid rgba(46, 168, 255, 0.15);
            box-shadow: 0 4px 16px rgba(46, 168, 255, 0.08);
            height: 100%;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 32px rgba(46, 168, 255, 0.15);
        }
        .card h3 {
            color: #FFD600 !important;
            font-size: 1.4rem !important;
            font-weight: 700 !important;
            margin-top: 0 !important;
            margin-bottom: 0.8rem !important;
        }
        .card p {
            color: #B0D4F1 !important;
            font-size: 1.05rem !important;
            line-height: 1.7 !important;
            margin-bottom: 0 !important;
        }
        .card ul {
            list-style-type: none;
            padding-left: 0;
            margin-bottom: 0;
        }
        .card ul li {
            color: #B0D4F1 !important;
            font-size: 1.05rem !important;
            line-height: 1.7 !important;
            padding: 0.2rem 0;
            border-bottom: 1px solid rgba(46, 168, 255, 0.05);
        }
        .card ul li:last-child {
            border-bottom: none;
        }
        .card ul li::before {
            content: "▸ ";
            color: #FF8F00;
            font-weight: 700;
        }
        .info-banner {
            background: linear-gradient(135deg, #0D2B4A, #1A4A7A);
            border-radius: 12px;
            padding: 1rem 2rem;
            margin-bottom: 1.5rem;
            border-left: 4px solid #2EA8FF;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            box-shadow: 0 2px 12px rgba(46, 168, 255, 0.06);
        }
        .info-banner strong {
            color: #FFFFFF;
            font-weight: 700;
        }
        .info-banner span {
            color: #B0D4F1;
        }
        .info-banner .date {
            color: #94A3B8;
            font-size: 0.85rem;
        }
        .col-list {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            padding: 0.5rem 0;
        }
        .col-tag {
            background: linear-gradient(135deg, #0D2B4A, #1A4A7A);
            padding: 0.4rem 1rem;
            border-radius: 24px;
            font-size: 0.85rem;
            color: #B0D4F1;
            font-weight: 500;
            border: 1px solid rgba(46, 168, 255, 0.12);
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        .col-tag:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(46, 168, 255, 0.1);
            border-color: #2EA8FF;
        }
        /* Optimisation des DataFrames */
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
        /* Supprimer les espaces vides dans les DataFrames */
        .stDataFrame .blank {
            display: none !important;
        }
        .stDataFrame .dataframe {
            margin-bottom: 0 !important;
        }
        .stDataFrame .table-container {
            padding-bottom: 0 !important;
        }
        .stDataFrame table {
            border-collapse: collapse !important;
        }
        .stDataFrame tbody tr:last-child td {
            border-bottom: none !important;
        }
        /* Supprimer tout espace supplémentaire */
        .element-container {
            margin-bottom: 0 !important;
        }
        .stDataFrame .stTable {
            border: none !important;
        }
        .badge {
            background: linear-gradient(135deg, #1E88E5, #0D47A1);
            padding: 0.6rem 2.5rem;
            border-radius: 30px;
            color: #FFFFFF;
            font-weight: 700;
            font-size: 1.3rem;
            border: 2px solid rgba(30, 136, 229, 0.4);
            display: inline-block;
            box-shadow: 0 4px 20px rgba(30, 136, 229, 0.35);
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
        }
        .badge:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 32px rgba(30, 136, 229, 0.45);
        }
        .empty-state {
            text-align: center;
            padding: 3rem 1rem;
            background: linear-gradient(135deg, #0D2B4A, #1A4A7A);
            border-radius: 16px;
            border: 2px dashed rgba(46, 168, 255, 0.15);
        }
        .empty-state .icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        .empty-state h3 {
            color: #FFFFFF !important;
            margin: 0 !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
        }
        .empty-state p {
            color: #94A3B8 !important;
            font-size: 1.1rem !important;
            margin: 0.5rem 0 0 0 !important;
        }
        /* Style pour data_editor */
        .stDataFrame {
            max-height: 500px !important;
            overflow: auto !important;
        }
        /* Supprimer les lignes vides dans les statistiques */
        .stTable table tbody tr:last-child {
            border-bottom: none !important;
        }
        .stTable table {
            margin-bottom: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# PAGE PRINCIPALE
# ============================================================

def render_accueil(df):
    """Affiche la page d'accueil avec style sombre"""
    
    apply_accueil_style()
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align:center; margin: 1rem 0 2rem 0;">
        <span class="badge">📌 Système intelligent de prédiction de la consommation par agence</span>
    </div>
    """, unsafe_allow_html=True)
    
    
    # ============================================================
    # CARTES OBJECTIF ET FONCTIONNALITÉS
    # ============================================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3> Objectif</h3>
            <p>Exploiter les données historiques afin d'analyser les tendances de consommation, d'identifier les facteurs influençant les prédictions, d'anticiper les besoins futurs par agence et de fournir une aide à la décision grâce au Machine Learning et à l'intelligence artificielle générative.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Fonctionnalités</h3>
            <ul>
                <li>📊 Analyse des données historiques</li>
                <li>🔮 Prédiction annuelle de consommation par agence</li>
                <li>📈 KPI et facteurs d'influence</li>
                <li>🤖 Rapport intelligent généré par IA</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
    # ============================================================
    # ÉTAT DES DONNÉES
    # ============================================================
    if df is not None:
        st.markdown(f"""
        <div class="info-banner">
            <div>
                <strong>✅ Données chargées</strong>
                <span style="margin-left:1rem;">{df.shape[0]:,} lignes · {df.shape[1]} colonnes</span>
            </div>
            <div class="date">
                📅 Mise à jour : {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ============================================================
        # LISTE DES COLONNES
        # ============================================================
        st.markdown('<h2 class="section-title">📋 Colonnes disponibles</h2>', unsafe_allow_html=True)
        
        colonnes = df.columns.tolist()
        cols_html = "".join([f'<span class="col-tag">{col}</span>' for col in colonnes])
        st.markdown(f'<div class="col-list">{cols_html}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ============================================================
        # APERÇU COMPLET DES DONNÉES (AFFICHÉ DIRECTEMENT)
        # ============================================================
        st.markdown('<h2 class="section-title">📊 Aperçu complet des données</h2>', unsafe_allow_html=True)
        st.caption(f"📌 Affichage de toutes les lignes ({df.shape[0]:,} lignes)")
        
        # Utiliser st.data_editor avec height pour le scroll
        st.data_editor(
            df,
            use_container_width=True,
            height=500,
            disabled=True,
            hide_index=False,
            num_rows="fixed"
        )
        
        # ============================================================
        # STATISTIQUES DESCRIPTIVES (SANS LIGNES VIDES)
        # ============================================================
        st.markdown("---")
        st.markdown('<h2 class="section-title">📊 Statistiques descriptives</h2>', unsafe_allow_html=True)
        
        # Sélectionner uniquement les colonnes numériques pour les statistiques
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            # Calculer les statistiques uniquement sur les colonnes numériques
            stats_df = df[numeric_cols].describe()
            
            # Réorganiser les colonnes pour un meilleur affichage
            priority_cols = ['Consommation', 'Montant_Tete_Facture', 'Hors_Taxe', 'TVA', 'TTC']
            other_cols = [col for col in numeric_cols if col not in priority_cols]
            ordered_cols = [col for col in priority_cols if col in numeric_cols] + other_cols
            
            stats_df = stats_df[ordered_cols]
            
            # Afficher le tableau avec height automatique basé sur le nombre de lignes
            # 8 lignes de données + 1 en-tête = 9 lignes au total
            row_height = 35  # hauteur approximative d'une ligne
            header_height = 40  # hauteur de l'en-tête
            total_height = (len(stats_df) * row_height) + header_height + 10
            
            # Utiliser st.dataframe avec height calculé automatiquement
            st.dataframe(
                stats_df,
                use_container_width=True,
                height=total_height
            )
        else:
            st.info("💡 Aucune colonne numérique disponible pour les statistiques descriptives.")
            
    else:
        # ============================================================
        # ÉTAT VIDE
        # ============================================================
        st.markdown("""
        <div class="empty-state">
            <div class="icon">📂</div>
            <h3>Aucune donnée chargée</h3>
            <p>Veuillez importer un fichier CSV ou Excel dans la barre latérale (à gauche).</p>
        </div>
        """, unsafe_allow_html=True)