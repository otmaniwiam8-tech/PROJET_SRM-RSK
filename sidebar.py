# sidebar.py
import streamlit as st
import pandas as pd
from data_loader import load_multiple_files

def render_sidebar():
    """Affiche la barre latérale avec le menu et l'upload"""
    with st.sidebar:
        st.markdown('<div class="sidebar-title">📂 Menu</div>', unsafe_allow_html=True)
        
        page = st.radio(
            "Aller à :",
            [
                "🏠 Accueil",
                "🧹 Nettoyage des données",
                "📊 Analyse des données historiques",
                "📈 KPI Actuels",
                "🔮 Prédiction de la consommation par agence",
                "⚡ KPI Prédictifs",
                "🧠 Facteurs influençant la consommation prédite",
                "📄 Rapport intelligent généré par IA"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        st.markdown('<p style="color:#B0C4DE; font-size:0.85rem; font-weight:500; margin-bottom:0.5rem;">📂 Importer vos données</p>', unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader(
            " ",
            type=['csv', 'xlsx', 'xls'],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        
        st.markdown('<p style="color:#5A7A9A; font-size:0.7rem; margin-top:-0.3rem;">200MB per file • CSV, XLSX, XLS • Plusieurs fichiers acceptés</p>', unsafe_allow_html=True)
        
        df = None
        if uploaded_files is not None and len(uploaded_files) > 0:
            try:
                result = load_multiple_files(uploaded_files)
                if result:
                    df, file_names = result
                    if len(uploaded_files) == 1:
                        st.markdown(f'<div class="sidebar-success">✅ {df.shape[0]} lignes chargées (1 fichier)</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="sidebar-success">✅ {df.shape[0]} lignes chargées ({len(uploaded_files)} fichiers)</div>', unsafe_allow_html=True)
                    
                    st.markdown(f'<div style="color:#B0C4DE; font-size:0.85rem;">📊 {df.shape[1]} colonnes</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="color:#5A7A9A; font-size:0.75rem; margin-top:0.3rem;">📄 {", ".join(file_names)}</div>', unsafe_allow_html=True)
                    
                    st.session_state.df = df
                    
            except Exception as e:
                st.markdown(f'<div class="sidebar-error">❌ Erreur : {e}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="sidebar-info">📥 Aucun fichier chargé</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style="color:#5A7A9A; font-size:0.7rem; text-align:center; padding-top:0.5rem; opacity:0.7;">
            <strong style="color:#B0C4DE;">SRM-RSK</strong><br>
            Données confidentielles
        </div>
        """, unsafe_allow_html=True)
    
    return page, df