import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME VE TEMİZLEME ---
EXCEL_FILE = "2026_SBA.xlsx" 

@st.cache_data
def load_data():
    try:
        df_s = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Raportör")
        # Sütun isimlerindeki boşlukları temizle (KeyError'u bitiren hamle)
        df_r.columns = [str(c).strip() for c in df_r.columns]
        return df_s, df_r
    except:
        return None, None

df_gundem, df_raportor = load_data()

# --- CSS: SAKIN BOZMA DENİLEN VE YENİ EKLER ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    h1 { color: #ffffff !important; text-align: center !important; font-weight: bold !important; margin-bottom: 25px !important; }
    
    /* BAŞLIK MESAFELERİ */
    .section-header { color: #ffffff !important; text-align: center !important; font-weight: bold !important; margin-top: 35px !important; margin-bottom: 10px !important; font-size: 1.6rem; }

    /* ÜST KUTU SİSTEMİ (ÇİVİLENDİ) */
    .metric-row { display: flex; justify-content: center; gap: 20px; margin-bottom: 15px; flex-wrap: nowrap; }
    .main-box { background-color: #001d3d; border: 2px solid #FEDD00; border-radius: 12px; padding: 15px 45px; text-align: center; min-width: 200px; }
    .main-val { color: #FEDD00; font-size: 3.2rem; font-weight: bold; display: block; line-height: 1; }
    .main-lab { color: #ffffff; font-size: 1.1rem; display: block; margin-top: 8px; }

    /* NİTELİK VE RAPORTÖR KUTULARI */
    .sub-box { background-color: #001d3d; border: 1px solid #FEDD00; border-radius: 8px; padding: 12px; text-align: center; min-width: 155px; }
    .sub-val { color: #FEDD00; font-size: 1.7rem; font-weight: bold; display: block; }
    .sub-lab { color: #ffffff; font-size: 0.85rem; display: block; }

    /* TABLO TASARIMI (ORTALI VE İÇERİK KADAR) */
    .table-container { display: flex; justify-content: center; margin-top: 10px; width: 100%; }
    .styled-table { width: auto !important; margin: auto; border-collapse: collapse; color: white; font-size: 0.95rem; }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 12px 20px; text-align: center !important; }
    .styled-table td { border: 1px solid #FEDD00; padding: 10px 18px; text-align: center !important; }
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; }
    
    /* SELECTBOX STİLİ */
    .stSelectbox label { color: white !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# .0 Temizleme Fonksiyonu
def clean(val):
    if pd.isna(val) or val == "" or val == 0: return ""
    try: return str(int(float(val)))
    except: return str(val)

# --- ÜST TARAF (DOKUNULMAZ BÖLGE) ---
st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

st.markdown("""
    <div class="metric-row">
        <div class="main-box"><span class="main-val">5</span><span class="main-lab">Kurul Sayısı</span></div>
        <div class="main-box"><span class="main-val">206</span><span class="main-lab">Toplam Başvuru</span></div>
    </div>
    <div class="metric-row">
        <div class="sub-box"><span class="sub-val">135</span><span class="sub-lab">Bireysel Araştırma</span></div>
        <div class="sub-box"><span class="sub-val">41</span><span class="sub-lab">Uzmanlık Tezi</span></div>
        <div class="sub-box"><span class="sub-val">12</span><span class="sub-lab">Y. Lisans Tezi</span></div>
        <div class="sub-box"><span class="sub-val">18</span><span class="sub-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# --- 1. GÜNDEM SAYILARI TABLOSU ---
if df_gundem is not None:
    st.markdown('<div class="section-header">📅 2026 Gündem Sayıları</div>', unsafe_allow_html=True)
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    
    t_row = pd.DataFrame([{"S.NO": "TOPLAM", "Gündem Tarihleri": "", "Başvuru": 206, "Düzeltme": 68, "Dilekçe": 45, "Toplam": 319}])
    dg_f = pd.concat([dg, t_row], ignore_index=True).applymap(clean)
    
    st.markdown(f'<div class="table-container">{dg_f.to_html(index=False, classes="styled-table")}</div>', unsafe_allow_html=True)

# --- 2. RAPORTÖR ANALİZİ (GÖRÜNMEYEN KISIM BURADA) ---
if df_raportor is not None:
    st.markdown("---")
    st.markdown('<div class="section-header">👤 Raportör Karar Dağılım Analizi</div>', unsafe_allow_html=True)
    
    # Raportör Listesi
    raportorler = df_raportor['Adı Soyadı'].dropna().unique().tolist()
    col_sel, col_empty = st.columns([1, 2]) # Seçim kutusunu biraz sola çekelim
    with col_sel:
        secilen = st.selectbox("Raportör Seçiniz:", raportorler)
    
    # Veriyi Çek
    rd = df_raportor[df_raportor['Adı Soyadı'] == secilen].iloc[0]
    
    # Raportör Özet Kutuları
    st.markdown(f"""
    <div class="metric-row">
        <div class="sub-box"><span class="sub-val">{clean(rd.get('Dosya Sayısı', 0))}</span><span class="sub-lab">Atanan Dosya</span></div>
        <div class="sub-box"><span class="sub-val">{clean(rd.get('Onay Toplam', 0))}</span><span class="sub-lab">Onaylanan</span></div>
        <div class="sub-box"><span class="sub-val" style="color:#ff4b4b;">{clean(rd.get('Düzeltme Toplam', 0))}</span><span class="sub-lab">Düzeltme</span></div>
        <div class="sub-box"><span class="sub-val" style="color:#FEDD00;">{clean(rd.get('GENEL TOPLAM', 0))}</span><span class="sub-lab">Genel Toplam</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Detay Tablosu (Onay Detayları)
    st.markdown('<div class="section-header" style="font-size:1.2rem;">📊 Karar Detayları</div>', unsafe_allow_html=True)
    
    detay_data = {
        "Kategori": ["Bireysel Araştırma", "Uzmanlık Tezi", "Yüksek Lisans Tezi", "Doktora Tezi"],
        "Onay Sayısı": [
            clean(rd.get('Bireysel Araştırma Onay', 0)),
            clean(rd.get('Uzmanlık Tezi Onay', 0)),
            clean(rd.get('Yüksek Lisans Tezi Onay', 0)),
            clean(rd.get('Doktora Tezi Onay', 0))
        ]
    }
    df_detay = pd.DataFrame(detay_data)
    # Sadece 0 olmayanları göster
    df_detay = df_detay[df_detay['Onay Sayısı'] != ""]
    
    st.markdown(f'<div class="table-container">{df_detay.to_html(index=False, classes="styled-table")}</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:#FEDD00; padding:20px; font-weight:bold; border-top:1px solid #FEDD00; margin-top:40px;">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
