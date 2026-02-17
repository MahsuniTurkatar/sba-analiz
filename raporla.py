import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME (DİNAMİK EXCEL) ---
EXCEL_FILE = "2026_SBA.xlsx"

@st.cache_data
def load_data():
    try:
        # Excel'den gerekli sayfaları oku
        gundem_df = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2).head(5) # İlk 5 satır (4 kurul + Toplam)
        raportor_df = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1")
        # Gereksiz sütunları temizle ve isimlendir
        return gundem_df, raportor_df
    except Exception as e:
        st.error(f"Excel dosyası okunurken hata oluştu: {e}")
        return None, None

df_gundem, df_r_raw = load_data()

# --- CSS: FB SARISI VE TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important;
        border: 2px solid #FEDD00 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        text-align: center !important;
    }
    .nitelik-container { display: flex; justify-content: space-between; gap: 10px; margin: 20px 0; }
    .nitelik-card {
        flex: 1; background-color: #001d3d; border: 1px solid #FEDD00;
        border-radius: 8px; padding: 15px; text-align: center;
    }
    .n-val { color: #FEDD00; font-size: 1.5rem; font-weight: bold; display: block; }
    .n-lab { color: #ffffff; font-size: 0.9rem; }
    .table-container { display: flex; justify-content: center; margin: 20px 0; }
    .styled-table { width: 85% !important; border-collapse: collapse; color: white; margin: auto; }
    .styled-table th { background-color: #001d3d; color: #FEDD00; border: 1px solid #FEDD00; padding: 12px; text-align: center !important; }
    .styled-table td { border: 1px solid #FEDD00; padding: 10px; text-align: center !important; }
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #FEDD00 !important; }
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- ANA PANEL ---
st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# Üst Metrikler (Excel'den çekilebilir veya sabit kalabilir)
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# Nitelik Kartları (Veriler Excel İstatistik sekmesinden manuel/otomatik)
st.markdown("""
    <div class="nitelik-container">
        <div class="nitelik-card"><span class="n-val">128</span><span class="n-lab">Bireysel Araştırma</span></div>
        <div class="nitelik-card"><span class="n-val">48</span><span class="n-lab">Uzmanlık Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">10</span><span class="n-lab">Y. Lisans Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">4</span><span class="n-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# Gündem Tablosu
st.write("### 📅 2026 Gündem Sayıları")
if df_gundem is not None:
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.markdown(df_gundem.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.write("#### 📋 Kurul Karar Çizelgesi")
    img_path = "genel_tablo_ekran_goruntusu.png"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.info("Kurul Karar Çizelgesi görseli bekleniyor...")

with tab2:
    st.write("#### 👥 Raportör Detaylı Analizi")
    # Burada Üye_1 sekmesindeki verileri kullanıyoruz
    if df_r_raw is not None:
        raportor_listesi = df_r_raw["Adı Soyadı"].dropna().tolist()
        sec_r = st.selectbox("Raportör Seçiniz:", raportor_listesi)
        r_data = df_r_raw[df_r_raw["Adı Soyadı"] == sec_r].iloc[0]
        
        # Sayısal Değerler
        dosya = r_data["Dosya"]
        onay = r_data["Onay"]
        duzeltme = r_data.get("Düzeltme", 0)
        ret = r_data.get("Ret", 0)
        kaek = r_data.get("KAEK", 0)
        kapsam = r_data.get("Kapsam Dışı", 0)
        geri = r_data.get("Geri Çekildi", 0)
        
        karar = int(onay + duzeltme + ret + kaek + kapsam + geri)
        
        m_c1, m_c2, m_c3 = st.columns(3)
        m_c1.metric("📌 Atanan Dosya", dosya)
        m_c2.metric("✅ Karar Verilen", karar)
        m_c3.metric("⏳ Bekleyen", int(dosya - karar))
        
        st.markdown(f"""
        <div style="background-color:#001d3d; border:1px solid #FEDD00; border-radius:10px; padding:20px; text-align:center;">
            <span style="color:#FEDD00;">✅ ONAY: {onay}</span> | 
            <span style="color:#FEDD00;">⚠️ DÜZELTME: {duzeltme}</span> | 
            <span style="color:#FEDD00;">📂 KAEK: {kaek}</span> | 
            <span style="color:#FEDD00;">❌ RET: {ret}</span> | 
            <span style="color:#FEDD00;">🚫 KAPSAM DIŞI: {kapsam}</span>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.write("#### 🏢 Birim Bazlı Başvuru Dağılımı")
    st.info("Bu kısım 'Pivot' sekmesinden otomatik beslenecek şekilde ayarlanabilir.")

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü")
    st.info("Sorumlu araştırmacı listesi Excel'den çekilmeye hazır.")

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
