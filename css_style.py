# css_style.py
import streamlit as st

def load_css():
    """Charge le CSS personnalisé"""
    st.markdown("""
<style>
    .main {
        background-color: #F4F6F8;
    }
    
    .header {
        background: linear-gradient(135deg, #0A2540 0%, #1A3A5C 100%);
        padding: 1.2rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 12px rgba(10, 37, 64, 0.15);
    }
    .header-left {
        display: flex;
        align-items: center;
        gap: 1.2rem;
    }
    .header-logo {
        background-color: #1E88E5;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        color: white;
        font-weight: 800;
        font-size: 1.3rem;
        letter-spacing: 1px;
    }
    .header-title {
        color: white;
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    .header-subtitle {
        color: #B0C4DE;
        font-size: 0.95rem;
        margin: 0;
        font-weight: 300;
    }
    .header-right {
        color: #B0C4DE;
        font-size: 0.85rem;
        text-align: right;
        border-left: 1px solid rgba(255,255,255,0.15);
        padding-left: 1.5rem;
    }
    .header-right strong {
        color: white;
        font-weight: 600;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #0A2540;
        padding-top: 1rem;
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    .sidebar-title {
        color: white !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #1E88E5 !important;
    }
    .sidebar-success {
        background-color: #00A86B !important;
        color: white !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    .sidebar-error {
        background-color: #D32F2F !important;
        color: white !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    .sidebar-info {
        color: #B0C4DE !important;
        font-size: 0.9rem !important;
        padding: 0.5rem !important;
        background-color: #1A3A5C !important;
        border-radius: 8px !important;
        text-align: center !important;
    }
    
    section[data-testid="stSidebar"] .stFileUploader {
        width: 100%;
    }
    section[data-testid="stSidebar"] .stFileUploader > div {
        background-color: rgba(255,255,255,0.04) !important;
        border-radius: 12px !important;
        border: 2px dashed rgba(255,255,255,0.12) !important;
        padding: 1.5rem 0.5rem !important;
        transition: all 0.3s ease !important;
        text-align: center !important;
    }
    section[data-testid="stSidebar"] .stFileUploader > div:hover {
        border-color: #1E88E5 !important;
        background-color: rgba(30,136,229,0.05) !important;
    }
    section[data-testid="stSidebar"] .stFileUploader button {
        background: linear-gradient(135deg, #1E88E5, #1565C0) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(30,136,229,0.3) !important;
    }
    section[data-testid="stSidebar"] .stFileUploader button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(30,136,229,0.4) !important;
    }
    section[data-testid="stSidebar"] .stFileUploader .stFileUploaderLabel {
        display: none !important;
    }
    
    .card {
        border: 2px solid #1E88E5;
        border-radius: 12px;
        padding: 1.5rem 1.8rem;
        background: linear-gradient(135deg, #E8F0FE 0%, #D6E4F8 100%);
        box-shadow: 0 2px 8px rgba(30, 136, 229, 0.08);
        height: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(30, 136, 229, 0.12);
    }
    .card h3 {
        color: #0D47A1 !important;
        margin-top: 0;
        margin-bottom: 0.8rem;
        font-size: 1.3rem;
        font-weight: 700;
    }
    .card p, .card li {
        color: #1A237E;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 0.3rem;
    }
    .card ul {
        list-style-type: none;
        padding-left: 0;
        margin-bottom: 0;
    }
    .card ul li {
        padding: 0.2rem 0;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #0A2540 0%, #1A3A5C 100%) !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        box-shadow: 0 4px 12px rgba(10, 37, 64, 0.15) !important;
        border-left: 4px solid #1E88E5 !important;
    }
    .stMetric .stMetricValue {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
    }
    .stMetric .stMetricLabel {
        color: #B0C4DE !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }
    
    h1, .stTitle {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        letter-spacing: -0.5px !important;
        background: linear-gradient(135deg, #0A2540 0%, #1A3A5C 100%);
        padding: 0.8rem 1.5rem;
        border-radius: 12px;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(10, 37, 64, 0.1);
        margin-bottom: 0.5rem;
    }
    h2, .stSubheader {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(21, 101, 192, 0.2);
        margin-bottom: 0.5rem;
    }
    h3 {
        color: #0D47A1 !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
    }
    
    .stAlert {
        border-radius: 10px !important;
        border-left: 4px solid !important;
    }
    .stAlert .stMarkdown {
        color: #0A2540 !important;
    }
    
    .footer {
        margin-top: 3rem;
        text-align: center;
        color: #5A6C7D;
        font-size: 0.8rem;
        border-top: 1px solid #E0E6ED;
        padding-top: 1.5rem;
        padding-bottom: 0.5rem;
    }
    .footer strong {
        color: #0A2540;
    }
    
    .divider {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #1E88E5, transparent);
        margin: 1.5rem 0;
        opacity: 0.4;
    }
    
    .section-divider {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, #1E88E5, #00A86B, #1E88E5);
        margin: 2rem 0;
        border-radius: 5px;
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
    
    .stButton button {
        background: linear-gradient(135deg, #1E88E5, #1565C0) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(30,136,229,0.3) !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 32px rgba(30,136,229,0.4) !important;
    }
    
    .stDownloadButton button {
        background: linear-gradient(135deg, #00A86B, #00897B) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(0,168,107,0.3) !important;
    }
    .stDownloadButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 32px rgba(0,168,107,0.4) !important;
    }
    
    .info-banner {
        background: linear-gradient(135deg, #E8F0FE, #D6E4F8);
        border-radius: 12px;
        padding: 1rem 1.8rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #1E88E5;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        box-shadow: 0 2px 12px rgba(30,136,229,0.06);
    }
    .info-banner strong {
        color: #0A2540;
        font-weight: 700;
    }
    .info-banner span {
        color: #1A237E;
    }
    .info-banner .date {
        color: #1A237E;
        font-size: 0.85rem;
        opacity: 0.7;
    }
    
    .col-list {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        padding: 0.5rem 0;
    }
    .col-tag {
        background: linear-gradient(135deg, #E8F0FE, #D6E4F8);
        padding: 0.4rem 1rem;
        border-radius: 24px;
        font-size: 0.85rem;
        color: #0A2540;
        font-weight: 500;
        border: 1px solid rgba(30,136,229,0.15);
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .col-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(30,136,229,0.1);
        border-color: #1E88E5;
    }
    
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #E8F0FE, #D6E4F8) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        color: #0A2540 !important;
        border: 1px solid rgba(30,136,229,0.08) !important;
        padding: 0.8rem 1.2rem !important;
    }
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #D6E4F8, #C4D6F0) !important;
        border-color: rgba(30,136,229,0.15) !important;
    }
    
    .stRadio label {
        color: #B0C4DE !important;
        font-weight: 500 !important;
        padding: 0.5rem 0.8rem !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    .stRadio label:hover {
        background-color: rgba(255,255,255,0.05) !important;
    }
    .stRadio [data-testid="stMarkdownContainer"] {
        color: white !important;
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
        background: linear-gradient(135deg, #0A2540 0%, #1A3A5C 100%) !important;
        border-radius: 10px !important;
        display: inline-block !important;
        box-shadow: 0 4px 12px rgba(10, 37, 64, 0.15) !important;
    }
    .section-title-facturation {
        color: #FFFFFF !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        margin: 1.5rem 0 1rem 0 !important;
        padding: 0.5rem 1.2rem !important;
        background: linear-gradient(135deg, #0A2540 0%, #1A3A5C 100%) !important;
        border-radius: 10px !important;
        display: inline-block !important;
        box-shadow: 0 4px 12px rgba(10, 37, 64, 0.15) !important;
    }
</style>
""", unsafe_allow_html=True)