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

# --- CSS: TABLO DÜZENİNDE ÖZEL METRİKLER VE BEYAZ BAŞLIKLAR ---
st.markdown("""
    <style>
    /* ARKA PLAN */
    .stApp { background-color: #000814; }
    
    /* BEYAZ VE ORTALI BAŞLIKLAR */
    h1, h2, h3 { 
        color: #ffffff !important; 
        text-align: center !important; 
        font-weight: bold !important;
        margin-bottom: 20px !important;
    }

    /* ÜST METRİK TABLOSU: KURUL SOLDA, BAŞVURU SAĞDA */
    .top-metric-container {
        display: flex;
        justify-content: center;
        margin-bottom: 40px;
    }
    .top-metric-table {
        border-collapse: collapse;
        width: auto;
        border: 2px solid #FEDD00;
        background-color: #001d3d;
    }
    .top-metric-table td {
        border: 1px solid #FEDD00;
        padding: 20px 60px; /* Genişlik ayarı */
        text-align: center;
    }
    .val-text { 
        color: #FEDD00; 
        font-size: 3rem; /* Sayılar büyük */
        font-weight: bold; 
        display: block; 
        line-height: 1.1;
    }
    .lab-text { 
        color: #ffffff; 
        font-size: 1.2rem; 
        font-weight: normal; 
        margin-top: 5px;
        display: block;
    }

    /* GENEL TABLO AYARLARI: İĞNELENMİŞ GENİŞLİK */
    .table-container { 
        display: flex; 
        justify-content: center; 
        margin: 20px 0; 
        width: 100%; 
    }
    .styled-table { 
        width: auto !important; 
        margin: auto; 
        border-collapse: collapse; 
        color: white; 
        font-size: 0.95rem; 
        table-layout: auto !important; 
    }
    .styled-table th { 
        background-color: #001d3d; 
        color: #FEDD00 !important; 
        border: 1px solid #FEDD00; 
        padding: 12px 25px; 
        text-align: center !important; 
    }
    .styled-table td { 
        border: 1px solid #FEDD00; 
        padding: 10px 22px; 
        text-align: center !important; 
    }
    
    /* TOPLAM SATIRI SARI VURGU */
    .total-row td { 
        background-color: #001d3d !important; 
        color: #FEDD00 !important; 
        font-weight: bold !important; 
        border-top: 2px solid #FEDD00 !important; 
    }
    </style>
    """, unsafe_allow_html=True)

def clean_df(df):
    return df.applymap(lambda x: "" if (pd.isna(x) or str(x).strip() in ["0", "0.0", "0.00"]) else (int(x) if isinstance(x, (int, float)) else x))

# --- SAYFA BAŞLIĞI ---
st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. ADIM: ÜST METRİK TABLOSU (SOLDA 5, SAĞDA 206) ---
st.markdown("""
    <div class="top-metric-container">
        <table class="top-metric-table">
            <tr>
                <td>
                    <span class="val-text">5</span>
                    <span class="lab-text">Kurul Sayısı</span>
                </td>
                <td>
                    <span class="val-text">206</span>
                    <span class="lab-text">Toplam Başvuru</span>
                </td>
            </tr>
        </table>
    </div>
""", unsafe_allow_html=True)

# --- 2. ADIM: GÜNDEM SAYILARI TABLOSU ---
if df_gundem is not None:
    st.markdown("<h3>📅 2026 Gündem Sayıları</h3>", unsafe_allow_html=True)
    
    # Veri Hazırlığı
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    dg = dg[dg['Toplam'] > 0]
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    
    # Toplam Satırı Ekleme
    t_row = pd.DataFrame([{
        "S.NO": "TOPLAM", 
        "Gündem Tarihleri": "", 
        "Başvuru": 206, 
        "Düzeltme": 68, 
        "Dilekçe": 45, 
        "Toplam": 319
    }])
    dg_final = pd.concat([dg, t_row], ignore_index=True)
    
    # HTML Tablo Çıktısı
    html_g = clean_df(dg_final).to_html(index=False, classes='styled-table')
    html_g = html_g.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
    st.markdown(f'<div class="table-container">{html_g}</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:#FEDD00; padding:20px; font-weight:bold; border-top:1px solid #FEDD00; margin-top:30px;">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
