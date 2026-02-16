import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: TASARIM VE TABLO DÜZENİ ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important;
        border: 2px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        text-align: center !important;
    }
    .nitelik-konteyner { display: flex; justify-content: space-between; gap: 10px; margin-bottom: 20px; }
    .nitelik-box {
        flex: 1; background-color: #001d3d; border: 1px solid #ffc300;
        border-radius: 8px; padding: 10px; text-align: center;
    }
    .n-label { color: #ffffff; font-size: 0.85rem; }
    .n-value { color: #ffc300; font-weight: bold; font-size: 1.2rem; display: block; }
    .table-container { display: flex; justify-content: center; margin: 20px 0; }
    .styled-table { width: 70% !important; border-collapse: collapse; color: white; }
    .styled-table th, .styled-table td { border: 1px solid #ffc300; padding: 8px; text-align: center !important; }
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    .footer { text-align: center; color: #ffc300; padding: 20px; border-top: 1px solid #ffc300; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETLERİ ---
gundem_data = {
    "S.NO": ["1.", "2.", "3.", "4.", "TOPLAM"],
    "Gündem Tarihleri": ["06.01.2026", "20.01.2026", "04.02.2026", "17.02.2026", "-"],
    "Başvuru": [55, 45, 45, 45, 190],
    "Düzeltme": [16, 13, 12, 17, 58],
    "Dilekçe": [9, 11, 15, 7, 42],
    "Toplam": [80, 69, 72, 69, 290]
}
df_gundem = pd.DataFrame(gundem_data)

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

c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

st.markdown("""
    <div class="nitelik-konteyner">
        <div class="nitelik-box"><span class="n-label">Bireysel Araştırma</span><span class="n-value">128</span></div>
        <div class="nitelik-box"><span class="n-label">Uzmanlık Tezi</span><span class="n-value">48</span></div>
        <div class="nitelik-box"><span class="n-label">Y. Lisans Tezi</span><span class="n-value">10</span></div>
        <div class="nitelik-box"><span class="n-label">Doktora Tezi</span><span class="n-value">4</span></div>
    </div>
""", unsafe_allow_html=True)

st.write("### 📅 2026 Gündem Sayıları")
st.markdown('<div class="table-container">', unsafe_allow_html=True)
st.markdown(df_gundem.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- SEKMELER ---
t1, t2, t3, t4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi (5 Adet)", "👨‍🏫 Sorumlu Analizi (5 Adet)"])

with t1:
    st.write("#### 📋 Kurul Üye_1 Genel Karar Çizelgesi")
    img_path = "genel_tablo_ekran_goruntusu.png"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.info("Görsel yükleniyor...")

with t2:
    st.write("#### 🔍 Raportör Detaylı Karar Takibi")
    r_sec = st.selectbox("Raportör Seçiniz:", df_raportor["Adı Soyadı"].tolist())
    r = df_raportor[df_raportor["Adı Soyadı"] == r_sec].iloc[0]
    m1, m2, m3 = st.columns(3)
    m1.metric("Toplam Dosya", r["Dosya"])
    m2.metric("Karar Verilen", int(r["Onay"] + r["Düzeltme"]))
    m3.metric("Fark", int(r["Dosya"] - (r["Onay"] + r["Düzeltme"])))
    st.markdown(f"> ✅ **ONAY:** {r['Onay']} | ⚠️ **DÜZELTME:** {r['Düzeltme']} | 📂 **KAEK:** {r['KAEK']} | ❌ **RET:** {r['Ret']}")

with t3:
    st.write("#### 🏢 En Çok Başvuru Yapan İlk 5 Birim")
    birimler = [
        {"Ad": "İç Hastalıkları Anabilim Dalı", "S": 27},
        {"Ad": "Çocuk Sağlığı ve Hastalıkları A.D.", "S": 23},
        {"Ad": "Kadın Hastalıkları ve Doğum A.D.", "S": 9},
        {"Ad": "Klinik Eczacılık Anabilim Dalı", "S": 9},
        {"Ad": "Göğüs Hastalıkları Anabilim Dalı", "S": 9}
    ]
    for b in birimler:
        st.markdown(f"""
        <div style="background-color:#001d3d; border:1px solid #ffc300; border-radius:5px; padding:10px; margin-bottom:5px;">
            <span style="color:#ffc300; font-weight:bold;">{b['Ad']}</span> 
            <span style="float:right; color:white;">{b['S']} Dosya</span>
        </div>
        """, unsafe_allow_html=True)

with t4:
    st.write("#### 👨‍🏫 En Çok Başvuru Yapan İlk 5 Sorumlu Araştırmacı")
    sorumlular = [
        {"Hoca": "Prof. Dr. Meltem Gülhan HALİL", "B": 4, "U": 2, "T": 6},
        {"Hoca": "Prof. Dr. Yasemin ÖZSÜREKCİ", "B": 2, "U": 3, "T": 5},
        {"Hoca": "Dr. Öğr. Üyesi Gonca ÖZTEN", "B": 4, "U": 0, "T": 4},
        {"Hoca": "Doç. Dr. Süleyman Nahit ŞENDUR", "B": 3, "U": 1, "T": 4},
        {"Hoca": "Prof. Dr. Ali Fuat KALYONCU", "B": 4, "U": 0, "T": 4}
    ]
    for s in sorumlular:
        with st.expander(f"{s['Hoca']} (Toplam: {s['T']} Dosya)"):
            st.write(f"📊 **Bireysel Araştırma:** {s['B']}")
            st.write(f"🎓 **Uzmanlık Tezi:** {s['U']}")

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
