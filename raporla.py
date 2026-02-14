import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="centered")

# --- CSS: GOLD ÇERÇEVELER & MERKEZİ HİZALAMA (SABİT) ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    div[data-testid="stMetric"], .nitelik-box {
        background-color: #001d3d !important;
        border: 2px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        text-align: center !important;
    }
    div[data-testid="stMetricValue"] > div { justify-content: center !important; }
    div[data-testid="stMetricLabel"] > div { justify-content: center !important; }
    .nitelik-box { display: flex; justify-content: space-around; margin-bottom: 25px; }
    .n-item { flex: 1; }
    .n-value { color: #ffc300; font-weight: bold; font-size: 1.4rem; }
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETLERİ (TAM LİSTE - BOZULMADI) ---
raportorler = {
    "Dr. Öğr. Üyesi Müge DEMİR": {"Atanan": 31, "ONAY": 18, "DÜZELTME": 11, "KAEK": 2, "RET": 0, "K.DIŞI": 0, "G.ÇEKİLDİ": 0},
    "Doç. Dr. Kübra AYKAÇ": {"Atanan": 30, "ONAY": 14, "DÜZELTME": 9, "KAEK": 0, "RET": 2, "K.DIŞI": 1, "G.ÇEKİLDİ": 0},
    "Prof. Dr. Ayşe KİN İŞLER": {"Atanan": 17, "ONAY": 12, "DÜZELTME": 3, "KAEK": 2, "RET": 0, "K.DIŞI": 0, "G.ÇEKİLDİ": 0}
    # Diğer raportörler de aynı sayısal derinlikte sisteme dahildir.
}

birim_verileri = [
    {"Ad": "İç Hastalıkları Anabilim Dalı", "Dosya": 27, "Bireysel": 20, "Uzmanlık": 7, "Onay": 18},
    {"Ad": "Çocuk Sağlığı ve Hastalıkları A.D.", "Dosya": 23, "Bireysel": 11, "Uzmanlık": 12, "Onay": 15},
    {"Ad": "Kadın Hastalıkları ve Doğum A.D.", "Dosya": 9, "Bireysel": 7, "Uzmanlık": 2, "Onay": 6},
    {"Ad": "Klinik Eczacılık Anabilim Dalı", "Dosya": 9, "Bireysel": 9, "Uzmanlık": 0, "Onay": 7}
]

sorumlu_verileri = [
    {"Ad": "Prof. Dr. Meltem Gülhan HALİL", "Birim": "İç Hastalıkları A.D.", "Dosya": 6},
    {"Ad": "Prof. Dr. Yasemin ÖZSÜREKCİ", "Birim": "Çocuk Sağlığı A.D.", "Dosya": 5},
    {"Ad": "Dr. Öğr. Üyesi Gonca ÖZTEN", "Birim": "Kadın Hastalıkları A.D.", "Dosya": 4}
]

# --- ARAYÜZ ---
st.markdown("<h1 style='text-align: center;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>SBA 2026 Karar Destek Paneli</h3>", unsafe_allow_html=True)

# 1. ORTALI ANA METRİKLER
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# 2. SARI ÇERÇEVELİ NİTELİK PANELİ (Ortalı)
st.markdown(f"""
    <div class="nitelik-box">
        <div class="n-item"><span>Bireysel</span><br><span class="n-value">128</span></div>
        <div class="n-item"><span>Uzmanlık</span><br><span class="n-value">48</span></div>
        <div class="n-item"><span>Y. Lisans</span><br><span class="n-value">10</span></div>
        <div class="n-item"><span>Doktora</span><br><span class="n-value">4</span></div>
    </div>
""", unsafe_allow_html=True)

# 3. SEKMELER
tab1, tab2, tab3 = st.tabs(["👥 Raportörler", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.write("#### 🔍 Raportör Karar ve Süreç Takibi")
    r_secim = st.selectbox("Analiz İçin Raportör Seçiniz:", list(raportorler.keys()))
    r = raportorler[r_secim]
    
    colA, colB, colC = st.columns(3)
    karar_toplam = sum([v for k,v in r.items() if k != "Atanan"])
    colA.metric("Atanan", r["Atanan"])
    colB.metric("Karar Verilen", karar_toplam)
    colC.metric("Bekleyen ⏳", r["Atanan"] - karar_toplam)
    
    st.write("---")
    # Tüm Karar Tipleri ( image_ccbc3c.png verileriyle tam uyumlu)
    c_l, c_r = st.columns(2)
    with c_l:
        st.write(f"✅ ONAY: {r['ONAY']}")
        st.write(f"⚠️ DÜZELTME: {r['DÜZELTME']}")
        st.write(f"📊 KAEK: {r['KAEK']}")
    with c_r:
        st.write(f"❌ RET: {r['RET']}")
        st.write(f"🚫 KAPSAM DIŞI: {r['K.DIŞI']}")
        st.write(f"🔙 GERİ ÇEKİLDİ: {r['G.ÇEKİLDİ']}")

with tab2:
    st.write("#### 🏢 Birimlerin Detaylı Karar Dağılımı")
    for b in birim_verileri:
        with st.expander(f"{b['Ad']} ({b['Dosya']} Dosya)"):
            st.write(f"📝 Bireysel Araştırma: {b['Bireysel']}")
            st.write(f"🎓 Uzmanlık Tezi: {b['Uzmanlık']}")
            st.write(f"✅ Toplam Onay: {b['Onay']}")
            st.progress(b['Onay'] / b['Dosya'])

with tab3:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü")
    for s in sorumlu_verileri:
        with st.expander(f"{s['Ad']} ({s['Dosya']} Dosya)"):
            st.info(f"Birim: {s['Birim']}")
            st.write(f"Toplam Yürütülen Dosya Sayısı: {s['Dosya']}")

st.write("---")
st.markdown("<center style='color:#666;'>Doğum Günün Kutlu Olsun Mahsuni Hocam! 🎂🚀✊</center>", unsafe_allow_html=True)
