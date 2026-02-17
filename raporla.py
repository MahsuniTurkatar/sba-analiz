import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME (HATALARI GİDERİLMİŞ) ---
EXCEL_FILE = "2026_SBA.xlsx"

@st.cache_data
def load_data():
    try:
        # Excel'den sayfaları oku ve NaN (boş) değerleri temizle
        gundem_df = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2).head(5)
        # NaN olan yerleri "-" veya 0 ile doldurarak "Nan" yazısını engelle
        gundem_df = gundem_df.fillna("-")
        
        raportor_df = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1")
        raportor_df = raportor_df.fillna(0) # Sayısal kısımlardaki boşlukları 0 yap
        
        return gundem_df, raportor_df
    except Exception as e:
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
    .table-container { display: flex; justify-content: center; margin: 20px 0; }
    .styled-table { width: 85% !important; border-collapse: collapse; color: white; margin: auto; }
    .styled-table th { background-color: #001d3d; color: #FEDD00; border: 1px solid #FEDD00; padding: 12px; text-align: center !important; }
    .styled-table td { border: 1px solid #FEDD00; padding: 10px; text-align: center !important; }
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #FEDD00 !important; }
    /* Uyarı kutusunu lacivert yap (Kırmızıdan kurtulmak için) */
    .stAlert { background-color: #001d3d !important; color: #FEDD00 !important; border: 1px solid #FEDD00 !important; }
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- ANA PANEL ---
st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# Üst Metrikler
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# Gündem Tablosu (NaN Temizlenmiş)
st.write("### 📅 2026 Gündem Sayıları")
if df_gundem is not None:
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.markdown(df_gundem.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.write("#### 📋 Kurul Karar Çizelgesi")
    # Kırmızı uyarı yerine daha şık bir bilgilendirme
    img_path = "genel_tablo_ekran_goruntusu.png"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.info("ℹ️ Kurul Karar Çizelgesi görseli yüklendiğinde burada görünecektir.")

with tab2:
    st.write("#### 👥 Raportör Detaylı Analizi")
    if df_r_raw is not None:
        raportor_listesi = df_r_raw["Adı Soyadı"].dropna().unique().tolist()
        sec_r = st.selectbox("Raportör Seçiniz:", raportor_listesi)
        r_data = df_r_raw[df_r_raw["Adı Soyadı"] == sec_r].iloc[0]
        
        m_c1, m_c2, m_c3 = st.columns(3)
        dosya = r_data.get("Dosya Sayısı", 0)
        # TOPLAM sütununu Excel'deki "Üye_1" sayfasından alıyoruz
        onay = r_data.get("Onay", 0)
        m_c1.metric("📌 Atanan Dosya", int(dosya))
        m_c2.metric("✅ Onaylanan", int(onay))
        m_c3.metric("⏳ İşlemde", int(dosya - onay))
    else:
        st.warning("Veri yüklenemedi, lütfen Excel dosyasını kontrol edin.")

with tab3:
    st.write("#### 🏢 Birim Bazlı Başvuru Dağılımı")
    st.info("ℹ️ Birim analizleri bir sonraki güncelleme ile aktif olacaktır.")

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü")
    st.info("ℹ️ Sorumlu araştırmacı listesi hazırlanıyor.")

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
