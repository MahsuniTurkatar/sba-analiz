import streamlit as st
import pandas as pd

# Sayfa Yapılandırması ve Üst Kısım (Mühürlü Bölge)
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx" 

@st.cache_data
def load_all_data():
    try:
        df_s = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        # Raportör sayfası genelde en baştan başlar veya başlıkları farklıdır
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Raportör") 
        return df_s, df_r
    except:
        return None, None

df_gundem, df_raportor = load_all_data()

# --- CSS (BOZULMAYACAK KISIM + YENİ EKLER) ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    h1 { color: #ffffff !important; text-align: center !important; font-weight: bold !important; margin-bottom: 30px !important; }
    .gundem-header { color: #ffffff !important; text-align: center !important; font-weight: bold !important; margin-top: 40px !important; margin-bottom: 10px !important; font-size: 1.5rem; }
    
    /* ÜST KUTULAR (İĞNELENDİ) */
    .metric-row { display: flex; justify-content: center; gap: 25px; margin-bottom: 20px; flex-wrap: nowrap; }
    .main-box { background-color: #001d3d; border: 2px solid #FEDD00; border-radius: 12px; padding: 20px 50px; text-align: center; min-width: 220px; }
    .main-val { color: #FEDD00; font-size: 3.5rem; font-weight: bold; display: block; line-height: 1; }
    .main-lab { color: #ffffff; font-size: 1.2rem; display: block; margin-top: 10px; }
    .sub-box { background-color: #001d3d; border: 1px solid #FEDD00; border-radius: 8px; padding: 15px; text-align: center; min-width: 160px; }
    .sub-val { color: #FEDD00; font-size: 1.8rem; font-weight: bold; display: block; }
    .sub-lab { color: #ffffff; font-size: 0.9rem; display: block; }

    /* TABLO VE ANALİZ */
    .table-container { display: flex; justify-content: center; width: 100%; }
    .styled-table { width: auto !important; margin: auto; border-collapse: collapse; color: white; font-size: 0.9rem; }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 10px 15px; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px 12px; text-align: center !important; }
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# Sayı Temizleme
def clean_num(x):
    if pd.isna(x) or x == "": return ""
    try:
        val = float(x)
        return str(int(val)) if val != 0 else ""
    except: return str(x)

# --- ÜST TARAF (DOKUNULMAZ) ---
st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)
st.markdown('<div class="metric-row"><div class="main-box"><span class="main-val">5</span><span class="main-lab">Kurul Sayısı</span></div><div class="main-box"><span class="main-val">206</span><span class="main-lab">Toplam Başvuru</span></div></div>', unsafe_allow_html=True)
st.markdown('<div class="metric-row"><div class="sub-box"><span class="sub-val">135</span><span class="sub-lab">Bireysel Araştırma</span></div><div class="sub-box"><span class="sub-val">41</span><span class="sub-lab">Uzmanlık Tezi</span></div><div class="sub-box"><span class="sub-val">12</span><span class="sub-lab">Y. Lisans Tezi</span></div><div class="sub-box"><span class="sub-val">18</span><span class="sub-lab">Doktora Tezi</span></div></div>', unsafe_allow_html=True)

if df_gundem is not None:
    st.markdown('<div class="gundem-header">📅 2026 Gündem Sayıları</div>', unsafe_allow_html=True)
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    t_row = pd.DataFrame([{"S.NO": "TOPLAM", "Gündem Tarihleri": "", "Başvuru": 206, "Düzeltme": 68, "Dilekçe": 45, "Toplam": 319}])
    dg_f = pd.concat([dg, t_row], ignore_index=True).applymap(clean_num)
    st.markdown(f'<div class="table-container">{dg_f.to_html(index=False, classes="styled-table")}</div>', unsafe_allow_html=True)

# --- 🎯 RAPORTÖR ANALİZİ (YENİ VE HATASIZ) ---
st.markdown("---")
st.markdown("<h2 style='color:white; text-align:center;'>👤 Raportör Karar Dağılım Analizi</h2>", unsafe_allow_html=True)

if df_raportor is not None:
    # Boşlukları ve gizli karakterleri temizle (KeyError önlemi)
    df_raportor.columns = [c.strip() for c in df_raportor.columns]
    
    # Raportör Seçimi
    raportorler = df_raportor['Adı Soyadı'].dropna().unique().tolist()
    secilen = st.selectbox("Analiz edilecek raportörü seçiniz:", raportorler)
    
    # Raportör Verisini Filtrele
    rd = df_raportor[df_raportor['Adı Soyadı'] == secilen].iloc[0]
    
    # Analiz Kartları (Metric gibi ama jilet gibi yan yana)
    st.markdown(f"""
    <div class="metric-row">
        <div class="sub-box"><span class="sub-val">{clean_num(rd.get('Dosya Sayısı', 0))}</span><span class="sub-lab">Atanan Dosya</span></div>
        <div class="sub-box"><span class="sub-val">{clean_num(rd.get('Onay Toplam', 0))}</span><span class="sub-lab">Toplam Onay</span></div>
        <div class="sub-box" style="border-color:#ff4b4b;"><span class="sub-val" style="color:#ff4b4b;">{clean_num(rd.get('Düzeltme Toplam', 0))}</span><span class="sub-lab">Düzeltme</span></div>
        <div class="sub-box" style="border-color:#4CAF50;"><span class="sub-val" style="color:#4CAF50;">{clean_num(rd.get('GENEL TOPLAM', 0))}</span><span class="sub-lab">Karar Verilen</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Detaylı Tablo Gösterimi
    st.markdown("<h3 style='color:white; text-align:center;'>Detaylı Karar Dökümü</h3>", unsafe_allow_html=True)
    cols = ['Bireysel Araştırma Onay', 'Uzmanlık Tezi Onay', 'Yüksek Lisans Tezi Onay', 'Doktora Tezi Onay']
    # Sütunlar varsa göster
    existing_cols = [c for c in cols if c in df_raportor.columns]
    if existing_cols:
        detay_df = pd.DataFrame({
            "Kategori": existing_cols,
            "Sayı": [clean_num(rd.get(c, 0)) for c in existing_cols]
        })
        st.markdown(f'<div class="table-container">{detay_df.to_html(index=False, classes="styled-table")}</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:#FEDD00; padding:20px; font-weight:bold; border-top:1px solid #FEDD00; margin-top:30px;">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
