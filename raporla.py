import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx" 

@st.cache_data
def load_data():
    try:
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1")
        return df_g, df_r
    except:
        return None, None

df_gundem, df_raportor = load_data()

# --- CSS: KESİN MERKEZLEME VE GÖRSEL DÜZEN ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* BAŞLIKLAR VE METRİKLER */
    h1, h2, h3, h4, [data-testid="stMetricLabel"] { 
        color: #FFFFFF !important; 
        text-align: center !important; 
        display: block !important;
    }
    
    [data-testid="stMetricValue"] { color: #FEDD00 !important; text-align: center !important; }
    
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
        margin: auto !important; width: fit-content !important; padding: 10px 40px !important;
    }

    /* TABLOLAR: HER ŞEYİ ORTALAMA */
    .table-wrapper { display: flex; justify-content: center; width: 100%; margin: 20px 0; }
    .styled-table { margin: auto; border-collapse: collapse; color: white; font-size: 0.85rem; }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 10px; text-align: center !important; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px; text-align: center !important; }
    
    /* TOPLAM SATIRI */
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# TEMİZLİK FONKSİYONU (.0 ve 0'ları siler)
def format_table(df):
    return df.applymap(lambda x: "" if (str(x) == "0" or str(x) == "0.0" or pd.isna(x)) else (int(x) if isinstance(x, (float, int)) else x))

st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. METRİKLER (ORTALI) ---
c1, c2 = st.columns(2)
with c1: st.metric("Toplam Başvuru", "206")
with c2: st.metric("Kurul Sayısı", "5")

# --- 2. GÜNDEM TABLOSU ---
if df_gundem is not None:
    st.markdown("<h3>🗓️ 2026 Gündem Sayıları</h3>", unsafe_allow_html=True)
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    dg = dg[dg['Toplam'] > 0]
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    st.markdown(f'<div class="table-wrapper">{format_table(dg).to_html(index=False, classes="styled-table")}</div>', unsafe_allow_html=True)

# --- 3. RAPORTÖR GENEL TABLOSU (İstediğin Tablo) ---
if df_raportor is not None:
    st.markdown("<h3>👥 Raportör Dosya ve Karar Dağılımı</h3>", unsafe_allow_html=True)
    
    # Sadece ana sütunları seçelim ki tablo boğulmasın (Excel'deki yapıyı koruyarak)
    columns_to_show = [
        "S.No", "Adı Soyadı", "Dosya Sayısı", 
        "BİREYSEL TOPLAM", "YÜKSEK LİSANS TEZİ TOPLAM", 
        "DOKTORA TEZİ TOPLAM", "UZMANLIK TEZİ TOPLAM", 
        "Onay Toplam", "Düzeltme Toplam ", "Karar Verilen Toplam "
    ]
    
    # Sütunların varlığını kontrol et ve temizle
    df_r_clean = df_raportor.copy()
    df_r_clean.columns = df_r_clean.columns.str.strip()
    available_cols = [c for c in columns_to_show if c.strip() in df_r_clean.columns]
    
    final_df = df_r_clean[available_cols].dropna(subset=["Adı Soyadı"])
    
    # HTML çıktı ve Toplam satırı renklendirme
    html_r = format_table(final_df).to_html(index=False, classes='styled-table')
    html_r = html_r.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
    
    st.markdown(f'<div class="table-wrapper">{html_r}</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:white; padding:20px;">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
