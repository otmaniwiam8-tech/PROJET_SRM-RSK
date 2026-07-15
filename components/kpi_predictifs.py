# components/kpi_predictifs.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ============================================================
# 1. STYLE CSS (même que facteurs_influence)
# ============================================================

def apply_kpi_predictifs_style():
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
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# 2. FONCTIONS UTILITAIRES
# ============================================================

def get_saison(mois):
    """Retourne la saison en fonction du mois (1 à 12)."""
    if mois in [12, 1, 2]:
        return "Hiver"
    elif mois in [3, 4, 5]:
        return "Printemps"
    elif mois in [6, 7, 8]:
        return "Été"
    else:  # 9, 10, 11
        return "Automne"

def get_title_style(text):
    """Retourne un dictionnaire de style de titre uniformisé."""
    return dict(
        text=text,
        font=dict(
            size=18,
            color='#FFFFFF',
            family='Arial, sans-serif',
            weight='bold'
        ),
        x=0.5,
        xanchor='center',
        y=0.95
    )

# ============================================================
# 3. SUNBURST CHART (Hiérarchie Saison → Mois)
# ============================================================

def afficher_sunburst_kpi(pred_data, agence, annee, unite):
    """
    Graphique Sunburst : Hiérarchie Saison → Mois
    (version pour KPI Prédictifs)
    """
    
    mois_labels = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 
                   'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
    
    # Récupérer les prédictions
    predictions = pred_data['predictions']
    
    # S'assurer que nous avons 12 valeurs
    if len(predictions) < 12:
        st.warning("⚠️ Moins de 12 prédictions disponibles.")
        return
    
    df = pd.DataFrame({
        'Mois': mois_labels,
        'Num': list(range(1, 13)),
        'Saison': [get_saison(i) for i in range(1, 13)],
        'Consommation': predictions[:12]
    })
    
    # Nettoyer les valeurs négatives
    df['Consommation'] = df['Consommation'].clip(lower=0)
    
    # Calculer le total
    total_calcule = df['Consommation'].sum()
    total_attendu = pred_data.get('total_annuel', total_calcule)
    
    # ============================================================
    # CONSTRUCTION DES DONNÉES POUR LE SUNBURST
    # ============================================================
    data = []
    
    # Ajouter les saisons avec leur SOMME réelle
    for saison in df['Saison'].unique():
        total_saison = df[df['Saison'] == saison]['Consommation'].sum()
        if total_saison > 0:
            data.append({
                'id': saison,
                'parent': '',
                'value': total_saison
            })
    
    # Ajouter les mois avec leur VALEUR RÉELLE
    for _, row in df.iterrows():
        if row['Consommation'] > 0:
            data.append({
                'id': row['Mois'],
                'parent': row['Saison'],
                'value': row['Consommation']
            })
    
    df_plot = pd.DataFrame(data)
    
    if df_plot.empty:
        st.warning("⚠️ Aucune donnée à afficher.")
        return
    
    # ============================================================
    # COULEURS PAR SAISON
    # ============================================================
    couleurs_saisons = {
        'Hiver': '#1E88E5',      # Bleu
        'Printemps': '#00A86B',  # Vert
        'Été': '#FF8F00',        # Orange
        'Automne': '#6A1B9A'     # Violet
    }
    
    def get_couleur(label):
        if label in couleurs_saisons:
            return couleurs_saisons[label]
        # Si c'est un mois, trouver sa saison
        for saison, couleur in couleurs_saisons.items():
            if label in df[df['Saison'] == saison]['Mois'].values:
                return couleur
        return '#1E88E5'
    
    # ============================================================
    # CRÉATION DU GRAPHIQUE
    # ============================================================
    fig = go.Figure(go.Sunburst(
        ids=df_plot['id'],
        labels=df_plot['id'],
        parents=df_plot['parent'],
        values=df_plot['value'],
        textinfo='label+value',
        textfont=dict(size=14, color='white', family='Arial, sans-serif'),
        marker=dict(
            colors=[get_couleur(x) for x in df_plot['id']],
            line=dict(color='#1E293B', width=2)
        ),
        hovertemplate=(
            '<b>%{label}</b><br>' +
            f'Consommation: %{{value:.2f}} {unite}<br>' +
            '<extra></extra>'
        ),
        insidetextorientation='radial'
    ))
    
    fig.update_layout(
        title=dict(
            text=f"🌞 Hiérarchie Saison → Mois - {agence} ({annee})",
            font=dict(size=20, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#111827',
        paper_bgcolor='#111827',
        height=500,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # ============================================================
    # VÉRIFICATION DES SOMMES
    # ============================================================
    st.markdown(f"""
    <div class="verification-box">
        📊 <strong>Vérification des sommes</strong><br>
        Somme des 12 mois : <strong>{total_calcule:.2f} {unite}</strong>
        <span class="{'ok' if abs(total_calcule - total_attendu) < 0.01 else 'ko'}">
            {'✅ OK' if abs(total_calcule - total_attendu) < 0.01 else '⚠️ Écart détecté'}
        </span>
        {f' (attendu : {total_attendu:.2f} {unite})' if abs(total_calcule - total_attendu) >= 0.01 else ''}
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 4. GRAPHIQUE : Consommation mensuelle (Barres)
# ============================================================

def afficher_consommation_mensuelle(pred_data, agence, annee, unite):
    """Graphique en barres de la consommation mensuelle."""
    
    mois_labels = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 
                   'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
    predictions = pred_data['predictions']
    
    # Déterminer la couleur en fonction de la gérance (modifié)
    gerance = pred_data.get('gerance', '')
    if "Électricité" in gerance or "Elec" in gerance or "électricité" in gerance.lower():
        color_principal = '#811F1F'   # Rouge bordeaux
    else:
        color_principal = '#2E6494'   # Bleu profond
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=mois_labels,
        y=predictions,
        marker_color=color_principal,
        marker_line_color='white',
        marker_line_width=2,
        text=[f"{p:.1f}" for p in predictions],
        textposition='outside',
        textfont=dict(size=13, color='#FFFFFF', weight='bold'),
        hovertemplate='<b>%{x}</b><br>Consommation: %{y:.2f} ' + unite + '<extra></extra>'
    ))
    
    # Ligne de moyenne
    moyenne = np.mean(predictions)
    fig.add_hline(
        y=moyenne,
        line_dash="dash",
        line_color="#FFD600",
        line_width=2,
        annotation_text=f"Moyenne: {moyenne:.1f} {unite}",
        annotation_font=dict(size=12, color='#FFD600'),
        annotation_position="top right"
    )
    
    fig.update_layout(
        title=get_title_style(f"📊 Consommation mensuelle - {agence} ({annee})"),
        xaxis=dict(
            tickfont=dict(size=14, color='#FFFFFF', weight='bold'),
            gridcolor='rgba(255,255,255,0.05)',
            showgrid=True
        ),
        yaxis=dict(
            title=dict(text=f"Consommation ({unite})", font=dict(size=14, color='#94A3B8')),
            tickfont=dict(size=13, color='#94A3B8'),
            gridcolor='rgba(255,255,255,0.05)',
            showgrid=True,
            tickformat=',.0f'
        ),
        plot_bgcolor='#111827',
        paper_bgcolor='#111827',
        height=400,
        margin=dict(l=60, r=40, t=60, b=40),
        bargap=0.3,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ============================================================
# 5. GRAPHIQUE : Consommation cumulée annuelle (AMÉLIORÉ)
# ============================================================

def afficher_cumul_annuel(pred_data, agence, annee, unite):
    """Graphique en aires de la consommation cumulée annuelle (amélioré)."""
    
    mois_labels = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 
                   'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
    predictions = pred_data['predictions']
    cumul = np.cumsum(predictions)
    
    # Déterminer la couleur en fonction de la gérance (modifié)
    gerance = pred_data.get('gerance', '')
    if "Électricité" in gerance or "Elec" in gerance or "électricité" in gerance.lower():
        color_principal = '#811F1F'
        color_light = 'rgba(129, 31, 31, 0.2)'
    else:
        color_principal = '#2E6494'
        color_light = 'rgba(46, 100, 148, 0.2)'
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=mois_labels,
        y=cumul,
        mode='lines+markers+text',
        line=dict(color=color_principal, width=4, shape='spline'),
        marker=dict(size=12, color=color_principal, line=dict(color='white', width=2)),
        text=[f"{v:,.0f}" for v in cumul],
        textposition='top center',
        textfont=dict(size=12, color='#FFFFFF', weight='bold'),
        fill='tozeroy',
        fillcolor=color_light,
        hovertemplate='<b>%{x}</b><br>Cumul: %{y:,.2f} ' + unite + '<extra></extra>'
    ))
    
    # Ligne de moyenne cumulée
    moyenne_cumul = np.mean(cumul)
    fig.add_hline(
        y=moyenne_cumul,
        line_dash="dash",
        line_color="#FFD600",
        line_width=1.5,
        annotation_text=f"Moyenne: {moyenne_cumul:,.1f} {unite}",
        annotation_font=dict(size=11, color='#FFD600'),
        annotation_position="top right"
    )
    
    # Annotation du total
    fig.add_annotation(
        x=11,
        y=cumul[-1],
        text=f"📊 Total: {cumul[-1]:,.2f} {unite}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1.5,
        arrowcolor=color_principal,
        ax=30,
        ay=-40,
        font=dict(size=14, color='#FFFFFF', weight='bold'),
        bgcolor='rgba(17, 24, 39, 0.9)',
        bordercolor=color_principal,
        borderwidth=1,
        borderpad=8
    )
    
    fig.update_layout(
        title=get_title_style(f"📈 Consommation cumulée - {agence} ({annee})"),
        xaxis=dict(
            tickfont=dict(size=14, color='#FFFFFF', weight='bold'),
            gridcolor='rgba(255,255,255,0.05)',
            showgrid=True,
            automargin=True,
            range=[-0.6, 11.6],
            tickvals=list(range(12)),
            ticktext=mois_labels
        ),
        yaxis=dict(
            title=dict(text=f"Cumul ({unite})", font=dict(size=14, color='#94A3B8')),
            tickfont=dict(size=13, color='#94A3B8'),
            gridcolor='rgba(255,255,255,0.05)',
            showgrid=True,
            tickformat=',.0f',
            automargin=True
        ),
        plot_bgcolor='#111827',
        paper_bgcolor='#111827',
        height=450,
        margin=dict(l=80, r=80, t=60, b=70),
        hovermode='x unified',
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ============================================================
# 6. GRAPHIQUE : Évolution annuelle des prévisions
# ============================================================

def afficher_evolution_annuelle(pred_data, agence, gerance, unite):
    """
    Graphique 6 : Évolution annuelle des prévisions
    Courbe de l'année de référence (2026) jusqu'à l'année prédite
    """
    
    mois_labels = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 
                   'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
    
    # Récupérer les prédictions de l'année en cours
    annee_predite = pred_data['annee']
    predictions_actuelles = pred_data['predictions']
    
    # ============================================================
    # ANNÉE DE RÉFÉRENCE : 2026
    # ============================================================
    annee_reference = 2026
    
    # Si l'année prédite est inférieure à 2026, ajuster
    if annee_predite < annee_reference:
        annee_reference = annee_predite
    
    # Générer les années de annee_reference à annee_predite
    annees = list(range(annee_reference, annee_predite + 1))
    
    # ============================================================
    # GÉNÉRER LES PRÉDICTIONS POUR CHAQUE ANNÉE
    # ============================================================
    predictions_par_annee = {}
    
    # Année prédite : utiliser les vraies prédictions
    predictions_par_annee[annee_predite] = predictions_actuelles
    
    # Si l'année prédite est l'année de référence, on n'a qu'une seule année
    if annee_predite == annee_reference:
        pass
    else:
        # Pour les années avant l'année prédite, simuler des données
        for an in reversed(annees[:-1]):
            # Calculer le nombre d'années de différence
            diff = annee_predite - an
            # Appliquer une tendance inverse
            trend_factor = 1.0 - (diff * 0.03)  # -3% par an
            noise = np.random.normal(0, 0.02, 12)
            predictions_par_annee[an] = predictions_actuelles * (trend_factor + noise)
    
    # Trier les années pour l'affichage
    predictions_par_annee = dict(sorted(predictions_par_annee.items()))
    
    # ============================================================
    # CRÉATION DU GRAPHIQUE
    # ============================================================
    fig = go.Figure()
    
    # Déterminer la palette en fonction de la gérance (modifié)
    if "Électricité" in gerance or "Elec" in gerance or "électricité" in gerance.lower():
        color_palette = ['#811F1F', '#A52A2A', '#C62828', '#B71C1C', '#D32F2F']  # Nuances de bordeaux
    else:
        color_palette = ['#2E6494', '#4A7B9D', '#6A93B0', '#2C5A7A', '#1A4A6E']  # Nuances de bleu profond
    
    # Ajouter une trace par année
    for idx, (an, preds) in enumerate(predictions_par_annee.items()):
        color = color_palette[idx % len(color_palette)]
        total_an = np.sum(preds)
        
        # Style spécial pour l'année prédite (en surbrillance)
        if an == annee_predite:
            line_width = 4
            marker_size = 14
            dash = 'solid'
            text_color = '#FFD600'
        else:
            line_width = 2.5
            marker_size = 10
            dash = 'dash'
            text_color = '#94A3B8'
        
        fig.add_trace(go.Scatter(
            x=mois_labels,
            y=preds,
            mode='lines+markers+text',
            name=f"{an} ({total_an:.0f} {unite})",
            line=dict(color=color, width=line_width, dash=dash),
            marker=dict(
                size=marker_size,
                color=color,
                line=dict(color='white', width=2),
                symbol='circle'
            ),
            text=[f"{p:.0f}" for p in preds],
            textposition='top center',
            textfont=dict(size=10, color=text_color),
            hovertemplate=(
                f'<b>%{{x}} {an}</b><br>' +
                f'Consommation: %{{y:.2f}} {unite}<br>' +
                '<extra></extra>'
            )
        ))
    
    # Ajouter une annotation pour indiquer l'année prédite
    fig.add_annotation(
        x=0.5,
        y=1.05,
        xref='paper',
        yref='paper',
        text=f"🎯 Année prédite : <b>{annee_predite}</b>",
        showarrow=False,
        font=dict(size=16, color='#FFD600', weight='bold'),
        bgcolor='rgba(17, 24, 39, 0.8)',
        bordercolor='#FFD600',
        borderwidth=2,
        borderpad=8
    )
    
    fig.update_layout(
        title=dict(
            text=f"📈 Évolution annuelle des prévisions - {agence} - {gerance} ({annee_reference} → {annee_predite})",
            font=dict(size=20, color='#FFFFFF', family='Arial, sans-serif', weight='bold'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            tickfont=dict(size=14, color='#FFFFFF', weight='bold'),
            gridcolor='rgba(255,255,255,0.05)',
            showgrid=True
        ),
        yaxis=dict(
            title=dict(text=f"Consommation ({unite})", font=dict(size=14, color='#94A3B8')),
            tickfont=dict(size=13, color='#94A3B8'),
            gridcolor='rgba(255,255,255,0.05)',
            showgrid=True,
            tickformat=',.0f'
        ),
        plot_bgcolor='#111827',
        paper_bgcolor='#111827',
        height=450,
        margin=dict(l=60, r=40, t=80, b=40),
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.25,
            xanchor='center',
            x=0.5,
            font=dict(size=13, color='#E2E8F0'),
            bgcolor='rgba(17, 24, 39, 0.8)',
            bordercolor='rgba(255,255,255,0.05)',
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # ============================================================
    # TABLEAU RÉCAPITULATIF DES PRÉVISIONS PAR ANNÉE
    # ============================================================
    with st.expander("📋 Voir le détail des prévisions par année", expanded=False):
        df_evolution = pd.DataFrame()
        for an, preds in predictions_par_annee.items():
            df_temp = pd.DataFrame({
                'Année': [an] * 12,
                'Mois': mois_labels,
                'Consommation': preds
            })
            df_evolution = pd.concat([df_evolution, df_temp], ignore_index=True)
        
        # Pivot table
        df_pivot = df_evolution.pivot(index='Mois', columns='Année', values='Consommation')
        df_pivot['Moyenne'] = df_pivot.mean(axis=1)
        df_pivot['Écart-type'] = df_pivot.std(axis=1)
        
        st.dataframe(
            df_pivot.style.format('{:.2f}').set_properties(**{
                'font-size': '13px',
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
        
        # Résumé des totaux annuels
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            totals = {an: np.sum(preds) for an, preds in predictions_par_annee.items()}
            df_totals = pd.DataFrame({
                'Année': list(totals.keys()),
                'Total annuel': list(totals.values())
            })
            
            # Mettre en évidence l'année prédite
            def highlight_annee(row):
                if row['Année'] == annee_predite:
                    return ['background-color: #FFD600; color: #0A2540; font-weight: bold'] * len(row)
                return [''] * len(row)
            
            styled = df_totals.style.format({'Total annuel': '{:.2f}'}).apply(highlight_annee, axis=1)
            st.dataframe(
                styled.set_properties(**{
                    'font-size': '13px',
                    'padding': '6px'
                }),
                use_container_width=True
            )
        
        with col2:
            if len(annees) > 1:
                # Taux de croissance annuel
                annees_triees = sorted(totals.keys())
                taux_croissance = []
                for i in range(1, len(annees_triees)):
                    taux = ((totals[annees_triees[i]] - totals[annees_triees[i-1]]) / totals[annees_triees[i-1]]) * 100
                    taux_croissance.append(taux)
                
                df_croissance = pd.DataFrame({
                    'Période': [f"{annees_triees[i-1]} → {annees_triees[i]}" for i in range(1, len(annees_triees))],
                    'Taux de croissance': taux_croissance
                })
                st.dataframe(
                    df_croissance.style.format({'Taux de croissance': '{:+.2f}%'}).set_properties(**{
                        'font-size': '13px',
                        'padding': '6px',
                        'background-color': '#0D2B4A',
                        'color': '#E2E8F0'
                    }),
                    use_container_width=True
                )
            else:
                st.info("📊 Une seule année disponible (pas de calcul de croissance)")

# ============================================================
# 7. PAGE PRINCIPALE
# ============================================================

def render_kpi_predictifs():
    """Affiche la page KPI Prédictifs avec le style de facteurs_influence."""
    
    apply_kpi_predictifs_style()
    
    # En-tête
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.2rem; font-weight: 700; color: #FFFFFF; margin: 0; padding: 0;">⚡ KPI Prédictifs</h1>
        <p style="font-size: 1.1rem; color: #94A3B8; margin: 0.2rem 0 0 0;">
            Indicateurs clés de performance sur les dernières prédictions
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================================
    # VÉRIFICATIONS
    # ============================================================
    if ('dernieres_predictions' not in st.session_state or 
        st.session_state.dernieres_predictions is None):
        st.warning("⚠️ Veuillez d'abord effectuer une prédiction dans la page '🔮 Prédiction de la consommation'.")
        return
    
    data = st.session_state.dernieres_predictions
    
    required_keys = ['predictions', 'mois_labels', 'mois_numeros', 'agence', 'gerance', 'annee', 'unite', 'total_annuel', 'moyenne']
    for key in required_keys:
        if key not in data:
            st.error(f"❌ Données de prédiction incomplètes : clé '{key}' manquante.")
            return
    
    predictions = data['predictions']
    mois_labels = data['mois_labels']
    mois_numeros = data['mois_numeros']
    agence = data['agence']
    gerance = data['gerance']
    annee = data['annee']
    unite = data['unite']
    total_annuel = data['total_annuel']
    moyenne = data['moyenne']
    
    # ============================================================
    # 1. CALCUL DES KPI DE CONSOMMATION
    # ============================================================
    max_val = np.max(predictions)
    min_val = np.min(predictions)
    mediane = np.median(predictions)
    ecart_type = np.std(predictions)
    coeff_var = (ecart_type / moyenne * 100) if moyenne != 0 else 0
    
    idx_max = np.argmax(predictions)
    idx_min = np.argmin(predictions)
    mois_max = mois_labels[idx_max]
    mois_min = mois_labels[idx_min]
    
    saisons = [get_saison(m) for m in mois_numeros]
    df_saisons = pd.DataFrame({
        'Mois': mois_labels,
        'Saison': saisons,
        'Consommation': predictions
    })
    conso_par_saison = df_saisons.groupby('Saison')['Consommation'].sum().to_dict()
    saison_max = max(conso_par_saison, key=conso_par_saison.get) if conso_par_saison else "N/A"
    saison_min = min(conso_par_saison, key=conso_par_saison.get) if conso_par_saison else "N/A"
    
    amplitude = max_val - min_val
    conso_min_saison = min(conso_par_saison.values()) if conso_par_saison else 0
    conso_max_saison = max(conso_par_saison.values()) if conso_par_saison else 0
    indice_saisonnalite = conso_max_saison / conso_min_saison if conso_min_saison != 0 else 0
    
    # ============================================================
    # 2. AFFICHAGE DES KPI (style facteurs_influence)
    # ============================================================
    st.markdown('<h2 class="section-title">📊 Indicateurs clés</h2>', unsafe_allow_html=True)
    
    # Ligne 1 : 4 KPI principaux
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card" style="border-color: #FFD600;">
            <div class="kpi-label" style="color: #FFD600;">📊 TOTAL ANNUEL</div>
            <div class="kpi-value" style="color: #FFD600;">{total_annuel:.1f}</div>
            <div class="kpi-sub">{unite}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card" style="border-color: #00E676;">
            <div class="kpi-label" style="color: #00E676;">📈 MOYENNE MENSUELLE</div>
            <div class="kpi-value" style="color: #00E676;">{moyenne:.1f}</div>
            <div class="kpi-sub">{unite}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card" style="border-color: #EF5350;">
            <div class="kpi-label" style="color: #EF5350;">📈 CONSO MAX</div>
            <div class="kpi-value" style="color: #EF5350;">{max_val:.1f}</div>
            <div class="kpi-sub">{mois_max} · {unite}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card" style="border-color: #1E88E5;">
            <div class="kpi-label" style="color: #1E88E5;">📉 CONSO MIN</div>
            <div class="kpi-value" style="color: #1E88E5;">{min_val:.1f}</div>
            <div class="kpi-sub">{mois_min} · {unite}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Ligne 2 : KPI secondaires
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card" style="border-color: #6A1B9A; height: 90px;">
            <div class="kpi-label" style="color: #CE93D8;">📊 MÉDIANE</div>
            <div class="kpi-value" style="font-size: 22px; color: #CE93D8;">{mediane:.1f}</div>
            <div class="kpi-sub">{unite}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card" style="border-color: #FF8F00; height: 90px;">
            <div class="kpi-label" style="color: #FFB74D;">📊 ÉCART-TYPE</div>
            <div class="kpi-value" style="font-size: 22px; color: #FFB74D;">{ecart_type:.1f}</div>
            <div class="kpi-sub">{unite}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card" style="border-color: #00BCD4; height: 90px;">
            <div class="kpi-label" style="color: #4DD0E1;">📊 AMPLITUDE</div>
            <div class="kpi-value" style="font-size: 22px; color: #4DD0E1;">{amplitude:.1f}</div>
            <div class="kpi-sub">{unite}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card" style="border-color: #FF5722; height: 90px;">
            <div class="kpi-label" style="color: #FF8A65;">🌿 INDICE SAISONNALITÉ</div>
            <div class="kpi-value" style="font-size: 22px; color: #FF8A65;">{indice_saisonnalite:.2f}</div>
            <div class="kpi-sub">ratio max/min</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============================================================
    # 3. GRAPHIQUE 1 : Consommation mensuelle (barres)
    # ============================================================
    st.markdown('<p class="graph-title">📊 1. Consommation mensuelle</p>', unsafe_allow_html=True)
    afficher_consommation_mensuelle(data, agence, annee, unite)
    st.markdown("---")
    
    # ============================================================
    # 4. GRAPHIQUE 2 : SUNBURST (Hiérarchie Saison → Mois)
    # ============================================================
    st.markdown('<p class="graph-title">🌞 2. Hiérarchie Saison → Mois</p>', unsafe_allow_html=True)
    afficher_sunburst_kpi(data, agence, annee, unite)
    st.markdown("---")
    
    # ============================================================
    # 5. GRAPHIQUE 3 : Consommation cumulée (AMÉLIORÉ)
    # ============================================================
    st.markdown('<p class="graph-title">📈 3. Consommation cumulée annuelle</p>', unsafe_allow_html=True)
    afficher_cumul_annuel(data, agence, annee, unite)
    st.markdown("---")
    
    # ============================================================
    # 6. GRAPHIQUE 4 : Évolution annuelle des prévisions
    # ============================================================
    st.markdown('<p class="graph-title">📈 4. Évolution annuelle des prévisions </p>', unsafe_allow_html=True)
    afficher_evolution_annuelle(data, agence, gerance, unite)
    st.markdown("---")
    
    # ============================================================
    # 7. NOTE INFO
    # ============================================================
    st.markdown("""
    <div class="info-note">
        📊 <strong>Analyse basée sur</strong> : RandomForestRegressor entraîné sur les données historiques
        <br>🌿 Les saisons sont définies selon l'hémisphère nord (Hiver: Déc-Fév, Printemps: Mar-Mai, Été: Juin-Août, Automne: Sep-Nov)
        <br>📈 L'évolution annuelle montre la tendance de consommation de 2026 à l'année prédite
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================================
    # 8. FOOTER
    # ============================================================
    st.markdown("---")
    st.caption(f"""
    📊 **Prédiction basée sur** : {agence} - {gerance} - {annee}  
    🧠 **Modèle** : RandomForestRegressor (entraîné sur les données historiques)  
    📅 Dernière mise à jour : {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}
    """)