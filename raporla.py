import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="centered")

# --- CSS: KURUMSAL DARK & GOLD ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important;
        border: 1px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    .nitelik-box {
        background-color: #001d3d;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #1e3a5f;
        display: flex;
        justify-content: space-around;
        margin-bottom: 25px;
    }
    .n-item { text-align: center; }
    .n-label { color: #ffffff; font-size: 0.8rem; display: block; }
    .n-value { color: #ffc300; font-weight: bold; font-size: 1.2rem; }
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETİ: 12 RAPORTÖR (Tam Liste) ---
raportor_data = {
    "Dr. Öğr. Üyesi Müge DEMİR": {"Atanan": 31, "ONAY": 18, "DÜZELTME": 11, "KAEK": 2},
    "Doç. Dr. Kübra AYKAÇ": {"Atanan": 30, "ONAY": 14, "DÜZELTME": 9, "KAEK": 7},
    "Doç. Dr. Burcu ERSÖZ ALAN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 6, "KAEK": 4},
    "Prof. Dr. Gözde GİRGİN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 5, "KAEK": 5},
    "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY": {"Atanan": 28, "ONAY": 17, "DÜZELTME": 4, "KAEK": 7},
    "Prof. Dr. Melih Önder BABAOĞLU": {"Atanan": 28, "ONAY": 12, "DÜZELTME": 8, "KAEK": 8},
    "Prof. Dr. M. Özgür UYANIK": {"Atanan": 27, "ONAY": 17, "DÜZELTME": 4, "KAEK": 6},
    "Prof. Dr. Ayşe Nurten AKARSU": {"Atanan": 22, "ONAY": 11, "DÜZELTME": 4, "KAEK": 7},
    "Doç. Dr. Ekim GÜMELER": {"Atanan": 17, "ONAY": 11, "DÜZELTME": 4, "KAEK": 2},
    "Prof. Dr. Yavuz AYHAN": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 8, "KAEK": 0},
    "Doç. Dr. Tolga ÇAKMAK": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 5, "KAEK": 3},
    "Prof. Dr. Ayşe KİN İŞLER": {"Atanan": 17, "ONAY": 12, "DÜZELTME": 3, "KAEK": 2}
}

# --- VERİ SETİ: BİRİMLER VE SORUMLULAR ---
birim_listesi = [
    {"Ad": "İç Hastalıkları Anabilim Dalı", "Dosya": 27, "Bireysel": 20, "Uzmanlık": 7},
    {"Ad": "Çocuk Sağlığı ve Hastalıkları A.D.", "Dosya": 23, "Bireysel": 11, "Uzmanlık": 12},
    {"Ad": "Kadın Hastalıkları ve Doğum A.D.", "Dosya": 9, "Bireysel": 7, "Uzmanlık": 2}
]

sorumlu_listesi = [
    {"Ad": "Prof. Dr. Meltem Gülhan HALİL", "Birim": "İç Hastalıkları A.D.", "Dosya": 6, "Bireysel": 4, "Uzmanlık": 2},
    {"Ad": "Prof. Dr. Yasemin ÖZSÜREKCİ", "Birim": "Çocuk Sağlığı A.D.", "Dosya": 5, "Bireysel": 2, "Uzmanlık": 3},
    {"Ad": "Dr. Öğr. Üyesi Gonca ÖZTEN", "Birim": "Kadın Hastalıkları ve Doğum A.D.", "Dosya": 4, "Bireysel": 4, "Uzmanlık": 0}
]

# --- ANA EKRAN ---
st.markdown("<h1 style='text-align: center;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>SBA 2026 Karar Destek Paneli</h3>", unsafe_allow_html=True)

# 📌 1. ANA ÖZET METRİKLER
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# 📌 2. NİTELİK AÇILIMI (190 Dosya Detayı)
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
    st.write("#### 🔍 Raportör Dosya Detayları")
    r_secim = st.selectbox("Raportör Seçiniz:", list(raportor_data.keys()))
    r_verisi = raportor_data[r_secim]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Atanan", r_verisi["Atanan"])
    col2.metric("Karar Verilen", r_verisi["ONAY"] + r_verisi["DÜZELTME"] + r_verisi["KAEK"])
    col3.metric("Bekleyen", r_verisi["Atanan"] - (r_verisi["ONAY"] + r_verisi["DÜZELTME"] + r_verisi["KAEK"]))
    
    st.write("---")
    for k, v in r_verisi.items():
        if k != "Atanan":
            st.write(f"**{k}:** {v} dosya")
            st.progress(v / r_verisi["Atanan"])

with tab2:
    st.write("#### 🏢 Birimlerin Nitelik Dağılımı")
    for b in birim_listesi:
        with st.expander(f"{b['Ad']} ({b['Dosya']} Dosya)"):
            st.write(f"✅ Bireysel Araştırma: {b['Bireysel']}")
            st.write(f"🎓 Uzmanlık Tezi: {b['Uzmanlık']}")
            st.progress(b['Bireysel'] / b['Dosya'])

with tab3:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü")
    for s in sorumlu_listesi:
        with st.expander(f"{s['Ad']} ({s['Dosya']} Dosya)"):
            st.info(f"Birim: {s['Birim']}")
            st.write(f"📝 Bireysel Araştırma: {s['Bireysel']}")
            st.write(f"🎓 Uzmanlık Tezi: {s['Uzmanlık']}")

st.write("---")
st.markdown("<center style='color:#666;'>Hacettepe SBA Karar Destek Sistemi © 2026</center>", unsafe_allow_html=True)
