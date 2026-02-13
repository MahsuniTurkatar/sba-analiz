import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="centered")

# --- CSS: GOLD ÇERÇEVELER & MERKEZİ HİZALAMA ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Ana Metrikler ve Nitelik Kutusu - Gold Çerçeve */
    div[data-testid="stMetric"], .nitelik-box {
        background-color: #001d3d !important;
        border: 2px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        text-align: center !important;
    }
    
    /* Metrik Değerlerini Ortala */
    div[data-testid="stMetricValue"] > div { justify-content: center !important; }
    div[data-testid="stMetricLabel"] > div { justify-content: center !important; }

    .nitelik-box {
        display: flex;
        justify-content: space-around;
        margin-bottom: 25px;
    }
    .n-item { flex: 1; }
    .n-label { color: #ffffff; font-size: 0.85rem; display: block; margin-bottom: 5px; opacity: 0.8; }
    .n-value { color: #ffc300; font-weight: bold; font-size: 1.4rem; }
    
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    
    /* Karar Renkleri */
    .onay { color: #2ecc71; font-weight: bold; }
    .ret { color: #e74c3c; font-weight: bold; }
    .duzeltme { color: #f39c12; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETİ: KARAR DETAYLARI (143 Karar Analizi) ---
# verilerine göre güncellendi.
karar_ozet = {
    "ONAY": 83,
    "DÜZELTME": 52,
    "KAEK": 3,
    "GÖRÜŞ": 2,
    "RET": 2,
    "KAPSAM DIŞI": 1,
    "GERİ ÇEKİLDİ": 0 # Gelecekte eklenebilir
}

# --- VERİ SETİ: RAPORTÖRLER (Süreç Takibi Eklenmiş) ---
# ve yeni talepler doğrultusunda genişletildi.
raportor_data = {
    "Dr. Öğr. Üyesi Müge DEMİR": {
        "Atanan": 31, 
        "Detay": {"ONAY": 18, "DÜZELTME": 11, "KAEK": 2, "RET": 0, "KAPSAM DIŞI": 0},
        "Gecmis": ["📁 Dosya #2026-04: Düzeltme → ONAY", "📁 Dosya #2026-11: Direkt ONAY"]
    },
    "Doç. Dr. Kübra AYKAÇ": {
        "Atanan": 30, 
        "Detay": {"ONAY": 14, "DÜZELTME": 9, "KAEK": 0, "RET": 2, "KAPSAM DIŞI": 1},
        "Gecmis": ["📁 Dosya #2026-02: Ret (Kriter uymuyor)", "📁 Dosya #2026-09: Düzeltme Bekleniyor"]
    },
    # Diğer 10 raportör bu yapıya göre listelenir...
}

# --- ARAYÜZ ---
st.markdown("<h1 style='text-align: center;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>SBA 2026 Karar Destek Paneli</h3>", unsafe_allow_html=True)

# 1. ORTALI ANA METRİKLER
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# 2. SARI ÇERÇEVELİ NİTELİK PANELİ
st.markdown(f"""
    <div class="nitelik-box">
        <div class="n-item"><span class="n-label">Bireysel</span><span class="n-value">128</span></div>
        <div class="n-item"><span class="n-label">Uzmanlık</span><span class="n-value">48</span></div>
        <div class="n-item"><span class="n-label">Y. Lisans</span><span class="n-value">10</span></div>
        <div class="n-item"><span class="n-label">Doktora</span><span class="n-value">4</span></div>
    </div>
""", unsafe_allow_html=True)

# 3. SEKMELER
tab1, tab2, tab3 = st.tabs(["👥 Raportörler & Süreç", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.write("#### 🔍 Raportör Karar ve Tarihçe Takibi")
    r_secim = st.selectbox("Raportör Seçiniz:", list(raportor_data.keys()))
    r = raportor_data[r_secim]
    
    toplam_karar = sum(r["Detay"].values())
    bekleyen = r["Atanan"] - toplam_karar
    
    colA, colB, colC = st.columns(3)
    colA.metric("Toplam Atanan", r["Atanan"])
    colB.metric("Toplam Karar", toplam_karar)
    colC.metric("Bekleyen ⏳", bekleyen)
    
    st.write("---")
    c_detay1, c_detay2 = st.columns(2)
    with c_detay1:
        st.write("##### 📊 Karar Dağılımı")
        for k, v in r["Detay"].items():
            st.write(f"**{k}:** {v}")
            st.progress(v / r["Atanan"] if r["Atanan"] > 0 else 0)
            
    with c_detay2:
        st.write("##### 🕒 Süreç Geçmişi (Düzeltme/Onay)")
        for log in r["Gecmis"]:
            st.info(log)

with tab2:
    st.write("#### 🏢 Birim Analizi (Tüm Kararlar Dahil)")
    # verilerine dayalı birim listesi burada devam eder...
    st.info("İç Hastalıkları Anabilim Dalı: 27 Dosya")

with tab3:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü")
    # yapısı korunarak listelenir.
    st.info("Prof. Dr. Meltem Gülhan HALİL: 6 Dosya")

st.write("---")
st.markdown("<center style='color:#666;'>Devrim Süreklidir ✊ — Hacettepe SBA 2026</center>", unsafe_allow_html=True)
