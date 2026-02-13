import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="centered")

# --- CSS: GOLD ÇERÇEVE & MERKEZİ HİZALAMA ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Metrikleri ve Sayıları Ortala */
    div[data-testid="stMetric"] {
        background-color: #001d3d !important;
        border: 2px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        text-align: center !important;
    }
    div[data-testid="stMetricValue"] {
        display: flex;
        justify-content: center !important;
    }
    div[data-testid="stMetricLabel"] {
        display: flex;
        justify-content: center !important;
    }
    
    /* Sarı Çerçeveli Nitelik Paneli */
    .nitelik-box {
        background-color: #001d3d;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #ffc300;
        display: flex;
        justify-content: space-around;
        margin-bottom: 25px;
        text-align: center;
    }
    
    .n-item { flex: 1; }
    .n-label { color: #ffffff; font-size: 0.85rem; display: block; margin-bottom: 5px; }
    .n-value { color: #ffc300; font-weight: bold; font-size: 1.4rem; }
    
    /* Başlıklar ve Sekmeler */
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    
    /* Expander Stili */
    .stExpander {
        background-color: #001d3d !important;
        border: 1px solid #1e3a5f !important;
        border-radius: 8px !important;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETLERİ ---
# Raportörler (Tam Liste ve Detaylı Kararlar)
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

birim_verileri = [
    {"Birim": "İç Hastalıkları Anabilim Dalı", "Sayi": 27, "Bireysel": 20, "Uzmanlık": 7, "Onay": 18, "Düzeltme": 7, "KAEK": 2},
    {"Birim": "Çocuk Sağlığı ve Hastalıkları A.D.", "Sayi": 23, "Bireysel": 11, "Uzmanlık": 12, "Onay": 15, "Düzeltme": 6, "KAEK": 2},
    {"Birim": "Kadın Hastalıkları ve Doğum A.D.", "Sayi": 9, "Bireysel": 7, "Uzmanlık": 2, "Onay": 6, "Düzeltme": 3, "KAEK": 0}
]

sorumlu_verileri = [
    {"Ad": "Prof. Dr. Meltem Gülhan HALİL", "Birim": "İç Hastalıkları A.D.", "Dosya": 6, "Bireysel": 4, "Uzmanlık": 2},
    {"Ad": "Prof. Dr. Yasemin ÖZSÜREKCİ", "Birim": "Çocuk Sağlığı A.D.", "Dosya": 5, "Bireysel": 2, "Uzmanlık": 3},
    {"Ad": "Dr. Öğr. Üyesi Gonca ÖZTEN", "Birim": "Kadın Hastalıkları ve Doğum A.D.", "Dosya": 4, "Bireysel": 4, "Uzmanlık": 0}
]

# --- ARAYÜZ BAŞLANGIÇ ---
st.markdown("<h1 style='text-align: center;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>SBA 2026 Karar Destek Sistemi</h3>", unsafe_allow_html=True)

# 1. ORTALANMIŞ ANA METRİKLER
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# 2. SARI ÇERÇEVELİ NİTELİK PANELİ (Ortalı)
st.markdown(f"""
    <div class="nitelik-box">
        <div class="n-item"><span class="n-label">Bireysel</span><span class="n-value">128</span></div>
        <div class="n-item"><span class="n-label">Uzmanlık</span><span class="n-value">48</span></div>
        <div class="n-item"><span class="n-label">Y. Lisans</span><span class="n-value">10</span></div>
        <div class="n-item"><span class="n-label">Doktora</span><span class="n-value">4</span></div>
    </div>
""", unsafe_allow_html=True)

# 3. SEKMELER
tab1, tab2, tab3 = st.tabs(["👥 Raportörler", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.write("#### 🔍 Raportör Dosya ve Bekleyen Takibi")
    r_secim = st.selectbox("Raportör Seçiniz:", list(raportor_data.keys()))
    r = raportor_data[r_secim]
    
    toplam_karar = sum(v for k, v in r.items() if k != "Atanan")
    bekleyen = r["Atanan"] - toplam_karar
    
    colA, colB, colC = st.columns(3)
    colA.metric("Atanan", r["Atanan"])
    colB.metric("Karar", toplam_karar)
    colC.metric("Bekleyen", bekleyen)
    
    st.write("---")
    for k, v in r.items():
        if k != "Atanan":
            st.write(f"**{k}:** {v}")
            st.progress(v / r["Atanan"])

with tab2:
    st.write("#### 🏢 Birimlerin Detaylı Karar Dağılımı")
    for b in birim_verileri:
        with st.expander(f"{b['Birim']} — {b['Sayi']} Dosya"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"📝 Bireysel: {b['Bireysel']}")
                st.write(f"🎓 Uzmanlık: {b['Uzmanlık']}")
            with col2:
                st.write(f"✅ Onay: {b['Onay']}")
                st.write(f"⚠️ Düzeltme: {b['Düzeltme']}")
                st.progress(b['Onay'] / b['Sayi'])

with tab3:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü")
    for s in sorumlu_verileri:
        with st.expander(f"{s['Ad']} — {s['Dosya']} Dosya"):
            st.markdown(f"**Birim:** {s['Birim']}")
            st.write(f"📄 Bireysel Araştırma: {s['Bireysel']}")
            st.write(f"🎓 Uzmanlık Tezi: {s['Uzmanlık']}")
            st.progress(s['Bireysel'] / s['Dosya'])

st.write("---")
st.markdown("<center style='color:#666;'>© 2026 Hacettepe SBA Karar Destek</center>", unsafe_allow_html=True)
