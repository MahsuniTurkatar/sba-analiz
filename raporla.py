import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx" 

@st.cache_data
def load_top_data():
    try:
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        return df_g
    except:
        return None

df_gundem = load_top_data()

# --- CSS: KUTU DÜZENİ VE BEYAZ BAŞLIKLAR ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* BEYAZ VE ORTALI BAŞLIKLAR */
    h1, h2, h3 { 
        color: #ffffff !important; 
        text-align: center !important; 
        font-weight: bold !important;
        margin-bottom: 20px !important;
    }

    /* METRİK KUTULARI (GÜNCELLENMİŞ ARALIKLI DÜZEN) */
    [data-testid="stHorizontalBlock"] {
        justify-content: center !important;
        gap: 50px !important; /* Kutular arası boşluk */
    }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; 
        border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; 
        padding: 15px 30px !important;
        text-align: center !important;
    }
    [data-testid="stMetricValue"] { 
        color: #FEDD00 !important; 
        font-size: 2.8rem !important; 
        font-weight: bold !important;
    }
    [data-testid="stMetricLabel"] { 
        color: #ffffff !important; 
        font-size: 1.1rem !important;
    }

    /* NİTELİK KARTLARI (METRİKLERİN ALTINDA) */
    .nitelik-row {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 20px;
        margin-bottom: 40px;
    }
    .nitelik-card {
        background-color: #001d3d;
        border: 1px solid #FEDD00;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        min-width: 150px;
    }
    .n-val { color: #FEDD00; font-size: 1.5rem; font-weight: bold; display: block; }
    .n-lab { color: #ffffff; font-size: 0.85rem; }

    /* TABLO TASARIMI */
    .table-container { display: flex; justify-content: center; margin: 20px 0; }
    .styled-table { 
        width: auto !important; margin: auto; border-collapse: collapse; color: white; 
        table-layout: auto !important; 
    }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 12px 20px; }
    .styled-table td { border: 1px solid #FEDD00; padding: 10px 18px; text-align: center !important; }
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

def clean_df(df):
    return df.applymap(lambda x: "" if (pd.isna(x) or str(x).strip() in ["0", "0.0", "0.00"]) else (int(x) if isinstance(x, (int, float)) else x))

# --- ANA BAŞLIK ---
st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. ÜST KISIM: KURUL VE BAŞVURU (KUTU İÇİNDE VE ARALIKLI) ---
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.metric(label="Kurul Sayısı", value="5")
with col_m2:
    st.metric(label="Toplam Başvuru", value="206")

# --- 2. ALT KISIM: NİTELİK SAYILARI ---
st.markdown("""
    <div class="nitelik-row">
        <div class="nitelik-card"><span class="n-val">135</span><span class="n-lab">Bireysel Araştırma</span></div>
        <div class="nitelik-card"><span class="n-val">41</span><span class="n-lab">Uzmanlık Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">12</span><span class="n-lab">Y. Lisans Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">18</span><span class="n-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# --- 3. GÜNDEM TABLOSU ---
if df_gundem is not None:
    st.markdown("<h3>📅 2026 Gündem Sayıları</h3>", unsafe_allow_html=True)
    
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    dg = dg[dg['Toplam'] > 0]
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    
    t_row = pd.DataFrame([{
        "S.NO": "TOPLAM", "Gündem Tarihleri": "", "Başvuru": 206, "Düzeltme": 68, "Dilekçe": 45, "Toplam": 319
    }])
    dg_final = pd.concat([dg, t_row], ignore_index=True)
    
    html_g = clean_df(dg_final).to_html(index=False, classes='styled-table')
    html_g = html_g.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
    st.markdown(f'<div class="table-container">{html_g}</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:#FEDD00; padding:20px; font-weight:bold; border-top:1px solid #FEDD00; margin-top:30px;">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
