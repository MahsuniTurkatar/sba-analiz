import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx"

@st.cache_data
def load_all_data():
    try:
        # Sayfaları oku
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        # Birleştirilmiş hücreler çözülmüş varsayılarak oku
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1") 
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot")
        return df_g, df_r, df_p
    except Exception as e:
        st.error(f"Excel Okuma Hatası: {e}")
        return None, None, None

df_gundem, df_raportor, df_pivot = load_all_data()

# --- CSS: FB TASARIMI (SABİT) ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
    }
    .nitelik-container { display: flex; justify-content: space-between; gap: 10px; margin: 20px 0; }
    .nitelik-card {
        flex: 1; background-color: #001d3d; border: 1px solid #FEDD00;
        border-radius: 8px; padding: 15px; text-align: center;
    }
    .n-val { color: #FEDD00; font-size: 1.5rem; font-weight: bold; display: block; }
    .n-lab { color: #ffffff; font-size: 0.9rem; }
    .table-container { display: flex; justify-content: center; margin: 20px 0; }
    .styled-table { width: 100% !important; border-collapse: collapse; color: white; }
    .styled-table th { background-color: #001d3d; color: #FEDD00; border: 1px solid #FEDD00; padding: 10px; text-align: center; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px; text-align: center; }
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #FEDD00 !important; }
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- İSKELET: ÜST METRİKLER (SABİT) ---
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# --- İSKELET: NİTELİK KARTLARI (SABİT) ---
st.markdown("""
    <div class="nitelik-container">
        <div class="nitelik-card"><span class="n-val">128</span><span class="n-lab">Bireysel Araştırma</span></div>
        <div class="nitelik-card"><span class="n-val">48</span><span class="n-lab">Uzmanlık Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">10</span><span class="n-lab">Y. Lisans Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">4</span><span class="n-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# --- GÜNDEM SAYILARI (45.0 DÜZELTMESİ) ---
if df_gundem is not None:
    # Sayıları int yap
    for col in df_gundem.columns[2:]: # Sayısal sütunlar genelde 2. indexten başlar
        df_gundem[col] = pd.to_numeric(df_gundem[col], errors='coerce').fillna(0).astype(int)
    
    # 0 olanları gösterme, TOPLAM kalsın
    df_display = df_gundem[(df_gundem.iloc[:, 5] > 0) | (df_gundem.iloc[:, 0] == "TOPLAM")]
    
    st.write("### 📅 2026 Gündem Sayıları")
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.markdown(df_display.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Araştırmacı Analizi"])

with tab1:
    st.write("#### 📋 Kurul Karar Çizelgesi")
    img_path = "genel_tablo_ekran_goruntusu.png"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.warning("⚠️ Görsel dosyası (genel_tablo_ekran_goruntusu.png) bulunamadı. Lütfen GitHub'a yükleyin.")

with tab2:
    st.write("#### 👥 Raportör Detaylı Analizi")
    if df_raportor is not None:
        # Sütun isimlerinden bağımsız olarak 2. sütunu (Adı Soyadı) al
        raportor_list = df_raportor.iloc[:, 1].dropna().unique().tolist()
        sec_r = st.selectbox("Raportör Seçin:", raportor_list)
        r_data = df_raportor[df_raportor.iloc[:, 1] == sec_r].iloc[0]
        
        rc1, rc2, rc3 = st.columns(3)
        rc1.metric("📌 Atanan Dosya", int(r_data[2]))
        rc2.metric("✅ Karar Verilen", int(r_data.iloc[-1]))
        rc3.metric("⏳ Bekleyen", int(r_data[2]) - int(r_data.iloc[-1]))

with tab3:
    st.write("#### 🏢 Birim Analizi")
    if df_pivot is not None:
        # Pivot sayfasındaki ilk iki sütun
        birim_data = df_pivot.iloc[:, [0, 1]].dropna()
        birim_data.columns = ["Birim Adı", "Dosya Sayısı"]
        st.table(birim_data)

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Analizi")
    if df_pivot is not None:
        # Pivot sayfasındaki 4. ve 5. sütun
        sorumlu_data = df_pivot.iloc[:, [3, 4]].dropna()
        sorumlu_data.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        st.table(sorumlu_data)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
