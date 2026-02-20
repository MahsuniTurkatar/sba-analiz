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
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot")
        
        # Sütun isimlerini ve verileri temizle
        df_r.columns = df_r.columns.str.strip()
        df_r['Adı Soyadı'] = df_r['Adı Soyadı'].astype(str).str.strip()
        return df_g, df_r, df_p
    except:
        return None, None, None

df_gundem, df_raportor, df_pivot = load_data()

# --- CSS: KESİN VE NET ORTALAMA ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* BAŞLIKLAR: BEYAZ VE ORTALI */
    h1, h2, h3, h4 { color: #FFFFFF !important; text-align: center !important; }
    
    /* METRİKLER: ARASI DAR VE YAN YANA */
    [data-testid="stMetricValue"] { color: #FEDD00 !important; text-align: center !important; font-size: 2rem !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; text-align: center !important; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; 
        border: 2px solid #FEDD00 !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        width: 200px !important;
        margin: auto !important;
    }
    
    /* TABLO TASARIMI: SIFIRSIZ VE ORTALI */
    .table-wrapper { display: flex; justify-content: center; width: 100%; margin: 20px 0; }
    .styled-table { margin: auto; border-collapse: collapse; color: white; font-size: 0.85rem; }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 10px; text-align: center !important; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px; text-align: center !important; }
    
    /* TOPLAM SATIRI */
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; border: 2px solid #FEDD00 !important; }

    .footer { text-align: center; color: white; padding: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# GÖRSEL TEMİZLİK (.0 ve 0'ları siler)
def clean_df(df):
    def fmt(x):
        if pd.isna(x) or str(x).strip() in ["0", "0.0", ""]: return ""
        try: return int(float(x))
        except: return x
    return df.applymap(fmt)

st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. METRİKLER (DARALTIŞMIŞ VE ORTALI) ---
m_c1, m_c2 = st.columns(2)
with m_c1: st.metric("Toplam Başvuru", "206")
with m_c2: st.metric("Kurul Sayısı", "5")

# --- 2. GÜNDEM TABLOSU ---
if df_gundem is not None:
    st.markdown("<h3>🗓️ 2026 Gündem Sayıları</h3>", unsafe_allow_html=True)
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    dg = dg[dg['Toplam'] > 0]
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    st.markdown(f'<div class="table-wrapper">{clean_df(dg).to_html(index=False, classes="styled-table")}</div>', unsafe_allow_html=True)

# --- 3. ÜYE_1 GENEL TABLO (Kayıp Tablo Burada) ---
if df_raportor is not None:
    st.markdown("<h3>👥 Raportör Karar Dağılım Çizelgesi</h3>", unsafe_allow_html=True)
    
    # Excel'deki "Adı Soyadı" sütununda "TOPLAM" yazan satırı en sona alarak tabloyu göster
    df_main = df_raportor.dropna(subset=['Adı Soyadı']).copy()
    
    # Sadece senin istediğin ana sütunları seçiyoruz
    cols = ["S.No", "Adı Soyadı", "Dosya Sayısı", "BİREYSEL TOPLAM", "YÜKSEK LİSANS TEZİ TOPLAM", "DOKTORA TEZİ TOPLAM", "UZMANLIK TEZİ TOPLAM", "Onay Toplam", "Karar Verilen Toplam "]
    # Dosyada mevcut olanları filtrele
    existing_cols = [c for c in cols if c in df_main.columns]
    df_display = df_main[existing_cols]

    html_r = clean_df(df_display).to_html(index=False, classes='styled-table')
    # Toplam satırını boya
    html_r = html_r.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
    st.markdown(f'<div class="table-wrapper">{html_r}</div>', unsafe_allow_html=True)

# --- 4. BİRİM VE SORUMLU (YAN YANA VE ORTALI) ---
if df_pivot is not None:
    st.markdown("<h3>🏢 Birim ve 👨‍🏫 Sorumlu Analizi</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    with c1:
        b = df_pivot.iloc[:, [0, 1]].dropna().copy()
        b.columns = ["Birim Adı", "Sayı"]
        b = b[~b["Birim Adı"].str.contains("Etiketleri|Toplam|Genel", case=False)]
        st.markdown(f'<div class="table-wrapper">{clean_df(b).to_html(index=False, classes="styled-table")}</div>', unsafe_allow_html=True)
        
    with c2:
        s = df_pivot.iloc[:, [3, 4]].dropna().copy()
        s.columns = ["Sorumlu", "Sayı"]
        s = s[~s["Sorumlu"].str.contains("Etiketleri|Toplam|Genel", case=False)]
        st.markdown(f'<div class="table-wrapper">{clean_df(s).to_html(index=False, classes="styled-table")}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
