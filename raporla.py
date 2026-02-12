import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# Lacivert Arka Plan & Sarı Yazı Stili
st.markdown("""
    <style>
    .main { background-color: #002366; }
    /* Metrik Kutuları: Lacivert zemin, Sarı yazı */
    div[data-testid="stMetric"] {
        background-color: #001a4d !important;
        border: 2px solid #FFD700 !important;
        padding: 15px !important;
        border-radius: 10px !important;
    }
    div[data-testid="stMetric"] label, div[data-testid="stMetric"] div {
        color: #FFD700 !important;
    }
    /* Birim Kartları */
    .unit-card {
        background-color: #001a4d;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FFD700;
        margin-bottom: 10px;
        color: #FFD700;
    }
    h1, h2, h3, h4, p, span { color: #FFD700 !important; }
    .stTabs [data-baseweb="tab"] { color: #FFD700 !important; }
    </style>
    """, unsafe_allow_html=True)

# Başlıklar
st.title("🏛️ Hacettepe Üniversitesi")
st.subheader("Sağlık Bilimleri Araştırma Etik Kurulu")
st.write("---")

# --- GÜNCEL VERİ SETİ (Excel ile Tam Uyumlu) ---
raportorler = {
    "Dr. Öğr. Üyesi Müge DEMİR": {"Atanan": 31, "ONAY": 18, "DÜZELTME": 11, "KAEK": 2, "GÖRÜŞ": 0, "RET": 0},
    "Doç. Dr. Kübra AYKAÇ": {"Atanan": 30, "ONAY": 14, "DÜZELTME": 9, "KAEK": 0, "GÖRÜŞ": 1, "RET": 1},
    "Doç. Dr. Burcu ERSÖZ ALAN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 6, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0},
    "Prof. Dr. Gözde GİRGİN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 5, "KAEK": 0, "GÖRÜŞ": 1, "RET": 0},
    "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY": {"Atanan": 28, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0},
    "Prof. Dr. Melih Önder BABAOĞLU": {"Atanan": 28, "ONAY": 12, "DÜZELTME": 8, "KAEK": 0, "GÖRÜŞ": 1, "RET": 1}
}

birim_detay = [
    {"Birim": "Kulak Burun Boğaz Anabilim Dalı", "Sorumlu": "Prof. Dr. X", "Sayi": 5},
    {"Birim": "Ortopedi ve Travmatoloji Anabilim Dalı", "Sorumlu": "Doç. Dr. Y", "Sayi": 5},
    {"Birim": "Nöroloji Anabilim Dalı", "Sorumlu": "Prof. Dr. Z", "Sayi": 5},
    {"Birim": "Anatomi Anabilim Dalı", "Sorumlu": "Dr. Öğr. Üyesi A", "Sayi": 4},
    {"Birim": "Radyoloji Anabilim Dalı", "Sorumlu": "Prof. Dr. B", "Sayi": 4},
    {"Birim": "Çocuk ve Ergen Ruh Sağlığı A.D.", "Sorumlu": "Doç. Dr. C", "Sayi": 4},
    {"Birim": "Üroloji Anabilim Dalı", "Sorumlu": "Dr. Öğr. Üyesi D", "Sayi": 4},
    {"Birim": "Deri ve Zührevi Hastalıklar A.D.", "Sorumlu": "Prof. Dr. E", "Sayi": 4},
    {"Birim": "Fiziksel Tıp ve Rehabilitasyon A.D.", "Sorumlu": "Doç. Dr. F", "Sayi": 3},
    {"Birim": "Göz Hastalıkları Anabilim Dalı", "Sorumlu": "Dr. G", "Sayi": 3}
]

tab1, tab2 = st.tabs(["👤 Raportör Detay", "🏢 Birim & Sorumlu"])

with tab1:
    secilen = st.selectbox("Raportör Seçiniz:", list(raportorler.keys()))
    u = raportorler[secilen]
    
    # Metrikler
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Atanan", f"{u['Atanan']}")
    karar_sayisi = u['ONAY'] + u['DÜZELTME'] + u['KAEK'] + u['GÖRÜŞ'] + u['RET']
    c2.metric("Karar Verilen", f"{karar_sayisi}")
    c3.metric("Bekleyen", f"{u['Atanan'] - karar_sayisi}")

    st.markdown("#### 📊 İşlem Kırılımı")
    for k, v in u.items():
        if k != "Atanan" and v >= 0:
            st.write(f"{k}: {v}")
            st.progress(v / u['Atanan'] if u['Atanan'] > 0 else 0)

with tab2:
    st.subheader("🏢 Birim Bazlı Başvuru ve Sorumlular")
    for b in birim_detay:
        st.markdown(f"""
            <div class="unit-card">
                <div style="display: flex; justify-content: space-between;">
                    <span><b>{b['Birim']}</b><br><small>Sorumlu: {b['Sorumlu']}</small></span>
                    <span style="font-size: 20px;"><b>{b['Sayi']} Dosya</b></span>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.write("---")
st.write("© 2026 Hacettepe Üniversitesi SBA")
