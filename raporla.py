import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx" 

@st.cache_data
def load_top_data():
    try:
        # Sayılar sayfası, S.NO satırı (skiprows=2)
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        return df_g
    except:
        return None

df_gundem = load_top_data()

# --- CSS: SAYILAR ÜSTTE, YAZILAR ALTTA VE ARALIKLI KUTULAR ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* BEYAZ VE ORTALI BAŞLIKLAR */
    h1, h2, h3 { 
        color: #ffffff !important; 
        text-align: center !important; 
        font-weight: bold !important;
    }

    /* KUTULARI YAN YANA VE ARALIKLI YAPAR */
    [data-testid="stHorizontalBlock"] {
        justify-content: center !important;
        gap: 60px !important;
    }

    /* KUTU İÇİ DÜZEN: SAYI ÜSTTE, ETİKET ALTTA */
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; 
        border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; 
        padding: 20px !important;
        text-align: center !important;
        display: flex !important;
        flex-direction: column-reverse !important; /* Etiketi alta, sayıyı üste iter */
    }

    /* SAYI (VALUE) STİLİ */
    [data-testid="stMetricValue"] { 
        color: #FEDD00 !important; 
        font-size: 3rem !important; 
        font-weight: bold !important;
    }

    /* YAZI (LABEL) STİLİ */
    [data-testid="stMetricLabel"] { 
        color: #ffffff !important; 
        font-size: 1.2rem !important;
        margin-top: 10px !important;
    }

    /* NİTELİK KARTLARI (KUTULARIN HEMEN ALTI) */
    .nitelik-row {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 30px 0;
    }
    .nitelik-card {
        background-color: #001d3d;
        border: 1px solid #FEDD00;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        min-width: 160px;
    }
    .n-val { color: #FEDD00; font-size: 1.6rem; font-weight: bold; display: block; }
    .n-lab { color: #ffffff; font-size: 0.9rem; }

    /* TABLO TASARIMI */
    .table-container { display: flex; justify-content: center; margin-top: 20px; }
    .styled-table { 
        width: auto !important; margin: auto; border-collapse: collapse; color: white;
    }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 12px 20px; }
    .styled-table td { border: 1px solid #FEDD00; padding: 10px 18px; text-align: center !important; }
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

def clean_df(df):
    return df.applymap(lambda x: "" if (pd.isna(x) or str(x).strip() in ["0", "0.0", "0.00"]) else (int(x) if isinstance(x, (int, float)) else x))

st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. ÜST KUTULAR (5 ve 206) ---
c1, c2 = st.columns(2)
with c1:
    st.metric(label="Kurul Sayısı", value="5")
with c2:
    st.metric(label="Toplam Başvuru", value="206")

# --- 2. NİTELİK SAYILARI (KUTULARIN ALTINDA) ---
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
    
    t_row = pd.DataFrame([{"S.NO": "TOPLAM", "Gündem Tarihleri": "", "Başvuru": 206, "Düzeltme": 68, "Dilekçe": 45, "Toplam": 319}])
    dg_final = pd.concat([dg, t_row], ignore_index=True)
    
    html_g = clean_df(dg_final).to_html(index=False, classes='styled-table')
    html_g = html_g.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
    st.markdown(f'<div class="table-container">{html_g}</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:#FEDD00; padding:20px; font-weight:bold; border-top:1px solid #FEDD00; margin-top:30px;">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
