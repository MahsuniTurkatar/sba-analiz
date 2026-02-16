import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: TABLO DARALTMA, ORTALAMA VE TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Metrik Kutuları */
    div[data-testid="stMetric"] {
        background-color: #001d3d !important;
        border: 2px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        text-align: center !important;
    }

    /* Nitelik Kutuları */
    .nitelik-konteyner {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 20px;
    }
    .nitelik-box {
        flex: 1;
        background-color: #001d3d;
        border: 1px solid #ffc300;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
    }
    .n-label { color: #ffffff; font-size: 0.85rem; }
    .n-value { color: #ffc300; font-weight: bold; font-size: 1.2rem; display: block; }

    /* Tabloyu Merkeze Al ve Daralt */
    .table-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    .styled-table {
        width: 70% !important;
        border-collapse: collapse;
        color: white;
    }
    .styled-table th, .styled-table td {
        border: 1px solid #ffc300;
        padding: 8px;
        text-align: center !important;
    }
    
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    .footer { text-align: center; color: #ffc300; padding: 20px; border-top: 1px solid #ffc300; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETLERİ (TAM LİSTE) ---

# 1. Gündem Tablosu
gundem_data = {
    "S.NO": ["1.", "2.", "3.", "4.", "TOPLAM"],
    "Gündem Tarihleri": ["06.01.2026", "20.01.2026", "04.02.2026", "17.02.2026", "-"],
    "Başvuru": [55, 45, 45, 45, 190],
    "Düzeltme": [16, 13, 12, 17, 58],
    "Dilekçe": [9, 11, 15, 7, 42],
    "Toplam": [80, 69, 72, 69, 290]
}
df_gundem = pd.DataFrame(gundem_data)

# 2. Raportör Verileri (Eksiksiz 12 Kişi)
raportor_data = {
    "Adı Soyadı": ["Prof. Dr. Ayşe Nurten AKARSU", "Prof. Dr. M. Özgür UYANIK", "Prof. Dr. Melih Önder BABAOĞLU", "Prof. Dr. Ayşe KİN İŞLER", "Prof. Dr. Yavuz AYHAN", "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY", "Prof. Dr. Gözde GİRGİN", "Doç. Dr. Kübra AYKAÇ", "Doç. Dr. Tolga ÇAKMAK", "Doç. Dr. Burcu ERSÖZ ALAN", "Doç. Dr. Ekim GÜMELER", "Dr. Öğr. Üyesi Müge DEMİR"],
    "Dosya": [31, 35, 28, 25, 25, 36, 36, 38, 25, 36, 26, 39],
    "Onay": [11, 17, 12, 12, 9, 17, 18, 14, 9, 18, 11, 18],
    "Düzeltme": [11, 7, 13, 3, 8, 8, 9, 15, 5, 10, 4, 11],
    "KAEK": [0, 1, 0, 2, 0, 1, 0, 1, 1, 0, 1, 2],
    "Görüş": [0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    "Ret": [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0]
}
df_raportor = pd.DataFrame(raportor_data)

# --- ÜST PANEL ---
st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# 190 Başvuru / 4 Toplantı
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# Nitelikler
st.markdown("""
    <div class="nitelik-konteyner">
        <div class="nitelik-box"><span class="n-label">Bireysel Araştırma</span><span class="n-value">128</span></div>
        <div class="nitelik-box"><span class="n-label">Uzmanlık Tezi</span><span class="n-value">48</span></div>
        <div class="nitelik-box"><span class="n-label">Y. Lisans Tezi</span><span class="n-value">10</span></div>
        <div class="nitelik-box"><span class="n-label">Doktora Tezi</span><span class="n-value">4</span></div>
    </div>
""", unsafe_allow_html=True)

# Gündem Tablosu (Daraltılmış, Ortalı, İndexsiz)
st.write("### 📅 2026 Gündem Sayıları")
st.markdown('<div class="table-container">', unsafe_allow_html=True)
st.markdown(df_gundem.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- SEKMELER (TÜM MENÜLER GERİ GELDİ) ---
t1, t2, t3, t4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with t1:
    st.write("#### 📋 Kurul Üye_1 Genel Karar Çizelgesi")
    img_path = "genel_tablo_ekran_goruntusu.png"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.info("Görsel (png) dosyası bekleniyor...")

with t2:
    st.write("#### 🔍 Raportör Detaylı Karar Takibi")
    r_sec = st.selectbox("Raportör Seçiniz:", df_raportor["Adı Soyadı"].tolist())
    r = df_raportor[df_raportor["Adı Soyadı"] == r_sec].iloc[0]
    col_r1, col_r2, col_r3 = st.columns(3)
    col_r1.metric("Toplam Dosya", r["Dosya"])
    col_r2.metric("Karar Verilen", int(r["Onay"] + r["Düzeltme"]))
    col_r3.metric("Fark (Bekleyen)", int(r["Dosya"] - (r["Onay"] + r["Düzeltme"])))
    st.markdown(f"""
    > ✅ **ONAY:** {r['Onay']} | ⚠️ **DÜZELTME:** {r['Düzeltme']} | 📂 **KAEK:** {r['KAEK']} | ❌ **RET:** {r['Ret']} | 📝 **GÖRÜŞ:** {r['Görüş']}
    """)

with t3:
    st.write("#### 🏢 Birim Analizi (İlk 5)")
    birimler = [("İç Hastalıkları A.D.", 27), ("Çocuk Sağlığı A.D.", 23), ("Kadın Doğum A.D.", 9), ("Klinik Eczacılık A.D.", 9), ("Göğüs Hastalıkları A.D.", 9)]
    for ad, sayi in birimler:
        with st.expander(f"{ad} ({sayi} Dosya)"):
            st.write("Birim detayları aktif.")

with t4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü")
    sorumlular = [
        {"Hoca": "Prof. Dr. Meltem Gülhan HALİL", "B": 4, "U": 2, "T": 6},
        {"Hoca": "Prof. Dr. Yasemin ÖZSÜREKCİ", "B": 2, "U": 3, "T": 5},
        {"Hoca": "Dr. Öğr. Üyesi Gonca ÖZTEN", "B": 4, "U": 0, "T": 4}
    ]
    for s in sorumlular:
        with st.expander(f"{s['Hoca']} ({s['T']} Dosya)"):
            st.write(f"📊 Bireysel: {s['B']} | 🎓 Uzmanlık: {s['U']}")

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
