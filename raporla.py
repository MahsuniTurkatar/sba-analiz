import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: GOLD DÜZEN & SABİT TASARIM ---
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
    .n-value { color: #ffc300; font-weight: bold; font-size: 1.4rem; }
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. VERİ SETİ: ÜYE_1 TABLOSU (EKSİKSİZ) ---
data = {
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
    "Görüş": [0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    "Ret": [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    "Kapsam Dışı": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    "Geri Çekildi": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Bireysel": [18, 15, 18, 14, 11, 19, 20, 23, 7, 19, 14, 20],
    "Uzmanlık": [9, 9, 6, 1, 5, 7, 5, 5, 4, 6, 2, 6]
}
df = pd.DataFrame(data)

# --- ÜST PANEL ---
st.markdown("<h1 style='text-align: center;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h3>", unsafe_allow_html=True)

# ANA ÖZET
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

st.markdown(f"""
    <div style="display: flex; justify-content: space-around; background: #001d3d; border: 1px solid #ffc300; padding: 10px; border-radius: 10px; margin-bottom: 20px;">
        <div style="text-align:center;">Bireysel Araştırma<br><span class="n-value">128</span></div>
        <div style="text-align:center;">Uzmanlık Tezi<br><span class="n-value">48</span></div>
        <div style="text-align:center;">Y. Lisans Tezi<br><span class="n-value">10</span></div>
        <div style="text-align:center;">Doktora Tezi<br><span class="n-value">4</span></div>
    </div>
""", unsafe_allow_html=True)

# SEKMELER
tab1, tab2, tab3, tab4 = st.tabs(["📊 Genel Durum", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.write("#### 📋 Kurul Üye_1 Genel Karar Çizelgesi")
    # Resim yolu hatasını önlemek için base64 veya direkt tablo olarak basmak en güvenlisi ama resim istendi
    try:
        st.image("image_4b8c07.png", use_column_width=True)
    except:
        st.warning("Görsel yüklenemedi. Veriler 'Raportör Analizi' sekmesinde mevcuttur.")
    
    st.download_button("📥 Tabloyu Dışa Aktar (CSV)", df.to_csv().encode('utf-8-sig'), "SBA_Genel_Durum.csv")

with tab2:
    st.write("#### 🔍 Raportör Detaylı Karar Takibi")
    r_secim = st.selectbox("Raportör Seçiniz:", df["Adı Soyadı"].tolist())
    r = df[df["Adı Soyadı"] == r_secim].iloc[0]
    
    # Metrikler
    m1, m2, m3 = st.columns(3)
    m1.metric("Toplam Atanan", r["Dosya Sayısı"])
    m2.metric("Karar Verilen", r["Onay"] + r["Düzeltme"])
    m3.metric("Bekleyen", r["Dosya Sayısı"] - (r["Onay"] + r["Düzeltme"]))
    
    # Eksiksiz Karar Tipleri
    st.write(f"✅ **ONAY:** {r['Onay']} | ⚠️ **DÜZELTME:** {r['Düzeltme']}")
    st.write(f"📂 **KAEK:** {r['KAEK']} | 📝 **GÖRÜŞ:** {r['Görüş']} | ❌ **RET:** {r['Ret']}")
    st.write(f"🚫 **KAPSAM DIŞI:** {r['Kapsam Dışı']} | 🔄 **GERİ ÇEKİLDİ:** {r['Geri Çekildi']}")
    st.progress(int(r['Onay']/r['Dosya Sayısı']*100))

with tab3:
    st.write("#### 🏢 Birimlerin Nitelik Dağılımı")
    birimler = [
        {"Ad": "İç Hastalıkları A.D.", "T": 27, "B": 20, "U": 7},
        {"Ad": "Çocuk Sağlığı A.D.", "T": 23, "B": 11, "U": 12},
        {"Ad": "Kadın Hastalıkları A.D.", "T": 9, "B": 7, "U": 2},
        {"Ad": "Klinik Eczacılık A.D.", "T": 9, "B": 9, "U": 0},
        {"Ad": "Göğüs Hastalıkları A.D.", "T": 9, "B": 6, "U": 3}
    ]
    for b in birimler:
        with st.expander(f"{b['Ad']} ({b['T']} Dosya)"):
            st.write(f"Bireysel: {b['B']} | Uzmanlık: {b['U']}")

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü (İlk 5)")
    sorumlular = [
        {"Hoca": "Prof. Dr. Meltem Gülhan HALİL", "D": 6, "B": 4, "U": 2, "Birim": "İç Hastalıkları A.D."},
        {"Hoca": "Prof. Dr. Yasemin ÖZSÜREKCİ", "D": 5, "B": 2, "U": 3, "Birim": "Çocuk Sağlığı A.D."},
        {"Hoca": "Dr. Öğr. Üyesi Gonca ÖZTEN", "D": 4, "B": 4, "U": 0, "Birim": "Klinik Eczacılık A.D."},
        {"Hoca": "Doç. Dr. Süleyman Nahit ŞENDUR", "D": 4, "B": 3, "U": 1, "Birim": "İç Hastalıkları A.D."},
        {"Hoca": "Prof. Dr. Ali Fuat KALYONCU", "D": 4, "B": 4, "U": 0, "Birim": "Göğüs Hastalıkları A.D."}
    ]
    for s in sorumlular:
        with st.expander(f"{s['Hoca']} ({s['D']} Dosya)"):
            st.write(f"**Birim:** {s['Birim']}")
            st.write(f"📊 Bireysel: {s['B']} | Uzmanlık: {s['U']}")

st.write("---")
st.markdown("<center style='color:#666;'>Hacettepe SBA © 2026 ✊</center>", unsafe_allow_html=True)
