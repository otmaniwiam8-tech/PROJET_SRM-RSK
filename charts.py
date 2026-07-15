# charts.py
import plotly.graph_objects as go
import streamlit as st
from config import COLORS

def create_bar_chart(df, x_col, y_col, title, color, xlabel, ylabel, suffix="", orientation='v'):
    """
    Crée un graphique à barres
    orientation: 'v' pour vertical, 'h' pour horizontal
    """
    fig = go.Figure()
    
    text_suffix = suffix if suffix else ""
    
    if orientation == 'h':
        fig.add_trace(go.Bar(
            x=df[y_col],
            y=df[x_col],
            orientation='h',
            marker_color=color,
            marker_line_color='white',
            marker_line_width=2,
            text=df[y_col].apply(lambda x: f"{x:,.0f} {text_suffix}"),
            textposition='outside',
            textfont=dict(size=13, color='#0A2540', family='Arial, sans-serif', weight='bold'),
            hovertemplate='<b>%{y}</b><br>Valeur: %{text}<extra></extra>'
        ))
    else:
        fig.add_trace(go.Bar(
            x=df[x_col],
            y=df[y_col],
            marker_color=color,
            marker_line_color='white',
            marker_line_width=2,
            text=df[y_col].apply(lambda x: f"{x:,.0f} {text_suffix}"),
            textposition='outside',
            textfont=dict(size=13, color='#0A2540', family='Arial, sans-serif', weight='bold'),
            hovertemplate='<b>%{x}</b><br>Valeur: %{text}<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=22, color='#0A2540', family='Arial, sans-serif', weight='bold'), x=0.5, xanchor='center'),
        xaxis=dict(
            title=dict(text=xlabel, font=dict(size=16, color='#0A2540', family='Arial, sans-serif')),
            tickfont=dict(size=14, color='#0A2540', family='Arial, sans-serif'),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(text=ylabel, font=dict(size=16, color='#0A2540', family='Arial, sans-serif')),
            tickfont=dict(size=13, color='#0A2540', family='Arial, sans-serif'),
            gridcolor='#E8ECEF',
            gridwidth=0.5,
            showgrid=True,
            tickformat=',.0f'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=450,
        margin=dict(l=60, r=60, t=60, b=60),
        bargap=0.3,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def create_line_chart(df, x_col, y_col, title, color, xlabel, ylabel, suffix=""):
    """Crée un graphique en ligne"""
    text_suffix = suffix if suffix else ""
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='lines+markers+text',
        line=dict(color=color, width=4),
        marker=dict(size=16, color=color, line=dict(color='white', width=3)),
        text=df[y_col].apply(lambda x: f"{x:,.0f} {text_suffix}"),
        textposition='top center',
        textfont=dict(size=13, color='#0A2540', family='Arial, sans-serif', weight='bold'),
        hovertemplate='<b>%{x}</b><br>Valeur: %{text}<extra></extra>'
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(size=22, color='#0A2540', family='Arial, sans-serif', weight='bold'), x=0.5, xanchor='center'),
        xaxis=dict(
            title=dict(text=xlabel, font=dict(size=16, color='#0A2540', family='Arial, sans-serif')),
            tickfont=dict(size=14, color='#0A2540', family='Arial, sans-serif'),
            gridcolor='#E8ECEF',
            gridwidth=0.5,
            showgrid=True
        ),
        yaxis=dict(
            title=dict(text=ylabel, font=dict(size=16, color='#0A2540', family='Arial, sans-serif')),
            tickfont=dict(size=13, color='#0A2540', family='Arial, sans-serif'),
            gridcolor='#E8ECEF',
            gridwidth=0.5,
            showgrid=True,
            tickformat=',.0f'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=450,
        margin=dict(l=60, r=60, t=60, b=60),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})