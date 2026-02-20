import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx" 

@st.cache_data
def load_all_data():
    try:
        # Gündem Sayıları
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        return df_g
    except:
        return None

df_gundem = load_all_data()

# --- CSS: BEYAZ BAŞLIKLAR, ORTALI METRİKLER VE İĞNELENMİŞ TABLOLAR ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* BAŞLIKLAR: BEYAZ VE ORTALI */
    h1, h2, h3, h4 { 
        color: #ffffff !important; 
        text-align: center !important; 
        font-weight: bold !important;
    }
    
    /* METRİKLER: FB DÜZENİNDE AMA YENİ SAYILARLA ORTADA */
    [data-testid="stHorizontalBlock"] { justify-content: center !important; gap: 20px !important; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
        width: fit-content !important; min-width: 200px; padding: 10px;
    }
    [data-testid="stMetricValue"] { color: #FEDD00 !important; font-size: 2.2rem !important; }
    [data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 1.1rem !important; }

    /* NİTELİK KARTLARI (YENİ SAYILAR) */
    .nitelik-container { display: flex; justify-content: center; gap: 15px; margin: 25px 0; }
    .nitelik-card {
        background-color: #001d3d; border: 1px solid #FEDD00;
        border-radius: 10px; padding: 15px; text-align: center; min-width: 160px;
    }
    .n-val { color: #FEDD00; font-size: 1.6rem; font-weight: bold; display: block; }
    .n-lab { color: #ffffff; font-size: 0.9rem; }

    /* TABLOLAR: ORTALI VE SÜTUNLAR İÇERİĞİ KADAR (TABLE-LAYOUT: AUTO) */
    .table-container { display: flex; justify-content: center; margin: 20px 0; width: 100%; }
    .styled-table { 
        width: auto !important; /* İĞNELENDİ: Sadece içerik kadar */
        margin: auto; border-collapse: collapse; color: white; font-size: 0.9rem; 
        table-layout: auto !important; 
    }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 12px 20px; text-align: center !important; white-space: nowrap; }
    .styled-table td { border: 1px solid #FEDD00; padding: 10px 18px; text-align: center !important; white-space: nowrap; }
    
    /* TOPLAM SATIRI VURGUSU */
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; border-top: 2px solid #FEDD00 !important; }
    </style>
    """, unsafe_allow_html=True)

# GÖRSEL TEMİZLİK (0'ları siler)
def clean_df(df):
    return df.applymap(lambda x: "" if (pd.isna(x) or str(x).strip() in ["0", "0.0", "0.00"]) else (int(x) if isinstance(x, (int, float)) else x))

st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. ÜST METRİKLER (GÜNCEL: 206 - 5) ---
m_col1, m_col2 = st.columns(2)
with m_col1: st.metric("📌 Toplam Başvuru", "206")
with m_col2: st.metric("🗓️ Kurul Sayısı", "5")

# --- 2. NİTELİK KARTLARI (GÜNCEL SAYILAR) ---
st.markdown("""
    <div class="nitelik-container">
        <div class="nitelik-card"><span class="n-val">135</span><span class="n-lab">Bireysel Araştırma</span></div>
        <div class="nitelik-card"><span class="n-val">41</span><span class="n-lab">Uzmanlık Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">12</span><span class="n-lab">Y. Lisans Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">18</span><span class="n-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# --- 3. GÜNDEM SAYILARI (TOPLAM SATIRI EKLENDİ) ---
if df_gundem is not None:
    st.markdown("<h3>📅 2026 Gündem Sayıları</h3>", unsafe_allow_html=True)
    # Temizleme ve Tarih Formatı
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    dg = dg[dg['Toplam'] > 0]
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    
    # En alta Toplam Satırı Ekleme (206 Başvuru / 319 Genel Toplam)
    t_row = pd.DataFrame([{
        "S.NO": "TOPLAM", 
        "Gündem Tarihleri": "", 
        "Başvuru": 206, 
        "Düzeltme": 68, 
        "Dilekçe": 45, 
        "Toplam": 319
    }])
    dg_final = pd.concat([dg, t_row], ignore_index=True)
    
    # Tabloyu Bas (Ortalı ve İçerik Kadar Geniş)
    html_g = clean_df(dg_final).to_html(index=False, classes='styled-table')
    html_g = html_g.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
    st.markdown(f'<div class="table-container">{html_g}</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:#FEDD00; padding:20px; font-weight:bold; border-top:1px solid #FEDD00; margin-top:30px;">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
