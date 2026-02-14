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

# --- 1. VERİ SETLERİ (TAM LİSTE - 12 RAPORTÖR) ---
raportor_verileri = {
    "Raportör Adı": [
        "Dr. Öğr. Üyesi Müge DEMİR", "Doç. Dr. Kübra AYKAÇ", "Doç. Dr. Burcu ERSÖZ ALAN",
        "Prof. Dr. Gözde GİRGİN", "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY", "Prof. Dr. Melih Önder BABAOĞLU",
        "Prof. Dr. M. Özgür UYANIK", "Prof. Dr. Ayşe Nurten AKARSU", "Doç. Dr. Ekim GÜMELER",
        "Prof. Dr. Yavuz AYHAN", "Doç. Dr. Tolga ÇAKMAK", "Prof. Dr. Ayşe KİN İŞLER"
    ],
    "Atanan": [31, 30, 28, 28, 28, 28, 27, 22, 17, 17, 17, 17],
    "ONAY": [18, 14, 18, 18, 17, 12, 17, 11, 11, 9, 9, 12],
    "DÜZELTME": [11, 9, 6, 5, 4, 8, 4, 4, 4, 8, 5, 3],
    "KAEK": [2, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 2],
    "GÖRÜŞ": [0, 0, 0, 5, 6, 8, 5, 7, 1, 0, 2, 0],
    "RET": [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "K.DIŞI": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "G.ÇEKİLDİ": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
df_uye1 = pd.DataFrame(raportor_verileri)

# Birimler (İlk 5 - Nitelikli)
birim_ilk5 = [
    {"Ad": "İç Hastalıkları Anabilim Dalı", "Dosya": 27, "Bireysel": 20, "Uzmanlık": 7},
    {"Ad": "Çocuk Sağlığı ve Hastalıkları A.D.", "Dosya": 23, "Bireysel": 11, "Uzmanlık": 12},
    {"Ad": "Kadın Hastalıkları ve Doğum A.D.", "Dosya": 9, "Bireysel": 7, "Uzmanlık": 2},
    {"Ad": "Klinik Eczacılık Anabilim Dalı", "Dosya": 9, "Bireysel": 9, "Uzmanlık": 0},
    {"Ad": "Göğüs Hastalıkları Anabilim Dalı", "Dosya": 9, "Bireysel": 6, "Uzmanlık": 3}
]

# Sorumlular (İlk 5 - Nitelikli)
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

# 1. ORTALI ANA METRİKLER
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# 2. SARI ÇERÇEVELİ NİTELİK PANELİ
st.markdown("""
    <div class="nitelik-box">
        <div class="n-item"><span>Bireysel</span><br><span class="n-value">128</span></div>
        <div class="n-item"><span>Uzmanlık</span><br><span class="n-value">48</span></div>
        <div class="n-item"><span>Y. Lisans</span><br><span class="n-value">10</span></div>
        <div class="n-item"><span>Doktora</span><br><span class="n-value">4</span></div>
    </div>
""", unsafe_allow_html=True)

# 3. SEKMELER
tab_excel, tab_birim, tab_sorumlu = st.tabs(["📄 Üye_1 (Genel Tablo - Excel)", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab_excel:
    st.write("#### 📋 Genel Veri İzleme Tablosu (Excel Görünümü)")
    # Excel stili tablo
    st.dataframe(df_uye1, use_container_width=True, hide_index=True)
    
    # PDF/Excel Aktarma Butonu
    st.download_button(
        label="📥 Tabloyu PDF/Excel Olarak Kaydet",
        data=df_uye1.to_csv().encode('utf-8-sig'),
        file_name='Hacettepe_SBA_Genel_Tablo.csv',
        mime='text/csv',
    )

with tab_birim:
    st.write("#### 🏢 En Çok Dosya Gönderen İlk 5 Birim")
    for b in birim_ilk5:
        with st.expander(f"{b['Ad']} ({b['Dosya']} Dosya)"):
            st.write(f"📝 Bireysel: {b['Bireysel']} | 🎓 Uzmanlık: {b['Uzmanlık']}")
            st.progress(b['Bireysel'] / b['Dosya'])

with tab_sorumlu:
    st.write("#### 👨‍🏫 En Çok Dosyası Olan İlk 5 Sorumlu Araştırmacı")
    for s in sorumlu_ilk5:
        with st.expander(f"{s['Ad']} ({s['Dosya']} Dosya)"):
            st.write(f"📄 Bireysel: {s['Bireysel']} | 🎓 Uzmanlık: {s['Uzmanlık']}")
            st.progress(s['Bireysel'] / s['Dosya'])

st.write("---")
st.markdown("<center style='color:#666;'>Mahsuni Hoca Özel Versiyon - 2026 ✊</center>", unsafe_allow_html=True)
