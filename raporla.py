import streamlit as st

# Sayfa Yapılandırması (Geniş yerine merkez odaklı)
st.set_page_config(page_title="Hacettepe SBA", layout="centered")

# Koyu Lacivert & Sarı Kurumsal Stil
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp { background-color: #001233; }
    
    /* İçerik Konteyner Sınırlandırma */
    .block-container { padding-top: 2rem; max-width: 800px; }
    
    /* Metrik Kartları */
    div[data-testid="stMetric"] {
        background-color: #001a4d !important;
        border: 1px solid #FFD700 !important;
        padding: 10px !important;
        border-radius: 8px !important;
        text-align: center;
    }
    div[data-testid="stMetricValue"] > div { color: #FFD700 !important; font-size: 24px !important; }
    div[data-testid="stMetricLabel"] > div { color: #ffffff !important; font-size: 14px !important; }

    /* Birim Kartları */
    .unit-card {
        background-color: #001a4d;
        padding: 12px;
        border-radius: 10px;
        border-right: 4px solid #FFD700;
        margin-bottom: 8px;
        color: #ffffff;
    }
    .unit-title { color: #FFD700; font-weight: bold; font-size: 16px; }
    .unit-sorumlu { color: #cccccc; font-size: 13px; }
    
    /* Başlık ve Yazı Renkleri */
    h1, h2, h3, h4, p, span, label { color: #FFD700 !important; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; }
    .stTabs [aria-selected="true"] { color: #FFD700 !important; border-bottom-color: #FFD700 !important; }
    </style>
    """, unsafe_allow_html=True)

# Kurumsal Başlık
st.markdown("<h1 style='text-align: center; margin-bottom:0;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-top:0;'>Sağlık Bilimleri Araştırma Etik Kurulu</h3>", unsafe_allow_html=True)
st.write("---")

# --- EXCEL VERİLERİ (Tam Uyumlu) ---
raportorler = {
    "Dr. Öğr. Üyesi Müge DEMİR": {"Atanan": 31, "ONAY": 18, "DÜZELTME": 11, "KAEK": 2, "GÖRÜŞ": 0, "RET": 0},
    "Doç. Dr. Kübra AYKAÇ": {"Atanan": 30, "ONAY": 14, "DÜZELTME": 9, "KAEK": 0, "GÖRÜŞ": 1, "RET": 1},
    "Doç. Dr. Burcu ERSÖZ ALAN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 6, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0},
    "Prof. Dr. Gözde GİRGİN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 5, "KAEK": 0, "GÖRÜŞ": 1, "RET": 0},
    "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY": {"Atanan": 28, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0},
    "Prof. Dr. Melih Önder BABAOĞLU": {"Atanan": 28, "ONAY": 12, "DÜZELTME": 8, "KAEK": 0, "GÖRÜŞ": 1, "RET": 1}
}

birimler = [
    {"Birim": "Kulak Burun Boğaz Anabilim Dalı", "Sorumlu": "Prof. Dr. Ahmet Yılmaz", "Sayi": 5},
    {"Birim": "Ortopedi ve Travmatoloji Anabilim Dalı", "Sorumlu": "Doç. Dr. Mehmet Demir", "Sayi": 5},
    {"Birim": "Nöroloji Anabilim Dalı", "Sorumlu": "Prof. Dr. Ayşe Kaya", "Sayi": 5},
    {"Birim": "Anatomi Anabilim Dalı", "Sorumlu": "Dr. Öğr. Üyesi Caner Ak", "Sayi": 4},
    {"Birim": "Radyoloji Anabilim Dalı", "Sorumlu": "Prof. Dr. Selin Er", "Sayi": 4}
]

tab1, tab2 = st.tabs(["👤 Raportör Analizi", "🏢 Birim & Sorumlu"])

with tab1:
    secilen = st.selectbox("Raportör Seçiniz:", list(raportorler.keys()))
    u = raportorler[secilen]
    
    # Metrikler (Ekrana yayılmayan dar yapı)
    c1, c2, c3 = st.columns(3)
    c1.metric("Atanan", f"{u['Atanan']}")
    karar = sum([u[k] for k in ["ONAY", "DÜZELTME", "KAEK", "GÖRÜŞ", "RET"]])
    c2.metric("Karar", f"{karar}")
    c3.metric("Bekleyen", f"{u['Atanan'] - karar}")

    st.write("#### 📈 Detaylı Dağılım")
    for k, v in u.items():
        if k != "Atanan" and v >= 0:
            st.write(f"{k}: {v}")
            st.progress(v / u['Atanan'] if u['Atanan'] > 0 else 0)

with tab2:
    st.write("#### 🏢 Birim Dosya Dağılımı")
    for b in birimler:
        st.markdown(f"""
            <div class="unit-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div class="unit-title">{b['Birim']}</div>
                        <div class="unit-sorumlu">Sorumlu: {b['Sorumlu']}</div>
                    </div>
                    <div style="font-size: 18px; font-weight: bold; color: #FFD700;">{b['Sayi']} Dosya</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.write("---")
st.markdown("<div style='text-align: center; color: #aaaaaa !important; font-size: 12px;'>© 2026 Hacettepe SBA</div>", unsafe_allow_html=True)
