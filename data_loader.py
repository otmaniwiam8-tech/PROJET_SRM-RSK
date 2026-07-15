# data_loader.py
import pandas as pd
import streamlit as st

def load_multiple_files(uploaded_files):
    """Charge et concatène plusieurs fichiers"""
    if not uploaded_files:
        return None
    
    dfs = []
    file_names = []
    
    for file in uploaded_files:
        if file.name.endswith('.csv'):
            df_temp = pd.read_csv(file)
        else:
            df_temp = pd.read_excel(file)
        dfs.append(df_temp)
        file_names.append(file.name)
    
    if len(dfs) == 1:
        df = dfs[0]
    else:
        cols = [set(d.columns) for d in dfs]
        if all(c == cols[0] for c in cols):
            df = pd.concat(dfs, ignore_index=True)
        else:
            st.error("❌ Les fichiers n'ont pas les mêmes colonnes")
            return None
    
    return df, file_names

def find_column(df, possible_names):
    """Trouve une colonne dans le DataFrame"""
    for col in possible_names:
        if col in df.columns:
            return col
    return None