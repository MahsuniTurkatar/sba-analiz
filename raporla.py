import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="centered")

# Dark Navy Blue & Hacettepe Gold Teması
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    .block-container { max-width: 800px; padding-top: 2rem; }
    
    /* Metrik Kartları */
    div[data-testid="stMetric"] {
        background-color: #001d3d !important;
        border: 1px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    
    /* Nitelik ve Veri Kartları */
    .data-card {
        background-color: #001d3d;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffc300;
        margin-bottom: 10px;
    }
    
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    .rank-num { color: #ffc300; font-weight: bold; font-size: 20px; margin-right: 12px; }
    </style>
    """, unsafe_allow_html=True)

# Kurumsal Başlık
st.markdown("<h1 style='text-align: center;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>SBA 2026 Karar Destek Sistemi</h3>", unsafe_allow_html=True)

# --- VERİ SETİ: RAPORTÖRLER (Eksiksiz) ---
raportorler = {
    "Dr. Öğr. Üyesi Müge DEMİR": {"Atanan": 31, "ONAY": 18, "DÜZELTME": 11, "KAEK": 2},
    "Doç. Dr. Kübra AYKAÇ": {"Atanan": 30, "ONAY": 14, "DÜZELTME": 9, "KAEK": 0},
    "Doç. Dr. Burcu ERSÖZ ALAN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 6, "KAEK": 0},
    "Prof. Dr. Gözde GİRGİN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 5, "KAEK": 0},
    "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY": {"Atanan": 28, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1},
    "Prof. Dr. Melih Önder BABAOĞLU": {"Atanan": 28, "ONAY": 12, "DÜZELTME": 8, "KAEK": 0},
    "Prof. Dr. M. Özgür UYANIK": {"Atanan": 27, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1},
    "Prof. Dr. Ayşe Nurten AKARSU": {"Atanan": 22, "ONAY": 11, "DÜZELTME": 4, "KAEK": 0},
    "Doç. Dr. Ekim GÜMELER": {"Atanan": 17, "ONAY": 11, "DÜZELTME": 4, "KAEK": 1},
    "Prof. Dr. Yavuz AYHAN": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 8, "KAEK": 0},
    "Doç. Dr. Tolga ÇAKMAK": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 5, "KAEK": 1},
    "Prof. Dr. Ayşe KİN İŞLER": {"Atanan": 17, "ONAY": 12, "DÜZELTME": 3, "KAEK": 2}
}

# --- VERİ SETİ: SORUMLU NİTELİKLERİ ---
sorumlu_detay = {
    "Prof. Dr. Meltem Gülhan HALİL": {"Birim": "İç Hastalıkları A.D.", "Toplam": 6, "Uzmanlık Tezi": 2, "Bireysel Araştırma": 4},
    "Prof. Dr. Yasemin ÖZSÜREKCİ": {"Birim": "Çocuk Sağlığı ve Hastalıkları A.D.", "Toplam": 5, "Uzmanlık Tezi": 3, "Bireysel Araştırma": 2},
    "Dr. Öğr. Üyesi Gonca ÖZTEN": {"Birim": "Klinik Eczacılık A.D.", "Toplam": 4, "Uzmanlık Tezi": 0, "Bireysel Araştırma": 4}
}

# --- VERİ SETİ: BİRİM İLK 5 ---
ilk_5_birim = [
    {"Birim": "İç Hastalıkları Anabilim Dalı", "Sayi": 27, "Bireysel": 20, "Uzmanlık": 7},
    {"Birim": "Çocuk Sağlığı ve Hastalıkları A.D.", "Sayi": 23, "Bireysel": 11, "Uzmanlık": 12},
    {"Birim": "Kadın Hastalıkları ve Doğum A.D.", "Sayi": 9, "Bireysel": 7, "Uzmanlık": 2},
    {"Birim": "Klinik Eczacılık Anabilim Dalı", "Sayi": 9, "Bireysel": 6, "Uzmanlık": 3},
    {"Birim": "Göğüs Hastalıkları Anabilim Dalı", "Sayi": 9, "Bireysel": 8, "Uzmanlık": 1}
]

st.write("---")

# 4 ANA SEKME (Raportörleri başa aldım!)
tab1, tab2, tab3 = st.tabs(["👥 Raportör Analizi", "🏢 Birim & Nitelik", "👨‍🏫 Sorumlu & Nitelik"])

with tab1:
    secilen_r = st.selectbox("Analiz İçin Raportör Seçiniz:", list(raportorler.keys()))
    u = raportorler[secilen_r]
    c1, c2, c3 = st.columns(3)
    karar = u['ONAY'] + u['DÜZELTME'] + u['KAEK']
    c1.metric("Toplam Atanan", f"{u['Atanan']}")
    c2.metric("Karar Verilen", f"{karar}")
    c3.metric("Bekleyen", f"{u['Atanan'] - karar}")
    
    st.write("#### 📊 Süreç Kırılımı")
    for k, v in u.items():
        if k != "Atanan":
            st.write(f"{k}: {v}")
            st.progress(v / u['Atanan'] if u['Atanan'] > 0 else 0)

with tab2:
    st.write("#### 🏢 Birimlerin Nitelik Dağılımı")
    for i, b in enumerate(ilk_5_birim, 1):
        with st.expander(f"#{i} {b['Birim']} ({b['Sayi']} Dosya)"):
            st.write(f"✅ Bireysel Araştırma: {b['Bireysel']}")
            st.write(f"🎓 Uzmanlık Tezi: {b['Uzmanlık']}")
            st.progress(b['Bireysel'] / b['Sayi'])

with tab3:
    secilen_s = st.selectbox("Sorumlu Hocayı Seçiniz:", list(sorumlu_detay.keys()))
    s = sorumlu_detay[secilen_s]
    st.metric(f"{secilen_s}", f"{s['Toplam']} Dosya")
    st.markdown(f"""
        <div class="data-card">
            <b>Birim:</b> {s['Birim']}<br>
            <b>Bireysel Araştırma:</b> {s['Bireysel Araştırma']}<br>
            <b>Uzmanlık Tezi:</b> {s['Uzmanlık Tezi']}
        </div>
    """, unsafe_allow_html=True)

st.write("---")
st.markdown("<center style='color:#444;'>Hacettepe SBA Karar Destek Sistemi © 2026</center>", unsafe_allow_html=True)
