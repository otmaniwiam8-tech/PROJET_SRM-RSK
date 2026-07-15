# components/facteurs_influence.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import shap

# ============================================================
# 1. STYLE CSS
# ============================================================

def apply_style():
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
            font-size: 12px;
            font-weight: 600;
            color: #B0D4F1;
            margin-bottom: 0.2rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .kpi-card .kpi-value {
            font-size: 32px;
            font-weight: 700;
            color: #FFFFFF;
            line-height: 1.1;
        }
        .kpi-card .kpi-sub {
            font-size: 14px;
            color: #B0D4F1;
        }
        .interpretation-box {
            background: #1E293B;
            border-radius: 12px;
            padding: 2rem 2.5rem;
            border-left: 6px solid #FF8F00;
            margin: 1rem 0;
        }
        .interpretation-box h4 {
            color: #FF8F00 !important;
            font-size: 1.6rem !important;
            margin-top: 0 !important;
            margin-bottom: 1.2rem !important;
            font-weight: 700 !important;
        }
        .interpretation-box p {
            color: #E2E8F0 !important;
            font-size: 1.2rem !important;
            line-height: 1.8 !important;
            margin: 0.7rem 0 !important;
        }
        .interpretation-box strong {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }
        .interpretation-box .highlight {
            color: #FFD600 !important;
            font-size: 1.4rem !important;
            font-weight: 700 !important;
        }
        .interpretation-box .positive {
            color: #00E676 !important;
            font-weight: 700 !important;
        }
        .interpretation-box .negative {
            color: #EF5350 !important;
            font-weight: 700 !important;
        }
        .interpretation-box .neutral {
            color: #FF8F00 !important;
            font-weight: 700 !important;
        }
        .interpretation-box hr {
            border-color: #2A3441 !important;
            margin: 1.2rem 0 !important;
        }
        .interpretation-box .summary {
            color: #B0D4F1 !important;
            font-size: 1.15rem !important;
            margin: 0 !important;
        }
        .interpretation-box .summary strong {
            color: #FFFFFF !important;
        }
        .interpretation-box .summary .total {
            color: #FFD600 !important;
            font-size: 1.4rem !important;
            font-weight: 700 !important;
        }
        .interpretation-box .italic-note {
            font-style: italic !important;
            color: #94A3B8 !important;
            font-size: 1.1rem !important;
            margin-top: 0.8rem !important;
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
        .verification-box {
            background: #0D2B4A;
            border-radius: 10px;
            padding: 0.8rem 1.5rem;
            border: 1px solid #2EA8FF;
            text-align: center;
            color: #B0D4F1;
            font-size: 14px;
            margin: 0.5rem 0;
        }
        .verification-box strong {
            color: #FFFFFF;
        }
        .verification-box .ok {
            color: #00E676;
        }
        .verification-box .ko {
            color: #EF5350;
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# 2. FONCTIONS SHAP
# ============================================================

def calculer_shap(df, model, feature_names):
    """Calcule les valeurs SHAP pour une prédiction donnée."""
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(df[feature_names])
        return shap_values, explainer
    except Exception as e:
        st.error(f"❌ Erreur lors du calcul SHAP : {e}")
        return None, None

def generer_interpretation(df_shap, agence, gerance, annee, pred_value, unite, total_annuel):
    """Génère une interprétation métier automatique avec le total annuel."""
    if df_shap.empty:
        return "Aucune donnée SHAP disponible."
    
    max_pos = df_shap.loc[df_shap['Contribution'].idxmax()]
    max_neg = df_shap.loc[df_shap['Contribution'].idxmin()]
    nb_pos = len(df_shap[df_shap['Contribution'] > 0])
    nb_neg = len(df_shap[df_shap['Contribution'] < 0])
    
    # Déterminer le facteur avec la plus grande influence (positive ou négative)
    max_abs = df_shap.loc[df_shap['Contribution'].abs().idxmax()]
    
    return f"""
    <div class="interpretation-box">
        <h4 style="color: #FF8F00; margin-top: 0;">📊 Analyse des facteurs d'influence</h4>
        <p>
            <strong>📌 Prédiction analysée :</strong> {agence} - {gerance} - {annee}<br>
            <strong>⚡ Consommation prédite annuelle :</strong> <span style="color: #FFD600; font-size: 1.2rem;">{total_annuel:.2f} {unite}</span><br>
            <strong>📊 Moyenne mensuelle :</strong> {pred_value:.2f} {unite}
        </p>
        <p>
            <strong>🏆 Facteur le plus influent :</strong> <span style="color: #00E676;">{max_pos['Facteur']}</span> 
            (contribution de <strong>+{max_pos['Contribution']:.2f}</strong> {unite})
        </p>
        <p>
            <strong>📉 Facteur le moins influent :</strong> <span style="color: #EF5350;">{max_neg['Facteur']}</span> 
            (contribution de <strong>{max_neg['Contribution']:.2f}</strong> {unite})
        </p>
        <p>
            <strong>⚖️ Équilibre global :</strong> {nb_pos} facteurs augmentent la consommation, 
            {nb_neg} facteurs la diminuent.
        </p>
        <p>
            <strong>🎯 Facteur avec la plus grande influence absolue :</strong> 
            <span style="color: #FF8F00;">{max_abs['Facteur']}</span> 
            (contribution de <strong>{max_abs['Contribution']:.2f}</strong> {unite})
        </p>
        <p style="font-style: italic; color: #94A3B8; margin-top: 0.5rem;">
            💡 Ces informations permettent d'identifier les leviers d'action pour optimiser 
            la consommation et orienter les décisions stratégiques.
        </p>
        <hr style="border-color: #2A3441; margin: 0.8rem 0;">
        <p style="color: #B0D4F1; font-size: 0.95rem; margin: 0;">
            📊 <strong>Résumé :</strong> Pour l'année <strong>{annee}</strong>, 
            la consommation prédite pour <strong>{agence}</strong> - <strong>{gerance}</strong> 
            est de <strong style="color: #FFD600; font-size: 1.1rem;">{total_annuel:.2f} {unite}</strong>, 
            soit une moyenne de <strong>{pred_value:.2f} {unite}</strong> par mois.
        </p>
    </div>
    """

# ============================================================
# 3. FONCTIONS D'AFFICHAGE
# ============================================================

def afficher_kpi_shap(df_shap, pred_value, unite, total_annuel):
    """Affiche les KPI SHAP avec mise en avant du facteur le plus influent."""
    if df_shap.empty:
        st.warning("Aucune donnée SHAP disponible.")
        return
    
    max_pos = df_shap.loc[df_shap['Contribution'].idxmax()]
    max_neg = df_shap.loc[df_shap['Contribution'].idxmin()]
    
    # ============================================================
    # LIGNE 1 : KPI PRINCIPAL + 2 KPI secondaires
    # ============================================================
    col_main, col_right1, col_right2 = st.columns([2, 1, 1])
    
    with col_main:
        st.markdown(f"""
        <div class="kpi-card" style="
            background: linear-gradient(135deg, #1A4A7A, #0D2B4A);
            border: 3px solid #FF8F00;
            height: auto;
            min-height: 110px;
            padding: 0.8rem 1.2rem;
            box-shadow: 0 0 25px rgba(255, 143, 0, 0.15);
        ">
            <div class="kpi-label" style="font-size: 11px; color: #FFD54F; letter-spacing: 0.5px;">🏆 FACTEUR LE PLUS INFLUENT</div>
            <div class="kpi-value" style="font-size: 30px; color: #FFD54F; line-height: 1.1;">{max_pos['Facteur']}</div>
            <div style="display: flex; align-items: center; gap: 8px; margin-top: 2px;">
                <span style="font-size: 15px; color: #FFE082; font-weight: 600;">+{max_pos['Contribution']:.2f} {unite}</span>
                <span style="font-size: 11px; color: #B0D4F1; background: rgba(255,255,255,0.05); padding: 2px 8px; border-radius: 10px;">
                    ⬆️ {max_pos['Niveau']}
                </span>
            </div>
            <div style="font-size: 11px; color: #90CAF9; margin-top: 2px;">
                🔹 {max_pos['Valeur']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right1:
        st.markdown(f"""
        <div class="kpi-card" style="height: 110px; border-color: #FFD600; padding: 0.8rem 1rem;">
            <div class="kpi-label" style="font-size: 10px; color: #FFD600;">📊 CONSOMMATION PRÉDITE ANNUELLE</div>
            <div class="kpi-value" style="font-size: 28px; line-height: 1.1; color: #FFD600;">{total_annuel:.1f}</div>
            <div class="kpi-sub" style="font-size: 12px; color: #B0D4F1;">{unite} · {total_annuel/12:.1f} {unite}/mois</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right2:
        st.markdown(f"""
        <div class="kpi-card" style="height: 110px; border-color: #EF5350; padding: 0.8rem 1rem;">
            <div class="kpi-label" style="font-size: 10px;">📉 FREIN PRINCIPAL</div>
            <div class="kpi-value" style="font-size: 20px; line-height: 1.1; color: #EF5350;">{max_neg['Facteur']}</div>
            <div class="kpi-sub" style="font-size: 12px; color: #EF5350;">{max_neg['Contribution']:.2f} {unite}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================================
    # LIGNE 2 : KPI secondaires (3 colonnes)
    # ============================================================
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card" style="height: 90px; padding: 0.6rem 0.8rem;">
            <div class="kpi-label" style="font-size: 10px;">📈 CONTRIBUTION +</div>
            <div class="kpi-value" style="font-size: 22px; color: #00E676; line-height: 1.1;">+{max_pos['Contribution']:.2f}</div>
            <div class="kpi-sub" style="font-size: 11px;">{unite}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card" style="height: 90px; padding: 0.6rem 0.8rem;">
            <div class="kpi-label" style="font-size: 10px;">📉 CONTRIBUTION -</div>
            <div class="kpi-value" style="font-size: 22px; color: #EF5350; line-height: 1.1;">{max_neg['Contribution']:.2f}</div>
            <div class="kpi-sub" style="font-size: 11px;">{unite}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        nb_pos = len(df_shap[df_shap['Contribution'] > 0])
        nb_neg = len(df_shap[df_shap['Contribution'] < 0])
        st.markdown(f"""
        <div class="kpi-card" style="height: 90px; padding: 0.6rem 0.8rem;">
            <div class="kpi-label" style="font-size: 10px;">⚖️ ÉQUILIBRE</div>
            <div class="kpi-value" style="font-size: 20px; line-height: 1.1;">
                <span style="color: #00E676;">+{nb_pos}</span>
                <span style="color: #94A3B8; font-size: 16px;">/</span>
                <span style="color: #EF5350;">-{nb_neg}</span>
            </div>
            <div class="kpi-sub" style="font-size: 11px;">facteurs</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# 4. GRAPHIQUES PLOTLY
# ============================================================

def afficher_graphique_barres(df_shap, unite):
    """Graphique 1 : Barres horizontales des contributions SHAP."""
    if df_shap.empty:
        st.warning("Aucune donnée SHAP disponible.")
        return
    
    mapping = {'Agence': 'Agence', 'Gerance': 'Gérance', 'Annee_Facture': 'Année', 'Mois': 'Mois'}
    df = df_shap.copy()
    df['Facteur_affichage'] = df['Facteur'].map(lambda x: mapping.get(x, x))
    
    colors = ['#00E676' if x > 0 else '#EF5350' for x in df['Contribution']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Contribution'],
        y=df['Facteur_affichage'],
        orientation='h',
        marker_color=colors,
        text=df['Contribution'].apply(lambda x: f"{x:+.2f}"),
        textposition='outside',
        textfont=dict(size=14, color='#FFFFFF'),
        hovertemplate='<b>%{y}</b><br>Contribution: %{x:+.2f} ' + unite + '<extra></extra>',
        width=0.7
    ))
    fig.update_layout(
        title=dict(
            text="📊 Contribution des facteurs à la consommation prédite",
            font=dict(size=18, color='#FFFFFF'),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#111827',
        paper_bgcolor='#111827',
        height=400,
        margin=dict(l=20, r=80, t=50, b=20),
        xaxis=dict(
            title=dict(text=f"Contribution SHAP ({unite})", font=dict(size=14, color='#94A3B8')),
            tickfont=dict(size=13, color='#94A3B8'),
            gridcolor='rgba(255,255,255,0.05)',
            showgrid=True,
            zeroline=True,
            zerolinecolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            tickfont=dict(size=14, color='#FFFFFF'),
            showgrid=False
        ),
        bargap=0.25
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def afficher_waterfall(df_shap, base_value, unite, agence, annee):
    """Graphique 2 : Waterfall Chart avec Plotly."""
    if df_shap.empty:
        st.warning("Aucune donnée SHAP disponible.")
        return
    
    mapping = {'Agence': 'Agence', 'Gerance': 'Gérance', 'Annee_Facture': 'Année', 'Mois': 'Mois'}
    df = df_shap.sort_values('Contribution', ascending=False).reset_index(drop=True)
    df['Facteur_affichage'] = df['Facteur'].map(lambda x: mapping.get(x, x))
    
    contributions = df['Contribution'].values
    facteurs = df['Facteur_affichage'].values
    cumul = np.cumsum(contributions) + base_value
    
    colors = ['#00E676' if x > 0 else '#EF5350' for x in contributions]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=facteurs,
        y=contributions,
        marker_color=colors,
        text=contributions,
        texttemplate='%{text:+.2f}',
        textposition='outside',
        textfont=dict(size=13, color='#FFFFFF'),
        name='Contribution SHAP',
        hovertemplate='<b>%{x}</b><br>Contribution: %{y:+.2f} ' + unite + '<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=facteurs,
        y=cumul,
        mode='lines+markers+text',
        name='Valeur cumulée',
        line=dict(color='#FFD600', width=2, dash='dash'),
        marker=dict(size=10, color='#FFD600', line=dict(color='white', width=1)),
        text=cumul,
        texttemplate='%{text:.1f}',
        textposition='top center',
        textfont=dict(size=12, color='#FFD600'),
        hovertemplate='<b>Cumul</b><br>%{y:.2f} ' + unite + '<extra></extra>'
    ))
    
    fig.add_hline(
        y=base_value,
        line_dash="dash",
        line_color="#94A3B8",
        line_width=1.5,
        annotation_text=f"Base: {base_value:.2f}",
        annotation_font=dict(size=11, color='#94A3B8'),
        annotation_position="bottom right"
    )
    
    fig.update_layout(
        title=dict(
            text=f"🌊 Construction de la consommation prédite - {agence} ({annee})",
            font=dict(size=18, color='#FFFFFF'),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#111827',
        paper_bgcolor='#111827',
        height=450,
        margin=dict(l=40, r=40, t=60, b=60),
        xaxis=dict(
            tickfont=dict(size=13, color='#FFFFFF'),
            gridcolor='rgba(255,255,255,0.05)',
            showgrid=True
        ),
        yaxis=dict(
            title=dict(text=f"Consommation ({unite})", font=dict(size=14, color='#94A3B8')),
            tickfont=dict(size=13, color='#94A3B8'),
            gridcolor='rgba(255,255,255,0.05)',
            showgrid=True
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.25,
            xanchor='center',
            x=0.5,
            font=dict(size=12, color='#E2E8F0')
        ),
        bargap=0.3
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ============================================================
# 5. HEATMAP (Palette discrète : Bleu pour Eau, Rouge pour Électricité)
# ============================================================

def afficher_heatmap_facteurs(pred_data, agence, annee, unite):
    """
    Graphique 3 : Heatmap des consommations mensuelles
    Palette discrète selon la gérance :
    - Eau : dégradé de bleu (clair → foncé)
    - Électricité : dégradé de rouge (clair → foncé)
    4 niveaux de couleur basés sur les quartiles.
    """
    
    mois_labels = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 
                   'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
    predictions = pred_data['predictions']
    
    # Déterminer le type d'énergie pour le titre et la palette
    gerance = pred_data.get('gerance', '')
    if "Électricité" in gerance or "Elec" in gerance or "électricité" in gerance.lower():
        icon = "⚡"
        type_energie = "Électricité"
        # Palette rouge (clair → foncé)
        colors = ['#FFCDD2', '#EF5350', '#C62828', '#8B0000']  # faible → élevé
    elif "Eau" in gerance or "eau" in gerance.lower():
        icon = "💧"
        type_energie = "Eau"
        # Palette bleue (clair → foncé)
        colors = ['#BBDEFB', '#42A5F5', '#1565C0', '#0B3D91']  # faible → élevé
    else:
        icon = "📊"
        type_energie = "Consommation"
        # Palette neutre (gris)
        colors = ['#E0E0E0', '#9E9E9E', '#616161', '#212121']
    
    # Créer 4 classes basées sur les quartiles
    valeurs = np.array(predictions)
    if len(valeurs) > 0:
        q25 = np.percentile(valeurs, 25)
        q50 = np.percentile(valeurs, 50)
        q75 = np.percentile(valeurs, 75)
        bins = [-np.inf, q25, q50, q75, np.inf]
        labels = [0, 1, 2, 3]
        categories = pd.cut(valeurs, bins=bins, labels=labels, include_lowest=True)
        categories = categories.fillna(2).astype(int)
    else:
        categories = np.array([2]*12)
    
    # Créer une matrice de catégories (1 ligne, 12 colonnes)
    z = categories.reshape(1, -1)
    
    # Définir la colorscale pour Plotly avec des paliers
    n = len(colors)
    step = 1.0 / n
    colorscale = []
    for i, col in enumerate(colors):
        colorscale.append([i * step, col])
        colorscale.append([(i+1) * step, col])
    # Supprimer le dernier doublon pour éviter un écart inutile
    # Mais on garde la dernière valeur à 1.0 avec la dernière couleur
    # La méthode ci-dessus fonctionne correctement.
    
    # Création du graphique
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=mois_labels,
        y=['Consommation'],
        colorscale=colorscale,
        zmin=0,
        zmax=3,
        text=[predictions],
        texttemplate='%{text:.1f}',
        textfont=dict(size=18, color='white', weight='bold'),
        hovertemplate='<b>%{x}</b><br>Consommation: %{text:.2f} ' + unite + '<extra></extra>',
        showscale=True,
        colorbar=dict(
            title=dict(text=f"Consommation ({unite})", font=dict(size=14, color='#94A3B8')),
            tickfont=dict(size=12, color='#94A3B8'),
            tickvals=[0, 1, 2, 3],
            ticktext=['Très faible', 'Faible', 'Élevée', 'Très élevée'],
            len=0.8,
            thickness=25,
            x=1.02,
            xanchor='left',
            outlinewidth=1,
            outlinecolor='#2A3441'
        ),
        xgap=3,
        ygap=3
    ))
    
    fig.update_layout(
        title=dict(
            text=f"{icon} Heatmap des consommations mensuelles - {type_energie} ({annee})",
            font=dict(size=20, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            tickfont=dict(size=16, color='#FFFFFF', weight='bold'),
            side='bottom',
            showgrid=False,
            zeroline=False,
            automargin=True
        ),
        yaxis=dict(
            tickfont=dict(size=16, color='#FFFFFF', weight='bold'),
            showticklabels=True,
            showgrid=False,
            zeroline=False,
            automargin=True
        ),
        plot_bgcolor='#111827',
        paper_bgcolor='#111827',
        height=350,
        margin=dict(l=80, r=120, t=60, b=60)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # ============================================================
    # TABLEAU DES VALEURS
    # ============================================================
    with st.expander("📋 Voir le détail des valeurs mensuelles", expanded=False):
        df_detail = pd.DataFrame({
            'Mois': mois_labels,
            'Consommation': predictions
        })
        st.dataframe(
            df_detail.style.format({
                'Consommation': '{:.2f}'
            }).set_properties(**{
                'font-size': '14px',
                'padding': '6px',
                'background-color': '#0D2B4A',
                'color': '#E2E8F0'
            }).set_table_styles([
                {'selector': 'thead th', 'props': [
                    ('background-color', '#1A4A7A'),
                    ('color', 'white'),
                    ('font-weight', 'bold'),
                    ('padding', '8px')
                ]}
            ]),
            use_container_width=True
        )
        
        # Statistiques
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total", f"{sum(predictions):.2f} {unite}")
        with col2:
            max_idx = np.argmax(predictions)
            st.metric("📈 Max", f"{max(predictions):.2f} {unite} ({mois_labels[max_idx]})")
        with col3:
            min_idx = np.argmin(predictions)
            st.metric("📉 Min", f"{min(predictions):.2f} {unite} ({mois_labels[min_idx]})")

# ============================================================
# 6. PAGE PRINCIPALE
# ============================================================

def render_facteurs_influence():
    """Page d'analyse des facteurs influençant la consommation prédite (SHAP)."""
    
    apply_style()
    
    # En-tête
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.2rem; font-weight: 700; color: #FFFFFF; margin: 0; padding: 0;">🧠 Facteurs influençant la consommation prédite</h1>
        <p style="font-size: 1.1rem; color: #94A3B8; margin: 0.2rem 0 0 0;">
            Analyse SHAP des facteurs expliquant la prédiction actuelle
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================================
    # 6.1 VÉRIFICATIONS
    # ============================================================
    if not st.session_state.get('modele_entraine', False) or st.session_state.modele is None:
        st.warning("⚠️ Veuillez d'abord effectuer une prédiction dans la page 📊 Prédiction de la consommation !")
        return
    
    if 'dernieres_predictions' not in st.session_state or st.session_state.dernieres_predictions is None:
        st.warning("⚠️ Veuillez d'abord effectuer une prédiction dans la page 📊 Prédiction de la consommation !")
        return
    
    model = st.session_state.modele
    feature_names = st.session_state.colonnes_modele
    encoders = st.session_state.encodeurs
    pred_data = st.session_state.dernieres_predictions
    
    agence = pred_data['agence']
    gerance = pred_data['gerance']
    annee = pred_data['annee']
    unite = pred_data['unite']
    predictions = pred_data['predictions']
    total_annuel = pred_data.get('total_annuel', np.sum(predictions))
    pred_value = total_annuel / 12
    
    st.info(f"📊 Analyse pour : **{agence}** - **{gerance}** - **{annee}**")
    
    # ============================================================
    # 6.2 PRÉPARATION DES DONNÉES SHAP
    # ============================================================
    try:
        agence_enc = encoders["Agence"].transform([[agence]])[0][0]
        gerance_enc = encoders["Gerance"].transform([[gerance]])[0][0]
    except Exception as e:
        st.error(f"❌ Erreur d'encodage : {e}")
        return
    
    X_shap = pd.DataFrame({
        "Agence": [agence_enc] * 12,
        "Gerance": [gerance_enc] * 12,
        "Annee_Facture": [annee] * 12,
        "Mois": list(range(1, 13))
    })
    
    # ============================================================
    # 6.3 CALCUL SHAP
    # ============================================================
    shap_values, explainer = calculer_shap(X_shap, model, feature_names)
    if shap_values is None:
        return
    
    shap_mean = np.mean(shap_values, axis=0)
    
    if hasattr(explainer, 'expected_value'):
        base_value = explainer.expected_value
        if isinstance(base_value, np.ndarray):
            base_value = base_value[0] if len(base_value) > 0 else 0
    else:
        base_value = np.mean(shap_values)
    
    df_shap = pd.DataFrame({
        'Facteur': feature_names,
        'Contribution': shap_mean
    })
    df_shap = df_shap.sort_values('Contribution', ascending=False).reset_index(drop=True)
    df_shap['Rang'] = df_shap.index + 1
    
    # Définir le niveau
    abs_max = df_shap['Contribution'].abs().max() or 1
    df_shap['Niveau'] = df_shap['Contribution'].apply(
        lambda x: 'Très fort' if abs(x) > 0.6 * abs_max else
                 'Fort' if abs(x) > 0.3 * abs_max else
                 'Moyen' if abs(x) > 0.1 * abs_max else
                 'Faible'
    )
    
    # Valeurs utilisées
    valeurs = {
        'Agence': agence, 
        'Gerance': gerance, 
        'Annee_Facture': str(annee), 
        'Mois': 'Moyenne sur 12 mois'
    }
    df_shap['Valeur'] = df_shap['Facteur'].map(lambda x: valeurs.get(x, 'N/A'))
    
    # ============================================================
    # 6.4 AFFICHAGE
    # ============================================================
    
    # KPI
    st.markdown('<h2 class="section-title">📊 Indicateurs clés</h2>', unsafe_allow_html=True)
    afficher_kpi_shap(df_shap, pred_value, unite, total_annuel)
    st.markdown("---")
    
    # Note
    st.markdown("""
    <div class="info-note">
        📋 Les détails des contributions SHAP sont visibles dans les graphiques ci-dessous.
        <br>Les barres en vert augmentent la consommation, celles en rouge la diminuent.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # Graphiques
    st.markdown('<h2 class="section-title">📊 Visualisation des contributions</h2>', unsafe_allow_html=True)
    
    st.markdown('<p class="graph-title">📊 1. Contribution des facteurs à la consommation prédite</p>', unsafe_allow_html=True)
    afficher_graphique_barres(df_shap, unite)
    st.markdown("---")
    
    st.markdown('<p class="graph-title">🌊 2. Construction de la consommation prédite</p>', unsafe_allow_html=True)
    afficher_waterfall(df_shap, base_value, unite, agence, annee)
    st.markdown("---")
    
    # HEATMAP (palette améliorée)
    st.markdown('<p class="graph-title">🌡️ 3. Heatmap des consommations mensuelles</p>', unsafe_allow_html=True)
    afficher_heatmap_facteurs(pred_data, agence, annee, unite)
    st.markdown("---")
    
    # Interprétation (à la fin)
    st.markdown('<h2 class="section-title">📝 Interprétation automatique</h2>', unsafe_allow_html=True)
    st.markdown(generer_interpretation(df_shap, agence, gerance, annee, pred_value, unite, total_annuel), unsafe_allow_html=True)
    st.markdown("---")
    
    # Footer
    st.caption(f"""
    📊 **Analyse SHAP** - Prédiction du {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}  
    🧠 **Modèle** : RandomForestRegressor (entraîné sur les données historiques)
    """)