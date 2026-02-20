import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması (SABİT)
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx" 

@st.cache_data
def load_all_data():
    try:
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1", skiprows=1)
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot", skiprows=1)
        return df_g, df_r, df_p
    except:
        return None, None, None

df_gundem, df_raportor, df_pivot = load_all_data()

# --- CSS: FB TASARIMI VE DARALTMA AYARLARI ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Metrik kutularını daraltma */
    [data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
        width: fit-content !important; min-width: 150px !important; margin: auto !important;
    }
    
    .table-container { display: flex; justify-content: center; margin: 10px 0; overflow-x: auto; }
    .styled-table { width: auto !important; border-collapse: collapse; color: white; margin-bottom: 10px; font-size: 0.85rem; }
    .styled-table th { background-color: #001d3d; color: #FEDD00; border: 1px solid #FEDD00; padding: 8px 12px; text-align: center; }
    .styled-table td { border: 1px solid #FEDD00; padding: 5px 10px; text-align: center; }
    
    /* Raportör TOPLAM: Lacivert Arka Plan, Sarı Yazı */
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; border: 2px solid #FEDD00 !important; }
    
    /* Birim/Sorumlu Alt Toplam Satırı */
    .sub-total td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; }

    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #FEDD00 !important; }
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. METRİKLER (DARALTILMIŞ) ---
col_m1, col_m2 = st.columns(2)
with col_m1: st.metric("📌 Toplam Başvuru", "190")
with col_m2: st.metric("🗓️ Kurul Sayısı", "4")

# --- 2. GÜNDEM SAYILARI (HER SAYFADA ÜSTTE OLSUN DİYE SEKMELERİN DIŞINDA) ---
if df_gundem is not None:
    df_g_final = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    df_g_final['Gündem Tarihleri'] = pd.to_datetime(df_g_final['Gündem Tarihleri'], errors='coerce').dt.strftime('%d.%m.%Y')
    for col in ['Başvuru', 'Düzeltme', 'Dilekçe', 'Toplam']:
        if col in df_g_final.columns:
            df_g_final[col] = pd.to_numeric(df_g_final[col], errors='coerce').fillna(0).astype(int)
    st.write("### 📅 2026 Gündem Sayıları")
    st.markdown('<div class="table-container">' + df_g_final.to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Araştırmacı Analizi"])

with tab1:
    st.write("### 📊 Genel Karar Dağılım Çizelgesi")
    if df_raportor is not None:
        # Excel'deki GENEL TOPLAM satırını (genellikle en altta) bulalım
        genel_toplam_row = df_raportor[df_raportor.iloc[:, 1].astype(str).str.contains("GENEL TOPLAM|TOPLAM", na=False)].iloc[0]
        
        def
