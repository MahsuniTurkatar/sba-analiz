import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="centered")

# --- CSS: GOLD NİTELİK ÇERÇEVESİ & DARK MOD ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Metrikler ve Nitelik Paneli için Gold Çerçeve */
    div[data-testid="stMetric"], .nitelik-box {
        background-color: #001d3d !important;
        border: 2px solid #ffc300 !important; /* İstediğin Sarı Çerçeve */
        border-radius: 12px !important;
        padding: 15px !important;
    }
    
    .nitelik-box {
        display: flex;
        justify-content: space-around;
        margin-bottom: 25px;
    }
    
    .n-item { text-align: center; }
    .n-label { color: #ffffff; font-size: 0.8rem; display: block; opacity: 0.8; }
    .n-value { color: #ffc300; font-weight: bold; font-size: 1.3rem; }
    
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETİ: 12 RAPORTÖR (Detaylı Süzme) ---
# verilerine göre güncellendi.
raportor_data = {
    "Dr. Öğr. Üyesi Müge DEMİR": {"Atanan": 31, "ONAY": 18, "DÜZELTME": 11, "KAEK": 2, "GÖRÜŞ": 0},
    "Doç. Dr. Kübra AYKAÇ": {"Atanan": 30, "ONAY": 14, "DÜZELTME": 9, "KAEK": 0, "GÖRÜŞ": 0},
    "Doç. Dr. Burcu ERSÖZ ALAN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 6, "KAEK": 0, "GÖRÜŞ": 0},
    "Prof. Dr. Gözde GİRGİN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 5, "KAEK": 0, "GÖRÜŞ": 5},
    "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY": {"Atanan": 28, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 6},
    "Prof. Dr. Melih Önder BABAOĞLU": {"Atanan": 28, "ONAY": 12, "DÜZELTME": 8, "KAEK": 0, "GÖRÜŞ": 8},
    "Prof. Dr. M. Özgür UYANIK": {"Atanan": 27, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 5},
    "Prof. Dr. Ayşe Nurten AKARSU": {"Atanan": 22, "ONAY": 11, "DÜZELTME": 4, "KAEK": 0, "GÖRÜŞ": 7},
    "Doç. Dr. Ekim GÜMELER": {"Atanan": 17, "ONAY": 11, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 1},
    "Prof. Dr. Yavuz AYHAN": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 8, "KAEK": 0, "GÖRÜŞ": 0},
    "Doç. Dr. Tolga ÇAKMAK": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 5, "KAEK": 1, "GÖRÜŞ": 2},
    "Prof. Dr. Ayşe KİN İŞLER": {"Atanan": 17, "ONAY": 12, "DÜZELTME": 3, "KAEK": 2, "GÖRÜŞ": 0}
}

# --- ARAYÜZ ---
st.markdown("<h1 style='text-align: center;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>SBA 2026 Karar Destek Paneli</h3>", unsafe_allow_html=True)

# 📌 1. ANA METRİKLER
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# 📌 2. SARI ÇERÇEVELİ NİTELİK PANELİ
st.markdown(f"""
    <div class="nitelik-box">
        <div class="n-item"><span class="n-label">Bireysel Araştırma</span><span class="n-value">128</span></div>
        <div class="n-item"><span class="n-label">Uzmanlık Tezi</span><span class="n-value">48</span></div>
        <div class="n-item"><span class="n-label">Y. Lisans Tezi</span><span class="n-value">10</span></div>
        <div class="n-item"><span class="n-label">Doktora Tezi</span><span class="n-value">4</span></div>
    </div>
""", unsafe_allow_html=True)

# --- 3. SEKMELER ---
tab1, tab2, tab3 = st.tabs(["👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.write("#### 🔍 Raportör Dosya ve Bekleyen Takibi")
    r_secim = st.selectbox("Raportör Seçiniz:", list(raportor_data.keys()))
    r = raportor_data[r_secim]
    
    # Karar verilenlerin toplamı (Tüm kategoriler)
    toplam_karar = sum(v for k, v in r.items() if k != "Atanan")
    bekleyen = r["Atanan"] - toplam_karar
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam Atanan", r["Atanan"])
    col2.metric("Karar Verilen", toplam_karar)
    # Bekleyen varsa kırmızımtırak bir uyarı hissi (isteğe bağlı)
    col3.metric("Bekleyen ⏳", bekleyen, delta=-bekleyen if bekleyen > 0 else None, delta_color="inverse")
    
    st.write("---")
    st.write("#### 📊 Detaylı İşlem Dağılımı")
    for k, v in r.items():
        if k != "Atanan":
            st.write(f"**{k}:** {v} dosya")
            st.progress(v / r["Atanan"] if r["Atanan"] > 0 else 0)

with tab2:
    # Birim analizi (image_c1625a.png yapısı korunarak)
    st.write("#### 🏢 Birimlerin Dosya Dağılımı")
    # ... Birim expander kodları ...

with tab3:
    # Sorumlu hoca analizi (image_c16297.png yapısı korunarak)
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü")
    # ... Sorumlu expander kodları ...

st.write("---")
st.markdown("<center style='color:#666;'>Hacettepe SBA Karar Destek Sistemi © 2026</center>", unsafe_allow_html=True)
