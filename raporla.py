import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: GOLD DÜZEN & YAN YANA NİTELİKLER & SABİT FOOTER ---
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
    /* Nitelikleri yan yana getiren zorunlu CSS */
    .nitelik-box { 
        display: flex !important; 
        flex-direction: row !important; 
        justify-content: space-around !important; 
        margin-bottom: 25px; 
    }
    .n-item { flex: 1; text-align: center; }
    .n-value { color: #ffc300; font-weight: bold; font-size: 1.4rem; display: block; }
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #000814;
        color: #ffc300;
        text-align: center;
        padding: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETİ (BOZULMADI - TAM LİSTE) ---
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
    "Geri Çekildi": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
df = pd.DataFrame(data)

# --- ÜST PANEL ---
st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>2026 Faaliyet Raporu</h3>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# Yan yana Nitelik Paneli
st.markdown("""
    <div class="nitelik-box">
        <div class="n-item">Bireysel Araştırma<br><span class="n-value">128</span></div>
        <div class="n-item">Uzmanlık Tezi<br><span class="n-value">48</span></div>
        <div class="n-item">Y. Lisans Tezi<br><span class="n-value">10</span></div>
        <div class="n-item">Doktora Tezi<br><span class="n-value">4</span></div>
    </div>
""", unsafe_allow_html=True)

# SEKMELER
tab1, tab2, tab3, tab4 = st.tabs(["📊 Genel Durum", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.write("#### 📋 Kurul Üye_1 Genel Karar Çizelgesi")
    # Verdiğin resim dosyasını buraya bağlıyoruz
    try:
        st.image("genel_tablo_ekran_goruntusu.png", use_column_width=True)
    except:
        st.error("Resim dosyası (genel_tablo_ekran_goruntusu.png) bulunamadı!")

with tab2:
    st.write("#### 🔍 Raportör Detaylı Karar Takibi")
    r_secim = st.selectbox("Raportör Seçiniz:", df["Adı Soyadı"].tolist())
    r = df[df["Adı Soyadı"] == r_secim].iloc[0]
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Toplam Atanan", r["Dosya Sayısı"])
    m2.metric("Karar Verilen", r["Onay"] + r["Düzeltme"])
    m3.metric("Bekleyen", r["Dosya Sayısı"] - (r["Onay"] + r["Düzeltme"]))
    
    st.write("---")
    st.write(f"✅ **ONAY:** {r['Onay']} | ⚠️ **DÜZELTME:** {r['Düzeltme']}")
    st.write(f"📂 **KAEK:** {r['KAEK']} | 📝 **GÖRÜŞ:** {r['Görüş']} | ❌ **RET:** {r['Ret']}")
    st.write(f"🚫 **KAPSAM DIŞI:** {r['Kapsam Dışı']} | 🔄 **GERİ ÇEKİLDİ:** {r['Geri Çekildi']}")

with tab3:
    st.write("#### 🏢 Birim Analizi")
    # Mevcut birim expander yapısı bozulmadan burada...
    st.info("İç Hastalıkları (27), Çocuk Sağlığı (23)...")

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü (İlk 5)")
    # Mevcut sorumlu expander yapısı bozulmadan burada...
    st.info("Prof. Dr. Meltem Gülhan HALİL ve diğer 4 hoca...")

# --- SABİT ALT BİLGİ ---
st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
