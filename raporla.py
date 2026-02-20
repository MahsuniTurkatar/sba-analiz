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

# --- CSS: TÜM DÜZENLEMELER ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* BAŞLIKLAR */
    h1 { color: #ffffff !important; text-align: center !important; font-weight: bold !important; margin-bottom: 30px !important; }
    
    /* Gündem Sayıları Başlığı - Tabloya yakınlaştırma */
    .gundem-header { 
        color: #ffffff !important; 
        text-align: center !important; 
        font-weight: bold !important; 
        margin-top: 40px !important; 
        margin-bottom: 10px !important; 
        font-size: 1.5rem;
    }

    /* ANA KONTEYNERLAR */
    .metric-row {
        display: flex;
        justify-content: center;
        gap: 25px;
        margin-bottom: 20px;
        flex-wrap: nowrap;
    }

    /* BÜYÜK ÜST KUTULAR (5 ve 206) */
    .main-box {
        background-color: #001d3d;
        border: 2px solid #FEDD00;
        border-radius: 12px;
        padding: 20px 50px;
        text-align: center;
        min-width: 220px;
    }
    .main-val { color: #FEDD00; font-size: 3.5rem; font-weight: bold; display: block; line-height: 1; }
    .main-lab { color: #ffffff; font-size: 1.2rem; display: block; margin-top: 10px; }

    /* ALT NİTELİK KUTULARI */
    .sub-box {
        background-color: #001d3d;
        border: 1px solid #FEDD00;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        min-width: 160px;
    }
    .sub-val { color: #FEDD00; font-size: 1.8rem; font-weight: bold; display: block; }
    .sub-lab { color: #ffffff; font-size: 0.9rem; display: block; }

    /* TABLO AYARLARI */
    .table-container { display: flex; justify-content: center; width: 100%; }
    .styled-table { width: auto !important; margin: auto; border-collapse: collapse; color: white; }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 12px 20px; }
    .styled-table td { border: 1px solid #FEDD00; padding: 10px 18px; text-align: center !important; }
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# Sayı Temizleme Fonksiyonu (.0'lardan kurtulmak için)
def clean_numbers(df):
    def format_val(x):
        if pd.isna(x) or x == "": return ""
        try:
            val = float(x)
            if val == 0: return ""
            return str(int(val)) # Tam sayıya çevir
        except:
            return str(x)
    return df.applymap(format_val)

st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. ÜST KUTULAR: KURUL VE TOPLAM ---
st.markdown("""
    <div class="metric-row">
        <div class="main-box"><span class="main-val">5</span><span class="main-lab">Kurul Sayısı</span></div>
        <div class="main-box"><span class="main-val">206</span><span class="main-lab">Toplam Başvuru</span></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. ALT KUTULAR: NİTELİKLER ---
st.markdown("""
    <div class="metric-row">
        <div class="sub-box"><span class="sub-val">135</span><span class="sub-lab">Bireysel Araştırma</span></div>
        <div class="sub-box"><span class="sub-val">41</span><span class="sub-lab">Uzmanlık Tezi</span></div>
        <div class="sub-box"><span class="sub-val">12</span><span class="sub-lab">Y. Lisans Tezi</span></div>
        <div class="sub-box"><span class="sub-val">18</span><span class="sub-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# --- 3. GÜNDEM TABLOSU ---
if df_gundem is not None:
    st.markdown('<div class="gundem-header">📅 2026 Gündem Sayıları</div>', unsafe_allow_html=True)
    
    # Veri işleme
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    dg = dg[dg['Toplam'] > 0]
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    
    # Toplam satırı
    t_row = pd.DataFrame([{"S.NO": "TOPLAM", "Gündem Tarihleri": "", "Başvuru": 206, "Düzeltme": 68, "Dilekçe": 45, "Toplam": 319}])
    dg_final = pd.concat([dg, t_row], ignore_index=True)
    
    # .0 Temizliği ve HTML'e çevirme
    html_g = clean_numbers(dg_final).to_html(index=False, classes='styled-table')
    html_g = html_g.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
    st.markdown(f'<div class="table-container">{html_g}</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:#FEDD00; padding:20px; font-weight:bold; border-top:1px solid #FEDD00; margin-top:30px;">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
