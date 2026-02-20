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
        # Sütun isimlerini ve "Adı Soyadı" verisini temizle
        df_r.columns = df_r.columns.str.strip()
        df_r['Adı Soyadı'] = df_r['Adı Soyadı'].astype(str).str.strip()
        return df_g, df_r
    except:
        return None, None

df_gundem, df_raportor = load_data()

# --- CSS: KESİN MERKEZLEME VE GÖRSEL DÜZEN ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* BAŞLIKLAR */
    h1, h2, h3 { color: #FFFFFF !important; text-align: center !important; }
    
    /* METRİKLERİ ORTALA VE YAN YANA TUT */
    [data-testid="stMetricValue"] { color: #FEDD00 !important; text-align: center !important; font-size: 2.2rem !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; text-align: center !important; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; 
        border: 2px solid #FEDD00 !important;
        border-radius: 12px !important;
        padding: 10px 30px !important;
        width: 220px !important;
        margin: 0 auto !important; /* Ortaya kilitler */
    }
    
    /* TABLOLAR: HER ŞEYİ ORTALAMA */
    .table-wrapper { display: flex; justify-content: center; width: 100%; margin: 20px 0; }
    .styled-table { margin: auto; border-collapse: collapse; color: white; font-size: 0.85rem; width: 80%; }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 10px; text-align: center !important; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px; text-align: center !important; }
    
    /* TOPLAM SATIRI VURGUSU */
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; border-top: 2px solid #FEDD00 !important; }
    </style>
    """, unsafe_allow_html=True)

# TEMİZLİK FONKSİYONU (.0 ve 0'ları siler)
def clean_df(df):
    def fmt(x):
        if pd.isna(x) or str(x).strip() in ["0", "0.0", ""]: return ""
        try: return int(float(x))
        except: return x
    return df.applymap(fmt)

st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. METRİKLER: YAN YANA VE ORTALI ---
# Sütunları daraltarak kutuları birbirine yaklaştırdım
_, col1, col2, _ = st.columns([1, 1, 1, 1])
with col1: st.metric("Toplam Başvuru", "206")
with col2: st.metric("Kurul Sayısı", "5")

# --- 2. GÜNDEM TABLOSU (TOPLAM SATIRI EKLENDİ) ---
if df_gundem is not None:
    st.markdown("<h3>🗓️ 2026 Gündem Sayıları</h3>", unsafe_allow_html=True)
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    dg = dg[dg['Toplam'] > 0]
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    
    # Alt Toplam Satırı Hesaplama
    t_basvuru = dg['Başvuru'].sum()
    t_duzeltme = dg['Düzeltme'].sum()
    t_dilekce = dg['Dilekçe'].sum()
    t_toplam = dg['Toplam'].sum()
    
    # Toplam satırını dataframe'e ekle
    toplam_row = pd.DataFrame([{"S.NO": "TOPLAM", "Gündem Tarihleri": "", "Başvuru": t_basvuru, "Düzeltme": t_duzeltme, "Dilekçe": t_dilekce, "Toplam": t_toplam}])
    dg_final = pd.concat([dg, toplam_row], ignore_index=True)
    
    html_g = clean_df(dg_final).to_html(index=False, classes="styled-table")
    html_g = html_g.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
    st.markdown(f'<div class="table-wrapper">{html_g}</div>', unsafe_allow_html=True)

# --- 3. RAPORTÖR TABLOSU (HATA DÜZELTİLDİ) ---
if df_raportor is not None:
    st.markdown("<h3>👥 Raportör Dosya ve Karar Dağılımı</h3>", unsafe_allow_html=True)
    
    # Sütunları güvenli şekilde seç
    cols = ["S.No", "Adı Soyadı", "Dosya Sayısı", "BİREYSEL TOPLAM", "YÜKSEK LİSANS TEZİ TOPLAM", "DOKTORA TEZİ TOPLAM", "UZMANLIK TEZİ TOPLAM", "Onay Toplam", "Karar Verilen Toplam "]
    df_r_clean = df_raportor.dropna(subset=['Adı Soyadı']).copy()
    
    # Mevcut olan sütunları filtrele
    valid_cols = [c for c in cols if c in df_r_clean.columns]
    df_display = df_r_clean[valid_cols]

    html_r = clean_df(df_display).to_html(index=False, classes='styled-table')
    # Satırda "TOPLAM" geçen yeri sarı yap
    html_r = html_r.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
    st.markdown(f'<div class="table-wrapper">{html_r}</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:white; padding:20px; font-weight:bold;">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
