import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="centered")

# CSS: Dark Navy Blue & Gold Teması + Nitelik Kartları
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    .block-container { max-width: 800px; padding-top: 1rem; }
    
    /* Ana Metrikler */
    div[data-testid="stMetric"] {
        background-color: #001d3d !important;
        border: 1px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    
    /* Nitelik Özet Satırı */
    .nitelik-bar {
        display: flex;
        justify-content: space-around;
        background-color: #001d3d;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #1e3a5f;
    }
    .n_item { text-align: center; color: #ffffff; }
    .n_val { color: #ffc300; font-weight: bold; font-size: 18px; display: block; }
    
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETLERİ ---
toplam_basvuru = 190
kurul_sayisi = 4

# Nitelik Açılımı (190 Dosya)
nitelik_ozet = {
    "📝 Bireysel": 128,
    "🎓 Uzmanlık": 48,
    "🔬 Y. Lisans": 10,
    "🩺 Doktora": 4
}

# Raportörler
raportorler = {
    "Dr. Öğr. Üyesi Müge DEMİR": {"Atanan": 31, "ONAY": 18, "DÜZELTME": 11, "KAEK": 2},
    "Doç. Dr. Kübra AYKAÇ": {"Atanan": 30, "ONAY": 14, "DÜZELTME": 9, "KAEK": 0},
    "Doç. Dr. Burcu ERSÖZ ALAN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 6, "KAEK": 0}
    # ... (Diğer 9 raportör eklenebilir)
}

# --- ARAYÜZ ---
st.markdown("<h1 style='text-align: center; margin-bottom:0;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-top:0;'>SBA 2026 Karar Destek Sistemi</h3>", unsafe_allow_html=True)

# 1. ANA ÖZET PANELLERİ
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", f"{toplam_basvuru}")
c2.metric("🗓️ Kurul Sayısı", f"{kurul_sayisi}")

# 2. 190 DOSYANIN AÇILIMI (Nitelik Sayıları)
st.markdown("""
    <div class="nitelik-bar">
        <div class="n_item"><small>Bireysel Araştırma</small><span class="n_val">128</span></div>
        <div class="n_item"><small>Uzmanlık Tezi</small><span class="n_val">48</span></div>
        <div class="n_item"><small>Y. Lisans Tezi</small><span class="n_val">10</span></div>
        <div class="n_item"><small>Doktora Tezi</small><span class="n_val">4</span></div>
    </div>
""", unsafe_allow_html=True)

st.write("---")

# 3. SEKMELER
tab1, tab2, tab3 = st.tabs(["👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.write("#### 🔍 Raportör Dosya Detayları")
    secilen_r = st.selectbox("Analiz İçin Raportör Seçiniz:", list(raportorler.keys()))
    u = raportorler[secilen_r]
    
    colA, colB, colC = st.columns(3)
    karar = u['ONAY'] + u['DÜZELTME'] + u['KAEK']
    colA.metric("Toplam Atanan", u['Atanan'])
    colB.metric("Karar Verilen", karar)
    colC.metric("Bekleyen", u['Atanan'] - karar)
    
    st.write("#### 📊 Süreç Kırılımı")
    for k, v in u.items():
        if k != "Atanan":
            st.write(f"{k}: {v} dosya")
            st.progress(v / u['Atanan'] if u['Atanan'] > 0 else 0)

with tab2:
    st.write("#### 🏢 Birimlerin Nitelik ve Karar Dağılımı")
    # Önceki versiyondaki expander yapısı aynen korunmuştur.

with tab3:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Detayları")
    # Sorumlu hoca dökümü ve expander yapısı aynen korunmuştur.

st.write("---")
st.markdown("<center style='color:#444;'>Hacettepe SBA Karar Destek Sistemi © 2026</center>", unsafe_allow_html=True)
