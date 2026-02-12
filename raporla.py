import streamlit as st

# Sayfa Yapılandırması (Dar ve odaklı)
st.set_page_config(page_title="Hacettepe SBA", layout="centered")

# Dark Navy Blue & Gold Teması
st.markdown("""
    <style>
    .stApp { background-color: #000814; } /* Ultra koyu lacivert */
    .block-container { max-width: 800px; padding-top: 2rem; }
    
    /* Metrik Kartları */
    div[data-testid="stMetric"] {
        background-color: #001d3d !important;
        border: 1px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    div[data-testid="stMetricValue"] > div { color: #ffc300 !important; }
    div[data-testid="stMetricLabel"] > div { color: #ffffff !important; }

    /* Birim Kartları */
    .unit-card {
        background-color: #001d3d;
        padding: 15px;
        border-radius: 10px;
        border-right: 5px solid #ffc300;
        margin-bottom: 10px;
    }
    
    /* Genel Yazı Renkleri */
    h1, h2, h3, h4, label { color: #ffc300 !important; }
    p, span { color: #ffffff !important; }
    .stSelectbox label { color: #ffc300 !important; }
    </style>
    """, unsafe_allow_html=True)

# Kurumsal Başlık
st.markdown("<h1 style='text-align: center;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu</h3>", unsafe_allow_html=True)
st.write("---")

# --- TAM RAPORTÖR LİSTESİ (12 Kişi) ---
raportorler = {
    "Dr. Öğr. Üyesi Müge DEMİR": {"Atanan": 31, "ONAY": 18, "DÜZELTME": 11, "KAEK": 2, "GÖRÜŞ": 0, "RET": 0},
    "Doç. Dr. Kübra AYKAÇ": {"Atanan": 30, "ONAY": 14, "DÜZELTME": 9, "KAEK": 0, "GÖRÜŞ": 1, "RET": 1},
    "Doç. Dr. Burcu ERSÖZ ALAN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 6, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0},
    "Prof. Dr. Gözde GİRGİN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 5, "KAEK": 0, "GÖRÜŞ": 1, "RET": 0},
    "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY": {"Atanan": 28, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0},
    "Prof. Dr. Melih Önder BABAOĞLU": {"Atanan": 28, "ONAY": 12, "DÜZELTME": 8, "KAEK": 0, "GÖRÜŞ": 1, "RET": 1},
    "Prof. Dr. M. Özgür UYANIK": {"Atanan": 27, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0},
    "Prof. Dr. Ayşe Nurten AKARSU": {"Atanan": 22, "ONAY": 11, "DÜZELTME": 4, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0},
    "Doç. Dr. Ekim GÜMELER": {"Atanan": 17, "ONAY": 11, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 0, "RET": 1},
    "Prof. Dr. Yavuz AYHAN": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 8, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0},
    "Doç. Dr. Tolga ÇAKMAK": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 5, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0},
    "Prof. Dr. Ayşe KİN İŞLER": {"Atanan": 17, "ONAY": 12, "DÜZELTME": 3, "KAEK": 2, "GÖRÜŞ": 0, "RET": 0}
}

# --- BİRİM VE SORUMLU LİSTESİ ---
birim_verisi = [
    {"Birim": "İç Hastalıkları Anabilim Dalı", "Sorumlu": "Prof. Dr. Ömer Karadağ", "Sayi": 8},
    {"Birim": "Kulak Burun Boğaz Anabilim Dalı", "Sorumlu": "Prof. Dr. Ahmet Yılmaz", "Sayi": 5},
    {"Birim": "Ortopedi ve Travmatoloji A.D.", "Sorumlu": "Doç. Dr. Mehmet Demir", "Sayi": 5},
    {"Birim": "Nöroloji Anabilim Dalı", "Sorumlu": "Prof. Dr. Ayşe Kaya", "Sayi": 5},
    {"Birim": "Anatomi Anabilim Dalı", "Sorumlu": "Dr. Öğr. Üyesi Caner Ak", "Sayi": 4}
]

tab1, tab2 = st.tabs(["👥 Raportör Dosya Takibi", "🏢 Birim & Sorumlu Analizi"])

with tab1:
    secilen_r = st.selectbox("Analiz Edilecek Raportörü Seçiniz:", list(raportorler.keys()))
    u = raportorler[secilen_r]
    
    c1, c2, c3 = st.columns(3)
    karar_toplam = u['ONAY'] + u['DÜZELTME'] + u['KAEK'] + u['GÖRÜŞ'] + u['RET']
    c1.metric("Toplam Atanan", f"{u['Atanan']}")
    c2.metric("Karar Verilen", f"{karar_toplam}")
    c3.metric("İşlem Bekleyen", f"{u['Atanan'] - karar_toplam}")

    st.write("#### 📊 Süreç Dağılımı")
    for k, v in u.items():
        if k != "Atanan":
            st.write(f"{k}: {v}")
            st.progress(v / u['Atanan'] if u['Atanan'] > 0 else 0)

with tab2:
    # Sorumlu Menüsü (Selectbox)
    sorumlu_listesi = [b['Sorumlu'] for b in birim_verisi]
    secilen_s = st.selectbox("Sorumluya Göre Filtrele:", ["Tüm Birimler"] + sorumlu_listesi)
    
    st.write("#### 🏢 Birim Bazlı İş Yükü")
    for b in birim_verisi:
        if secilen_s == "Tüm Birimler" or secilen_s == b['Sorumlu']:
            st.markdown(f"""
                <div class="unit-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <b style="color:#ffc300; font-size:16px;">{b['Birim']}</b><br>
                            <small style="color:#cccccc;">Sorumlu: {b['Sorumlu']}</small>
                        </div>
                        <div style="font-size: 20px; font-weight: bold; color:#ffc300;">{b['Sayi']} Dosya</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

st.write("---")
st.markdown("<center style='color:#666;'>© 2026 Hacettepe SBA Karar Destek Sistemi</center>", unsafe_allow_html=True)
