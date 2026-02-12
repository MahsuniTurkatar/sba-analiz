import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="centered")

# Gece Mavisi & Altın Sarısı Stil
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    .block-container { max-width: 800px; padding-top: 2rem; }
    
    /* Metrikler */
    div[data-testid="stMetric"] {
        background-color: #001d3d !important;
        border: 1px solid #ffc300 !important;
        border-radius: 12px !important;
    }
    
    /* Analiz Kartları */
    .data-card {
        background-color: #001d3d;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffc300;
        margin-bottom: 10px;
    }
    
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    .rank-num { color: #ffc300; font-weight: bold; font-size: 20px; margin-right: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Kurumsal Başlık
st.markdown("<h1 style='text-align: center;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu</h3>", unsafe_allow_html=True)
st.write("---")

# --- RAPORTÖR VERİLERİ (Tam Liste) ---
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

# --- BİRİM & SORUMLU VERİLERİ ---
ilk_5_birim = [
    {"Birim": "İç Hastalıkları Anabilim Dalı", "Sayi": 8},
    {"Birim": "Kulak Burun Boğaz Anabilim Dalı", "Sayi": 5},
    {"Birim": "Ortopedi ve Travmatoloji A.D.", "Sayi": 5},
    {"Birim": "Nöroloji Anabilim Dalı", "Sayi": 5},
    {"Birim": "Anatomi Anabilim Dalı", "Sayi": 4}
]

ilk_5_sorumlu = [
    {"Sorumlu": "Prof. Dr. Ömer Karadağ", "Birim": "İç Hastalıkları Anabilim Dalı", "Sayi": 6},
    {"Sorumlu": "Prof. Dr. Ahmet Yılmaz", "Birim": "Kulak Burun Boğaz Anabilim Dalı", "Sayi": 4},
    {"Sorumlu": "Doç. Dr. Mehmet Demir", "Birim": "Ortopedi ve Travmatoloji A.D.", "Sayi": 4},
    {"Sorumlu": "Prof. Dr. Ayşe Kaya", "Birim": "Nöroloji Anabilim Dalı", "Sayi": 3},
    {"Sorumlu": "Dr. Öğr. Üyesi Caner Ak", "Birim": "Anatomi Anabilim Dalı", "Sayi": 3}
]

# --- SEKME YAPISI ---
tab1, tab2, tab3 = st.tabs(["👥 Raportörler", "🏢 İlk 5 Birim", "👨‍🏫 İlk 5 Sorumlu"])

with tab1:
    secilen_r = st.selectbox("Raportör Seçiniz:", list(raportorler.keys()))
    u = raportorler[secilen_r]
    c1, c2, c3 = st.columns(3)
    karar = sum([u[k] for k in ["ONAY", "DÜZELTME", "KAEK", "GÖRÜŞ", "RET"]])
    c1.metric("Toplam", f"{u['Atanan']}")
    c2.metric("Karar", f"{karar}")
    c3.metric("Bekleyen", f"{u['Atanan'] - karar}")
    
    st.write("#### 📊 Dağılım")
    for k, v in u.items():
        if k != "Atanan":
            st.write(f"{k}: {v}")
            st.progress(v / u['Atanan'] if u['Atanan'] > 0 else 0)

with tab2:
    st.write("### 🏢 En Çok Başvuran İlk 5 Birim")
    for i, b in enumerate(ilk_5_birim, 1):
        st.markdown(f"""
            <div class="data-card">
                <span class="rank-num">#{i}</span>
                <span style="font-size:18px;"><b>{b['Birim']}</b></span>
                <span style="float:right; color:#ffc300; font-weight:bold;">{b['Sayi']} Dosya</span>
            </div>
        """, unsafe_allow_html=True)

with tab3:
    st.write("### 👨‍🏫 En Çok Başvuran İlk 5 Sorumlu")
    for i, s in enumerate(ilk_5_sorumlu, 1):
        st.markdown(f"""
            <div class="data-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span class="rank-num">#{i}</span>
                        <span style="font-size:18px;"><b>{s['Sorumlu']}</b></span><br>
                        <small style="margin-left:35px; color:#cccccc;">{s['Birim']}</small>
                    </div>
                    <div style="color:#ffc300; font-weight:bold; font-size:18px;">{s['Sayi']} Dosya</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.write("---")
st.markdown("<center style='color:#666;'>© 2026 Hacettepe SBA Karar Destek Sistemi</center>", unsafe_allow_html=True)
