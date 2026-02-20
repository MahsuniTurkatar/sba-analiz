import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
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

# --- CSS: FB TASARIMI VE HİZALAMA ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Metrik Kutuları: Ortalı ve Dar */
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; color: white !important; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
        width: 220px !important; margin: auto !important;
    }
    
    /* Tablo Düzeni */
    .table-container { display: flex; justify-content: center; margin: 20px 0; }
    .styled-table { width: auto !important; border-collapse: collapse; color: white; font-size: 0.9rem; }
    .styled-table th { background-color: #001d3d; color: #FEDD00; border: 1px solid #FEDD00; padding: 10px 15px; text-align: center; }
    .styled-table td { border: 1px solid #FEDD00; padding: 6px 15px; text-align: center; }
    
    /* Sola Dayalı Sütunlar (Birim ve Sorumlu için) */
    .left-align { text-align: left !important; padding-left: 20px !important; }
    
    /* Toplam Satırı: Lacivert-Sarı */
    .total-row td { background-color: #FEDD00 !important; color: #001d3d !important; font-weight: bold !important; }
    
    h1, h2, h3, h4 { color: #FEDD00 !important; text-align: center !important; }
    .stTabs [data-baseweb="tab"] { color: #FEDD00 !important; }
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.write("# Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları")

# --- 1. ÜST METRİKLER (ORTALANMIŞ) ---
col_m1, col_m2, col_m3, col_m4 = st.columns([2, 1, 1, 2])
with col_m2: st.metric("📌 Toplam Başvuru", "190")
with col_m3: st.metric("🗓️ Kurul Sayısı", "4")

# --- 2. GÜNDEM SAYILARI (ORTALANMIŞ) ---
if df_gundem is not None:
    st.write("### 📅 2026 Gündem Sayıları")
    df_g_final = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    df_g_final['Gündem Tarihleri'] = pd.to_datetime(df_g_final['Gündem Tarihleri'], errors='coerce').dt.strftime('%d.%m.%Y')
    st.markdown('<div class="table-container">' + df_g_final.to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Araştırmacı Analizi"])

with tab1:
    st.write("### 📊 Genel Karar Dağılım Çizelgesi")
    if df_raportor is not None:
        try:
            # Excel'in en altındaki TOPLAM satırı
            total_data = df_raportor[df_raportor.iloc[:,
