import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: GOLD DÜZEN & MERKEZİ HİZALAMA ---
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

# --- 1. VERİ SETLERİ (TAM LİSTE) ---

#
raportor_listesi = {
    "Dr. Öğr. Üyesi Müge DEMİR": {"Atanan": 31, "ONAY": 18, "DÜZELTME": 11, "KAEK": 2, "GÖRÜŞ": 0, "RET": 0, "K.DIŞI": 0},
    "Doç. Dr. Kübra AYKAÇ": {"Atanan": 30, "ONAY": 14, "DÜZELTME": 9, "KAEK": 0, "GÖRÜŞ": 0, "RET": 2, "K.DIŞI": 1},
    "Doç. Dr. Burcu ERSÖZ ALAN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 6, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0, "K.DIŞI": 0},
    "Prof. Dr. Gözde GİRGİN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 5, "KAEK": 0, "GÖRÜŞ": 5, "RET": 0, "K.DIŞI": 0},
    "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY": {"Atanan": 28, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 6, "RET": 0, "K.DIŞI": 0},
    "Prof. Dr. Melih Önder BABAOĞLU": {"Atanan": 28, "ONAY": 12, "DÜZELTME": 8, "KAEK": 0, "GÖRÜŞ": 8, "RET": 0, "K.DIŞI": 0},
    "Prof. Dr. M. Özgür UYANIK": {"Atanan": 27, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 5, "RET": 0, "K.DIŞI": 0},
    "Prof. Dr. Ayşe Nurten AKARSU": {"Atanan": 22, "ONAY": 11, "DÜZELTME": 4, "KAEK": 0, "GÖRÜŞ": 7, "RET": 0, "K.DIŞI": 0},
    "Doç. Dr. Ekim GÜMELER": {"Atanan": 17, "ONAY": 11, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0, "K.DIŞI": 0},
    "Prof. Dr. Yavuz AYHAN": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 8, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0, "K.DIŞI": 0},
    "Doç. Dr. Tolga ÇAKMAK": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 5, "KAEK": 1, "GÖRÜŞ": 2, "RET": 0, "K.DIŞI": 0},
    "Prof. Dr. Ayşe KİN İŞLER": {"Atanan": 17, "ONAY": 12, "DÜZELTME": 3, "KAEK": 2, "GÖRÜŞ": 0, "RET": 0, "K.DIŞI": 0}
}

# İlk 5 Birim
birim_ilk5 = [
    {"Ad": "İç Hastalıkları Anabilim Dalı", "Dosya": 27, "Bireysel": 20, "Uzmanlık": 7},
    {"Ad": "Çocuk Sağlığı ve Hastalıkları A.D.", "Dosya": 23, "Bireysel": 11, "Uzmanlık": 12},
    {"Ad": "Kadın Hastalıkları ve Doğum A.D.", "Dosya": 9, "Bireysel": 7, "Uzmanlık": 2},
    {"Ad": "Klinik Eczacılık Anabilim Dalı", "Dosya": 9, "Bireysel": 9, "Uzmanlık": 0},
    {"Ad": "Göğüs Hastalıkları Anabilim Dalı", "Dosya": 9, "Bireysel": 6, "Uzmanlık": 3}
]

# İlk 5 Sorumlu
sorumlu_ilk5 = [
    {"Ad": "Prof. Dr. Meltem Gülhan HALİL", "Dosya": 6, "Bireysel": 4, "Uzmanlık": 2},
    {"Ad": "Prof. Dr. Yasemin ÖZSÜREKCİ", "Dosya": 5, "Bireysel": 2, "Uzmanlık": 3},
    {"Ad": "Dr. Öğr. Üyesi Gonca ÖZTEN", "Dosya": 4, "Bireysel": 4, "Uzmanlık": 0},
    {"Ad": "Doç. Dr. Süleyman Nahit ŞENDUR", "Dosya": 4, "Bireysel": 3, "Uzmanlık": 1},
    {"Ad": "Prof. Dr. Ali Fuat KALYONCU", "Dosya": 4, "Bireysel": 4, "Uzmanlık": 0}
]

# --- ARAYÜZ ---
st.markdown("<h1 style='text-align: center;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>SBA 2026 Karar Destek Paneli</h3>", unsafe_allow_html=True)

# ÜST PANEL: ORTALI METRİKLER & SARI NİTELİK
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

st.markdown(f"""
    <div class="nitelik-box">
        <div class="n-item"><span>Bireysel</span><br><span class="n-value">128</span></div>
        <div class="n-item"><span>Uzmanlık</span><br><span class="n-value">48</span></div>
        <div class="n-item"><span>Y. Lisans</span><br><span class="n-value">10</span></div>
        <div class="n-item"><span>Doktora</span><br><span class="n-value">4</span></div>
    </div>
""", unsafe_allow_html=True)

# SEKMELER
tab_ana, tab1, tab2, tab3 = st.tabs(["📄 Üye_1 (Genel Tablo)", "👥 Raportörler", "🏢 İlk 5 Birim", "👨‍🏫 İlk 5 Sorumlu"])

# --- ÜYE_1 SAYFASI (GENEL TABLO) ---
with tab_ana:
    st.write("### 📋 Genel Karar ve İşlem Tablosu")
    df_genel = pd.DataFrame.from_dict(raportor_listesi, orient='index')
    st.dataframe(df_genel, use_container_width=True)
    
    # PDF Aktarma (Simülasyon/CSV aktarma butonu - Streamlit standartı)
    st.download_button(label="📥 Üye_1 Tablosunu PDF/CSV Olarak Aktar", 
                       data=df_genel.to_csv(), 
                       file_name='uye_1_genel_tablo.csv', mime='text/csv')

# --- RAPORTÖRLER (12 KİŞİ) ---
with tab1:
    st.write("### 🔍 Raportör Karar ve Bekleyen Analizi")
    r_secim = st.selectbox("Raportör Seçiniz:", list(raportor_listesi.keys()))
    r = raportor_listesi[r_secim]
    
    # Ortalı Metrikler
    m1, m2, m3 = st.columns(3)
    karar_verilen = sum([v for k,v in r.items() if k != "Atanan"])
    m1.metric("Atanan", r["Atanan"])
    m2.metric("Karar Verilen", karar_verilen)
    m3.metric("Bekleyen ⏳", r["Atanan"] - karar_verilen)
    
    # Detaylı Dağılım
    st.write("---")
    cols = st.columns(3)
    cols[0].write(f"✅ ONAY: {r['ONAY']}")
    cols[0].write(f"⚠️ DÜZELTME: {r['DÜZELTME']}")
    cols[1].write(f"📊 KAEK: {r['KAEK']}")
    cols[1].write(f"💬 GÖRÜŞ: {r['GÖRÜŞ']}")
    cols[2].write(f"❌ RET: {r['RET']}")
    cols[2].write(f"🚫 KAPSAM DIŞI: {r['K.DIŞI']}")

# --- İLK 5 BİRİM ---
with tab2:
    st.write("### 🏢 En Çok Dosya Gönderen İlk 5 Birim (Nitelikli)")
    for b in birim_ilk5:
        with st.expander(f"{b['Ad']} — {b['Dosya']} Dosya"):
            st.write(f"📝 Bireysel Araştırma: {b['Bireysel']}")
            st.write(f"🎓 Uzmanlık Tezi: {b['Uzmanlık']}")
            st.progress(b['Bireysel'] / b['Dosya'])

# --- İLK 5 SORUMLU ---
with tab3:
    st.write("### 👨‍🏫 En Çok Dosyası Olan İlk 5 Sorumlu Araştırmacı")
    for s in sorumlu_ilk5:
        with st.expander(f"{s['Ad']} — {s['Dosya']} Dosya"):
            st.write(f"📄 Bireysel Araştırma: {s['Bireysel']}")
            st.write(f"🎓 Uzmanlık Tezi: {s['Uzmanlık']}")
            st.progress(s['Bireysel'] / s['Dosya'])

st.write("---")
st.markdown("<center style='color:#666;'>Görüşmek Üzere Hocam! ✊</center>", unsafe_allow_html=True)
