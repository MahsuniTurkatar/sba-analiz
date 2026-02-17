import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması (SABİT)
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx"  # Dosya adı istediğin gibi sabitlendi ✊

@st.cache_data
def load_all_data():
    try:
        # Sayılar sekmesi
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        # Raportör Analizi (Üye_1)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1", skiprows=1)
        # Pivot Analizleri
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot", skiprows=2)
        return df_g, df_r, df_p
    except:
        return None, None, None

df_gundem, df_raportor, df_pivot = load_all_data()

# --- CSS: FB TASARIMI (ASLA DOKUNULMADI) ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
    }
    .nitelik-container { display: flex; justify-content: space-between; gap: 10px; margin: 20px 0; }
    .nitelik-card {
        flex: 1; background-color: #001d3d; border: 1px solid #FEDD00;
        border-radius: 8px; padding: 15px; text-align: center;
    }
    .n-val { color: #FEDD00; font-size: 1.5rem; font-weight: bold; display: block; }
    .n-lab { color: #ffffff; font-size: 0.9rem; }
    .table-container { display: flex; justify-content: center; margin: 20px 0; }
    .styled-table { width: 100% !important; border-collapse: collapse; color: white; }
    .styled-table th { background-color: #001d3d; color: #FEDD00; border: 1px solid #FEDD00; padding: 10px; text-align: center; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px; text-align: center; }
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #FEDD00 !important; }
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. ÜST METRİKLER (SABİT) ---
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# --- 2. NİTELİK KARTLARI (SABİT) ---
st.markdown("""
    <div class="nitelik-container">
        <div class="nitelik-card"><span class="n-val">128</span><span class="n-lab">Bireysel Araştırma</span></div>
        <div class="nitelik-card"><span class="n-val">48</span><span class="n-lab">Uzmanlık Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">10</span><span class="n-lab">Y. Lisans Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">4</span><span class="n-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# --- 3. GÜNDEM SAYILARI (DİNAMİK & 5. KURUL UYUMLU) ---
if df_gundem is not None:
    df_g_work = df_gundem.copy()
    
    # Tarih formatı GG.AA.YYYY
    df_g_work['Gündem Tarihleri'] = pd.to_datetime(df_g_work['Gündem Tarihleri'], errors='coerce').dt.strftime('%d.%m.%Y')
    
    # Sayıları tam sayıya çevirme (45.0 -> 45)
    for col in ['Başvuru', 'Düzeltme', 'Dilekçe', 'Toplam']:
        if col in df_g_work.columns:
            df_g_work[col] = pd.to_numeric(df_g_work[col], errors='coerce').fillna(0).astype(int)
    
    # Süzgeç: S.No olanları ve verisi olanları getir (Dinamik kurul ekleme)
    df_g_final = df_g_work[
        (df_g_work['S.NO'].notna()) & 
        ((df_g_work['Toplam'] > 0) | (df_g_work['S.NO'].astype(str).str.contains("TOPLAM", case=False)))
    ]
    
    st
