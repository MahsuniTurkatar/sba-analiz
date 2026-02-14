import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: GOLD DÜZEN (SABİT) ---
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
    .nitelik-box { display: flex; justify-content: space-around; margin-bottom: 25px; }
    .n-item { flex: 1; text-align: center; }
    .n-value { color: #ffc300; font-weight: bold; font-size: 1.4rem; }
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. VERİ SETİ: ÜYE_1 EXCEL TAM VERİLERİ ---
raportor_data = {
    "Adı Soyadı": [
        "Prof. Dr. Ayşe Nurten AKARSU", "Prof. Dr. M. Özgür UYANIK", "Prof. Dr. Melih Önder BABAOĞLU",
        "Prof. Dr. Ayşe KİN İŞLER", "Prof. Dr. Yavuz AYHAN", "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY",
        "Prof. Dr. Gözde GİRGİN", "Doç. Dr. Kübra AYKAÇ", "Doç. Dr. Tolga ÇAKMAK",
        "Doç. Dr. Burcu ERSÖZ ALAN", "Doç. Dr. Ekim GÜMELER", "Dr. Öğr. Üyesi Müge DEMİR"
    ],
    "Dosya Sayısı": [31, 35, 28, 25, 25, 36, 36, 38, 25, 36, 26, 39],
    "Onay": [11, 17, 12, 12, 9, 17, 18, 14, 9, 18, 11, 18],
    "Düzeltme": [11, 7, 13, 3, 8, 8, 9, 15, 5, 10, 4, 11],
    "KAEK": [0, 1, 0, 2, 0, 1, 0, 1, 1, 0, 1, 2],
    "Görüş": [0, 1, 1, 2, 0, 1, 1, 0, 1, 0, 0, 0],
    "Kapsam Dışı": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    "Geri Çekildi": [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Bireysel": [18, 15, 18, 14, 11, 19, 20, 23, 7, 19, 14, 20],
    "Uzmanlık": [9, 9, 6, 1, 5, 7, 5, 5, 4, 6, 2, 6]
}
df = pd.DataFrame(raportor_data)

# --- ARAYÜZ ÜST KISIM ---
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

# 1. GENEL DURUM (RESİM OLARAK)
with tab_genel:
    st.write("#### 📋 Kurul Üye_1 Detaylı Karar Çizelgesi")
    # Hocam buraya senin yüklediğin tablo resmini direkt basıyoruz
    st.image("image_4b8c07.png", caption="Üye_1 Genel Veri Tablosu", use_column_width=True)
    st.download_button(
        label="📥 Tabloyu Excel Olarak İndir",
        data=df.to_csv().encode('utf-8-sig'),
        file_name='SBA_Genel_Durum.csv', mime='text/csv'
    )

# 2. RAPORTÖR ANALİZİ (Eksiksiz Veri)
with tab_raportor:
    st.write("#### 🔍 Raportör Dosya Detayları")
    r_secim = st.selectbox("Analiz İçin Raportör Seçiniz:", df["Adı Soyadı"].tolist())
    r = df[df["Adı Soyadı"] == r_secim].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam Atanan", r["Dosya Sayısı"])
    col2.metric("Karar Verilen", r["Onay"] + r["Düzeltme"])
    col3.metric("Bekleyen", r["Dosya Sayısı"] - (r["Onay"] + r["Düzeltme"]))
    
    st.write("---")
    # Tüm Karar Tipleri
    cols = st.columns(2)
    cols[0].write(f"✅ ONAY: {r['Onay']}")
    cols[0].progress(int(r['Onay']/r['Dosya Sayısı']*100) if r['Dosya Sayısı']>0 else 0)
    cols[1].write(f"⚠️ DÜZELTME: {r['Düzeltme']}")
    cols[1].progress(int(r['Düzeltme']/r['Dosya Sayısı']*100) if r['Dosya Sayısı']>0 else 0)
    
    st.write(f"📂 KAEK: {r['KAEK']} | 📝 GÖRÜŞ: {r['Görüş']} | 🚫 KAPSAM DIŞI: {r['Kapsam Dışı']} | 🔄 GERİ ÇEKİLDİ: {r['Geri Çekildi']}")

# 3. BİRİM ANALİZİ
with tab_birim:
    st.write("#### 🏢 Birimlerin Nitelik Dağılımı")
    birimler = [
        {"Ad": "İç Hastalıkları A.D.", "Toplam": 27, "B": 20, "U": 7},
        {"Ad": "Çocuk Sağlığı A.D.", "Toplam": 23, "B": 11, "U": 12},
        {"Ad": "Kadın Hastalıkları A.D.", "Toplam": 9, "B": 7, "U": 2},
        {"Ad": "Klinik Eczacılık A.D.", "Toplam": 9, "B": 9, "U": 0},
        {"Ad": "Göğüs Hastalıkları A.D.", "Toplam": 9, "B": 6, "U": 3}
    ]
    for b in birimler:
        with st.expander(f"{b['Ad']} ({b['Toplam']} Dosya)"):
            st.write(f"Bireysel: {b['B']} | Uzmanlık: {b['U']}")

# 4. SORUMLU ANALİZİ (İLK 5 VE DOĞRU VERİ)
with tab_sorumlu:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü (İlk 5)")
    sorumlular = {
        "Prof. Dr. Meltem Gülhan HALİL": {"Dosya": 6, "B": 4, "U": 2, "Birim": "İç Hastalıkları A.D."},
        "Prof. Dr. Yasemin ÖZSÜREKCİ": {"Dosya": 5, "B": 2, "U": 3, "Birim": "Çocuk Sağlığı A.D."},
        "Dr. Öğr. Üyesi Gonca ÖZTEN": {"Dosya": 4, "B": 4, "U": 0, "Birim": "Klinik Eczacılık A.D."},
        "Doç. Dr. Süleyman Nahit ŞENDUR": {"Dosya": 4, "B": 3, "U": 1, "Birim": "İç Hastalıkları A.D."},
        "Prof. Dr. Ali Fuat KALYONCU": {"Dosya": 4, "B": 4, "U": 0, "Birim": "Göğüs Hastalıkları A.D."}
    }
    s_hoca = st.selectbox("Hoca Seçiniz:", list(sorumlular.keys()))
    s_verisi = sorumlular[s_hoca]
    
    st.metric(f"{s_verisi['Dosya']} Dosya", s_verisi['Birim'])
    st.info(f"📊 Bireysel: {s_verisi['B']} | Uzmanlık: {s_verisi['U']}")

st.write("---")
st.markdown("<center style='color:#666;'>Sağlık Bilimleri Etik Kurulu © 2026 ✊</center>", unsafe_allow_html=True)
