import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: ESKİ GENİŞ VE SAĞLAM DÜZEN ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Üst Metrikler (190 ve 4) */
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
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .nitelik-box {
        flex: 1;
        background-color: #001d3d;
        border: 1px solid #ffc300;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
    }
    .n-label { color: #ffffff; font-size: 0.9rem; }
    .n-value { color: #ffc300; font-weight: bold; font-size: 1.4rem; display: block; }

    /* Başlıklar ve Sekmeler */
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    
    .footer {
        width: 100%;
        text-align: center;
        color: #ffc300;
        padding: 20px;
        border-top: 1px solid #ffc300;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETLERİ ---

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

# 2. Raportörler (Karar Kalemleriyle Birlikte)
raportor_data = {
    "Adı Soyadı": ["Prof. Dr. Ayşe Nurten AKARSU", "Prof. Dr. M. Özgür UYANIK", "Prof. Dr. Melih Önder BABAOĞLU", "Prof. Dr. Ayşe KİN İŞLER", "Prof. Dr. Yavuz AYHAN", "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY", "Prof. Dr. Gözde GİRGİN", "Doç. Dr. Kübra AYKAÇ", "Doç. Dr. Tolga ÇAKMAK", "Doç. Dr. Burcu ERSÖZ ALAN", "Doç. Dr. Ekim GÜMELER", "Dr. Öğr. Üyesi Müge DEMİR"],
    "Dosya": [31, 35, 28, 25, 25, 36, 36, 38, 25, 36, 26, 39],
    "Onay": [11, 17, 12, 12, 9, 17, 18, 14, 9, 18, 11, 18],
    "Düzeltme": [11, 7, 13, 3, 8, 8, 9, 15, 5, 10, 4, 11],
    "KAEK": [0, 1, 0, 2, 0, 1, 0, 1, 1, 0, 1, 2],
    "Görüş": [0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    "Ret": [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    "Kapsam Dışı": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    "Geri Çekildi": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
df_raportor = pd.DataFrame(raportor_data)

# --- ÜST PANEL ---
st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# Metrikler
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

# Gündem Tablosu
st.write("### 📅 2026 Gündem Sayıları")
st.table(df_gundem)

# --- SEKMELER (ÇALIŞAN MENÜLER) ---
t1, t2, t3, t4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with t1:
    st.write("#### 📋 Kurul Üye_1 Genel Karar Çizelgesi")
    st.image("genel_tablo_ekran_goruntusu.png", use_column_width=True)

with t2:
    st.write("#### 🔍 Raportör Detaylı Karar Takibi")
    r_sec = st.selectbox("Raportör Seçiniz:", df_raportor["Adı Soyadı"].tolist())
    r = df_raportor[df_raportor["Adı Soyadı"] == r_sec].iloc[0]
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Toplam Dosya", r["Dosya"])
    m2.metric("Karar Verilen", int(r["Onay"] + r["Düzeltme"]))
    m3.metric("Bekleyen", int(r["Dosya"] - (r["Onay"] + r["Düzeltme"])))
    
    st.markdown(f"""
    > ✅ **ONAY:** {r['Onay']} | ⚠️ **DÜZELTME:** {r['Düzeltme']} | 📂 **KAEK:** {r['KAEK']}  
    > 📝 **GÖRÜŞ:** {r['Görüş']} | ❌ **RET:** {r['Ret']} | 🚫 **KAPSAM DIŞI:** {r['Kapsam Dışı']}
    """)

with t3:
    st.write("#### 🏢 Birim Analizi (İlk 5)")
    birimler = [("İç Hastalıkları Anabilim Dalı", 27), ("Çocuk Sağlığı ve Hastalıkları A.D.", 23), ("Kadın Hastalıkları ve Doğum A.D.", 9), ("Klinik Eczacılık Anabilim Dalı", 9), ("Göğüs Hastalıkları Anabilim Dalı", 9)]
    for ad, sayi in birimler:
        with st.expander(f"{ad} ({sayi} Dosya)"):
            st.write("Detaylı analiz aktif.")

with t4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü")
    sorumlular = [{"Hoca": "Prof. Dr. Meltem Gülhan HALİL", "B": 4, "U": 2}, {"Hoca": "Prof. Dr. Yasemin ÖZSÜREKCİ", "B": 2, "U": 3}, {"Hoca": "Dr. Öğr. Üyesi Gonca ÖZTEN", "B": 4, "U": 0}]
    for s in sorumlular:
        with st.expander(f"{s['Hoca']}"):
            st.write(f"📊 Bireysel: {s['B']} | 🎓 Uzmanlık: {s['U']}")

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
