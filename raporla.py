import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: GOLD DÜZEN & MERKEZİ HİZALAMA (SABİT) ---
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

# --- 1. VERİ SETİ: EXCEL GENEL TABLO (Üye_1) ---
# Excel'deki hiyerarşik yapıyı (Bireysel, Y.Lisans, Doktora, Uzmanlık) koruyan özet tablo
genel_tablo_data = {
    "Adı Soyadı": [
        "Prof. Dr. Ayşe Nurten AKARSU", "Prof. Dr. M. Özgür UYANIK", "Prof. Dr. Melih Önder BABAOĞLU",
        "Prof. Dr. Ayşe KİN İŞLER", "Prof. Dr. Yavuz AYHAN", "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY",
        "Prof. Dr. Gözde GİRGİN", "Doç. Dr. Kübra AYKAÇ", "Doç. Dr. Tolga ÇAKMAK",
        "Doç. Dr. Burcu ERSÖZ ALAN", "Doç. Dr. Ekim GÜMELER", "Dr. Öğr. Üyesi Müge DEMİR"
    ],
    "Toplam Atanan": [22, 26, 27, 17, 17, 27, 28, 30, 16, 28, 17, 31],
    "Onay": [11, 17, 12, 12, 9, 17, 18, 14, 9, 18, 11, 18],
    "Düzeltme": [11, 7, 13, 3, 8, 8, 9, 15, 5, 10, 4, 11],
    "KAEK": [0, 1, 0, 2, 0, 1, 0, 1, 1, 0, 1, 2],
    "Görüş": [0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0]
}
df_genel = pd.DataFrame(genel_tablo_data)

# --- 2. BİRİM & SORUMLU VERİLERİ (İLK 5) ---
birim_ilk5 = [
    {"Ad": "İç Hastalıkları Anabilim Dalı", "Dosya": 27, "Bireysel": 20, "Uzmanlık": 7},
    {"Ad": "Çocuk Sağlığı ve Hastalıkları A.D.", "Dosya": 23, "Bireysel": 11, "Uzmanlık": 12},
    {"Ad": "Kadın Hastalıkları ve Doğum A.D.", "Dosya": 9, "Bireysel": 7, "Uzmanlık": 2},
    {"Ad": "Klinik Eczacılık Anabilim Dalı", "Dosya": 9, "Bireysel": 9, "Uzmanlık": 0},
    {"Ad": "Göğüs Hastalıkları Anabilim Dalı", "Dosya": 9, "Bireysel": 6, "Uzmanlık": 3}
]

# --- ARAYÜZ ---
st.markdown("<h1 style='text-align: center;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h3>", unsafe_allow_html=True)

# ANA METRİKLER
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# NİTELİK PANELİ
st.markdown("""
    <div class="nitelik-box">
        <div class="n-item"><span>Bireysel Araştırma</span><br><span class="n-value">128</span></div>
        <div class="n-item"><span>Uzmanlık Tezi</span><br><span class="n-value">48</span></div>
        <div class="n-item"><span>Y. Lisans Tezi</span><br><span class="n-value">10</span></div>
        <div class="n-item"><span>Doktora Tezi</span><br><span class="n-value">4</span></div>
    </div>
""", unsafe_allow_html=True)

# SEKMELER
tab_genel, tab_raportor, tab_birim, tab_sorumlu = st.tabs([
    "📊 Genel Durum", "👥 Raportör Analizi", "🏢 Birim & Nitelik", "👨‍🏫 Sorumlu & Nitelik"
])

# 1. GENEL DURUM (Excel Stili PDF Aktarım Odaklı)
with tab_genel:
    st.write("#### 📋 Kurul Genel Karar Çizelgesi (Üye_1)")
    st.dataframe(df_genel, use_container_width=True, hide_index=True)
    st.download_button(
        label="📥 Genel Tabloyu PDF/Excel Olarak Dışa Aktar",
        data=df_genel.to_csv().encode('utf-8-sig'),
        file_name='SBA_Genel_Durum_Tablosu.csv',
        mime='text/csv'
    )

# 2. RAPORTÖR ANALİZİ (Görsel Kırılım)
with tab_raportor:
    st.write("#### 🔍 Raportör Dosya Detayları")
    r_secim = st.selectbox("Analiz İçin Raportör Seçiniz:", df_genel["Adı Soyadı"].tolist())
    r_data = df_genel[df_genel["Adı Soyadı"] == r_secim].iloc[0]
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Toplam Atanan", r_data["Toplam Atanan"])
    m2.metric("Karar Verilen", r_data["Onay"] + r_data["Düzeltme"])
    m3.metric("Bekleyen", r_data["Toplam Atanan"] - (r_data["Onay"] + r_data["Düzeltme"]))
    
    st.write("---")
    st.write(f"✅ ONAY: {r_data['Onay']}")
    st.progress(int(r_data['Onay'] / r_data['Toplam Atanan'] * 100))
    st.write(f"⚠️ DÜZELTME: {r_data['Düzeltme']}")
    st.progress(int(r_data['Düzeltme'] / r_data['Toplam Atanan'] * 100))

# 3. BİRİM & NİTELİK
with tab_birim:
    st.write("#### 🏢 Birimlerin Nitelik Dağılımı")
    for b in birim_ilk5:
        with st.expander(f"# {birim_ilk5.index(b)+1} {b['Ad']} ({b['Dosya']} Dosya)"):
            st.write(f"✅ Bireysel Araştırma: {b['Bireysel']}")
            st.write(f"🎓 Uzmanlık Tezi: {b['Uzmanlık']}")
            st.progress(b['Bireysel'] / b['Dosya'])

# 4. SORUMLU & NİTELİK
with tab_sorumlu:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü (İlk 5)")
    # image_49b686.png yapısı buraya sabitlendi
    st.info("Prof. Dr. Meltem Gülhan HALİL (6 Dosya) | Birim: İç Hastalıkları A.D.")
    st.info("Prof. Dr. Yasemin ÖZSÜREKCİ (5 Dosya) | Birim: Çocuk Sağlığı A.D.")

st.write("---")
st.markdown("<center style='color:#666;'>Hacettepe SBA Karar Destek Sistemi © 2026 ✊</center>", unsafe_allow_html=True)
