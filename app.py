# app.py
import streamlit as st
import base64
import os
from config import PAGE_TITLE, PAGE_ICON, LAYOUT
from css_style import load_css

# ============================================================
# FONCTION POUR RÉCUPÉRER LE LOGO EN BASE64
# ============================================================
def get_logo_base64():
    """Retourne le logo encodé en base64 pour l'utiliser dans le HTML."""
    logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo_srm.png')
    try:
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

# --------------------------------------------------
# 1. CONFIGURATION DE LA PAGE
# --------------------------------------------------
st.set_page_config(
    page_title=PAGE_TITLE,
    layout=LAYOUT,
    page_icon=PAGE_ICON,
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 2. CSS PERSONNALISÉ
# --------------------------------------------------
load_css()

# --------------------------------------------------
# 3. INITIALISATION DE LA SESSION
# --------------------------------------------------
if 'df' not in st.session_state:
    st.session_state.df = None
if 'df_clean' not in st.session_state:
    st.session_state.df_clean = None
if 'modele' not in st.session_state:
    st.session_state.modele = None
if 'encodeurs' not in st.session_state:
    st.session_state.encodeurs = None
if 'modele_entraine' not in st.session_state:
    st.session_state.modele_entraine = False
if 'colonnes_modele' not in st.session_state:
    st.session_state.colonnes_modele = None
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Accueil"
if 'metriques_modele' not in st.session_state:
    st.session_state.metriques_modele = {}
if 'dernieres_predictions' not in st.session_state:
    st.session_state.dernieres_predictions = None
if 'dernier_rapport_ia' not in st.session_state:
    st.session_state.dernier_rapport_ia = None
if 'dernier_rapport_ia_date' not in st.session_state:
    st.session_state.dernier_rapport_ia_date = None

# --------------------------------------------------
# 4. EN-TÊTE AVEC LOGO AMÉLIORÉ (AGRANDI)
# --------------------------------------------------
logo_b64 = get_logo_base64()
if logo_b64:
    # Logo plus grand (100px) pour plus de visibilité
    logo_img = f'<img src="data:image/png;base64,{logo_b64}" alt="Logo SRM" style="height:100px; width:auto; margin-right:20px; vertical-align:middle; filter:drop-shadow(0 2px 6px rgba(0,0,0,0.15));">'
else:
    # Fallback : texte stylisé
    logo_img = '<div class="header-logo" style="font-size:2rem; padding:0.5rem 1.5rem; background:#1E88E5; border-radius:12px; color:white; font-weight:800;">SRM</div>'

st.markdown(f"""
<div class="header" style="display:flex; align-items:center; justify-content:space-between; background:linear-gradient(135deg, #0A2540 0%, #1A3A5C 100%); padding:1rem 2.5rem; border-radius:14px; margin-bottom:2rem; box-shadow:0 6px 20px rgba(10,37,64,0.2);">
    <div class="header-left" style="display:flex; align-items:center; gap:1.2rem;">
        {logo_img}
        <div>
            <div class="header-title" style="color:white; font-size:2.2rem; font-weight:700; line-height:1.2; margin:0; letter-spacing:-0.5px;">Plateforme intelligente d'aide à la décision</div>
            <div class="header-subtitle" style="color:#B0C4DE; font-size:1.1rem; font-weight:300; margin:0.1rem 0 0 0;">De la donnée à la décision : analyses, prédictions et intelligence artificielle générative.</div>
        </div>
    </div>
    <div class="header-right" style="color:#B0C4DE; text-align:right; border-left:1px solid rgba(255,255,255,0.12); padding-left:1.8rem;">
        <strong style="color:white; font-size:1.3rem; font-weight:600;">SRM-RSK</strong><br>
        <span style="font-size:0.95rem; opacity:0.8;">Régie des Eaux et d'Électricité</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 5. BARRE LATÉRALE
# --------------------------------------------------
from sidebar import render_sidebar
page, df = render_sidebar()

if df is not None:
    st.session_state.df = df

# --------------------------------------------------
# 6. PAGES
# --------------------------------------------------
if page == "🏠 Accueil":
    from components.accueil import render_accueil
    render_accueil(st.session_state.df)

elif page == "🧹 Nettoyage des données":
    from components.nettoyage import render_nettoyage
    render_nettoyage(st.session_state.df)

elif page == "📊 Analyse des données historiques":
    from components.analyse import render_analyse
    render_analyse(st.session_state.df_clean, st.session_state.df)

elif page == "📈 KPI Actuels":
    from components.kpi import render_kpi
    render_kpi(st.session_state.df)

elif page == "🔮 Prédiction de la consommation par agence":
    from components.prediction import render_prediction
    render_prediction()

elif page == "⚡ KPI Prédictifs":
    from components.kpi_predictifs import render_kpi_predictifs
    render_kpi_predictifs()

elif page == "🧠 Facteurs influençant la consommation prédite":
    from components.facteurs_influence import render_facteurs_influence
    render_facteurs_influence()

elif page == "📄 Rapport intelligent généré par IA":
    from components.rapport_ia import render_rapport_ia
    render_rapport_ia()

# --------------------------------------------------
# 7. PIED DE PAGE
# --------------------------------------------------
st.markdown("""
<div class="footer">
    © 2026 <strong>SRM-RSK</strong> - Régie des Eaux et d'Électricité · Plateforme d'analyse décisionnelle · Données confidentielles
</div>
""", unsafe_allow_html=True)