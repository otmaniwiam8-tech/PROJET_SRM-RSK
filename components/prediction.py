# components/prediction.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ============================================================
# 1. STYLE CSS (compatible avec les autres pages)
# ============================================================

def apply_prediction_style():
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
        .param-title {
            color: #FF8F00 !important;
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            margin-bottom: 0.5rem !important;
        }
        .stSelectbox label, .stNumberInput label {
            font-size: 1rem !important;
            font-weight: 600 !important;
            color: #B0D4F1 !important;
        }
        
        /* ============================================================
           BOUTON BLEU (modifié)
           ============================================================ */
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
        .stButton button:active {
            transform: translateY(0px) !important;
            box-shadow: 0 2px 8px rgba(30, 136, 229, 0.3) !important;
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
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #0D2B4A, #1A4A7A) !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            color: #B0D4F1 !important;
            border: 1px solid rgba(46, 168, 255, 0.15) !important;
            padding: 0.8rem 1.2rem !important;
        }
        .streamlit-expanderHeader:hover {
            background: linear-gradient(135deg, #1A4A7A, #0D2B4A) !important;
            border-color: rgba(46, 168, 255, 0.3) !important;
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# 2. PAGE DE PRÉDICTION
# ============================================================

def render_prediction():
    """Affiche la page de prédiction de la consommation future sans graphique."""
    
    apply_prediction_style()
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.2rem; font-weight: 700; color: #FFFFFF; margin: 0; padding: 0;">🔮 Prédiction de la consommation</h1>
        <p style="font-size: 1.1rem; color: #94A3B8; margin: 0.2rem 0 0 0;">
            Prédiction mensuelle et annuelle par agence et gérance
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================================
    # VÉRIFICATIONS
    # ============================================================
    if st.session_state.df is None:
        st.warning("⚠️ Veuillez d'abord importer un fichier dans la barre latérale.")
        st.stop()
    
    if st.session_state.df_clean is None:
        st.markdown("""
        <div class="block-message">
            <div class="icon">🚨</div>
            <h2>Données non nettoyées</h2>
            <p>
                Vous devez <strong>obligatoirement</strong> passer par la page <br>
                <strong style="color:#0D47A1; font-size:1.4rem;">'Nettoyage des données'</strong> <br>
                avant d'accéder à la prédiction.
            </p>
            <p style="font-size:1.1rem; color:#5A6C7D;">
                ⚠️ Les données brutes contiennent des valeurs manquantes, des doublons et des incohérences.<br>
                La prédiction ne sera pas fiable sans un nettoyage préalable.
            </p>
            <div class="btn-container">
        """, unsafe_allow_html=True)
        if st.button("🧹 Aller au nettoyage des données", type="primary"):
            st.session_state.page = "🧹 Nettoyage des données"
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)
        st.stop()
    
    if not st.session_state.get('modele_entraine', False) or st.session_state.modele is None:
        st.markdown("""
        <div style="background:#1E293B; border-radius:12px; padding:2rem 2.5rem; border-left:6px solid #FF8F00; text-align:center; margin:2rem 0;">
            <div style="font-size:3.5rem; margin-bottom:0.5rem;">⏳</div>
            <h2 style="color:#FFD600; font-size:1.8rem; font-weight:700; margin:0 0 0.5rem 0;">
                Entraînement du modèle en cours
            </h2>
            <p style="color:#94A3B8; font-size:1.2rem; margin:0;">
                Le modèle est en cours d'entraînement sur vos données nettoyées.<br>
                Veuillez rafraîchir la page dans quelques instants.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    # ============================================================
    # MODÈLE DISPONIBLE
    # ============================================================
    model = st.session_state.modele
    encoders = st.session_state.encodeurs
    feature_names = st.session_state.colonnes_modele
    df = st.session_state.df_clean
    
    # ============================================================
    # FILTRES
    # ============================================================
    st.markdown('<p class="param-title">📊 Paramètres de prédiction</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        agences = sorted(df['Agence'].dropna().unique().tolist())
        agence = st.selectbox("🏢 Agence", agences)
    
    with col2:
        gerances = sorted(df['Gerance'].dropna().unique().tolist())
        gerance = st.selectbox("⚡ Gérance", gerances)
    
    with col3:
        annees_existantes = sorted(df['Annee_Facture'].unique().tolist())
        annee_defaut = annees_existantes[-1] + 1 if annees_existantes else 2026
        annee = st.number_input(
            "📅 Année à prédire",
            min_value=2000,
            max_value=2100,
            value=annee_defaut,
            step=1,
            format="%d"
        )
    
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        lancer = st.button("🔮 Lancer la prédiction", type="primary", use_container_width=True)
    
    if lancer:
        try:
            agence_enc = encoders["Agence"].transform([[agence]])[0][0]
            gerance_enc = encoders["Gerance"].transform([[gerance]])[0][0]
            
            if agence_enc == -1 or gerance_enc == -1:
                st.warning("⚠️ Cette agence ou gérance n'existe pas dans les données d'entraînement.")
            
            # Déterminer la couleur et l'unité selon la gérance
            if "Électricité" in gerance or "Elec" in gerance or "électricité" in gerance.lower():
                color_principal = '#D32F2F'
                label_energie = "Électricité"
                unite = "kWh"
            elif "Eau" in gerance or "eau" in gerance.lower():
                color_principal = '#1E88E5'
                label_energie = "Eau"
                unite = "m³"
            else:
                color_principal = '#1E88E5'
                label_energie = gerance
                unite = "kWh"
            
            mois_labels = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 
                          'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
            
            predictions = []
            for mois in range(1, 13):
                X_new = pd.DataFrame({
                    "Agence": [agence_enc],
                    "Gerance": [gerance_enc],
                    "Annee_Facture": [annee],
                    "Mois": [mois]
                })
                pred = model.predict(X_new[feature_names])[0]
                predictions.append(max(0, pred))
            
            total_annuel = sum(predictions)
            moyenne = total_annuel / 12
            predictions_arrondies = [round(p, 2) for p in predictions]
            total_arrondi = round(total_annuel, 2)
            moyenne_arrondie = round(moyenne, 2)
            
            mois_max = mois_labels[np.argmax(predictions)]
            valeur_max = max(predictions)
            mois_min = mois_labels[np.argmin(predictions)]
            valeur_min = min(predictions)
            
            # ============================================================
            # STOCKAGE DES PRÉDICTIONS
            # ============================================================
            st.session_state.dernieres_predictions = {
                'mois_numeros': list(range(1, 13)),
                'mois_labels': mois_labels,
                'predictions': predictions,
                'predictions_arrondies': predictions_arrondies,
                'agence': agence,
                'gerance': gerance,
                'annee': annee,
                'unite': unite,
                'total_annuel': total_annuel,
                'moyenne': moyenne
            }
            
            st.markdown("---")
            st.markdown(f"""
            <div style="margin: 1rem 0;">
                <h2 style="color: #FFD600; font-size: 1.5rem; font-weight: 700; margin: 0;">📊 Résultats pour {agence} - {gerance} - {annee}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # ============================================================
            # KPI CARDS
            # ============================================================
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.markdown(f"""
                <div class="kpi-card" style="border-color: #FFD600;">
                    <div class="kpi-label" style="color: #FFD600;">📊 TOTAL ANNUEL</div>
                    <div class="kpi-value" style="color: #FFD600;">{total_arrondi:,.2f}</div>
                    <div class="kpi-sub">{unite}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="kpi-card" style="border-color: #00E676;">
                    <div class="kpi-label" style="color: #00E676;">📈 MOYENNE MENSUELLE</div>
                    <div class="kpi-value" style="color: #00E676;">{moyenne_arrondie:,.2f}</div>
                    <div class="kpi-sub">{unite}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="kpi-card" style="border-color: #EF5350;">
                    <div class="kpi-label" style="color: #EF5350;">📈 MOIS MAX</div>
                    <div class="kpi-value" style="color: #EF5350;">{mois_max}</div>
                    <div class="kpi-sub">{valeur_max:.2f} {unite}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="kpi-card" style="border-color: #1E88E5;">
                    <div class="kpi-label" style="color: #1E88E5;">📉 MOIS MIN</div>
                    <div class="kpi-value" style="color: #1E88E5;">{mois_min}</div>
                    <div class="kpi-sub">{valeur_min:.2f} {unite}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                st.markdown(f"""
                <div class="kpi-card" style="border-color: #6A1B9A;">
                    <div class="kpi-label" style="color: #CE93D8;">📆 NOMBRE DE MOIS</div>
                    <div class="kpi-value" style="color: #CE93D8;">12</div>
                    <div class="kpi-sub">mois</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ============================================================
            # TABLEAU DANS UN EXPANDER
            # ============================================================
            with st.expander("📋 Voir le détail des prédictions", expanded=False):
                df_pred = pd.DataFrame({
                    "Mois": mois_labels,
                    f"Consommation ({unite})": predictions_arrondies
                })
                
                st.dataframe(
                    df_pred.style.set_properties(**{
                        'font-size': '18px',
                        'font-family': 'Arial, sans-serif',
                        'padding': '12px',
                        'background-color': '#0D2B4A',
                        'color': '#E2E8F0'
                    }).set_table_styles([
                        {'selector': 'thead th', 'props': [
                            ('font-size', '18px'),
                            ('font-weight', 'bold'),
                            ('background-color', '#1A4A7A'),
                            ('color', 'white'),
                            ('padding', '14px')
                        ]},
                        {'selector': 'tbody tr:hover', 'props': [
                            ('background-color', '#1A4A7A'),
                            ('transition', '0.3s')
                        ]}
                    ]).format({f"Consommation ({unite})": "{:.2f}"}),
                    use_container_width=True,
                    height=400
                )
                
                st.caption(f"""
                📊 **Récapitulatif** :  
                • Somme des 12 mois : **{total_arrondi:.2f} {unite}**  
                • Moyenne mensuelle : **{moyenne_arrondie:.2f} {unite}**
                """)
            
            # ============================================================
            # RÉCAPITULATIF
            # ============================================================
            st.markdown("---")
            st.markdown(f"""
            <div class="info-note">
                📊 <strong>Récapitulatif</strong><br>
                • Somme des 12 mois : <strong style="color: #FFD600;">{total_arrondi:.2f} {unite}</strong><br>
                • Moyenne mensuelle : <strong style="color: #00E676;">{moyenne_arrondie:.2f} {unite}</strong><br>
                • Mois max : <strong style="color: #EF5350;">{mois_max}</strong> ({valeur_max:.2f} {unite})<br>
                • Mois min : <strong style="color: #1E88E5;">{mois_min}</strong> ({valeur_min:.2f} {unite})
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Erreur : {e}")
    else:
        st.caption("👆 Sélectionnez les paramètres et cliquez sur **Lancer la prédiction**.")
    
    # ============================================================
    # FOOTER
    # ============================================================
    st.markdown("---")
    st.caption(f"""
    📊 **Prédiction basée sur** : RandomForestRegressor entraîné sur les données historiques  
    🧠 **Modèle** : RandomForestRegressor  
    📅 Dernière mise à jour : {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}
    """)