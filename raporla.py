import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: SABİT VE SAĞLAM DÜZEN ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Üst Metrik Kutuları */
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 20px;
    }
    .metric-box {
        flex: 1;
        background-color: #001d3d;
        border: 2px solid #ffc300;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
    }
    .metric-label { color: #ffffff; font-size: 0.85rem; display: block; }
    .metric-value { color: #ffc300; font-weight: bold; font-size: 1.3rem; }

    /* Başlıklar ve Tablo Stil */
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    .stDataFrame, .stTable { border: 1px solid #ffc300; border-radius: 5px; }
    
    /* Footer */
    .footer {
        width: 100%;
        text-align: center;
        color: #ffc300;
        padding: 20px;
        border-top: 1px solid #ffc300;
        margin-top: 30px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. VERİ SETİ: RAPORTÖRLER (12 KİŞİ - TAM LİSTE) ---
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
    "Görüş": [0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    "Ret": [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    "Kapsam Dışı": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    "Geri Çekildi": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
df_raportor = pd.DataFrame(raportor_data)

# --- 2. VERİ SETİ: GÜNDEM SAYILARI (RESİMDEKİ GİBİ) ---
gundem_data = {
    "S.NO": [1, 2, 3, 4],
    "Gündem Tarihleri": ["06.01.2026", "20.01.2026", "04.02.2026", "17.02.2026"],
    "Başvuru": [55, 45, 45, 45],
    "Düzeltme": [16, 13, 12, 17],
    "Dilekçe": [9, 11, 15, 7],
    "Toplam": [80, 69, 72, 69]
}
df_gundem = pd.DataFrame(gundem_data)
# Alt toplam satırı
toplam_satiri = pd.DataFrame({"S.NO":["TOPLAM"], "Gündem Tarihleri":["-"], "Başvuru":[190], "Düzeltme":[58], "Dilekçe":[42], "Toplam":[290]})
df_gundem_full = pd.concat([df_gundem, toplam_satiri], ignore_index=True)

# --- 3. VERİ SETİ: SORUMLULAR (GONCA HOCA VE SAYILAR DAHİL) ---
sorumlular = [
    {"Hoca": "Prof. Dr. Meltem Gülhan HALİL", "Birim": "İç Hastalıkları A.D.", "B": 4, "U": 2, "T": 6},
    {"Hoca": "Prof. Dr. Yasemin ÖZSÜREKCİ", "Birim": "Çocuk Sağlığı A.D.", "B": 2, "U": 3, "T": 5},
    {"Hoca": "Dr. Öğr. Üyesi Gonca ÖZTEN", "Birim": "Kadın Hastalıkları ve Doğum A.D.", "B": 4, "U": 0, "T": 4},
    {"Hoca": "Doç. Dr. Süleyman Nahit ŞENDUR", "Birim": "İç Hastalıkları A.D.", "B": 3, "U": 1, "T": 4},
    {"Hoca": "Prof. Dr. Ali Fuat KALYONCU", "Birim": "Göğüs Hastalıkları A.D.", "B": 4, "U": 0, "T": 4}
]

# --- ÜST PANEL ---
st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>2026 Analiz Raporu</h3>", unsafe_allow_html=True)

# Nitelik Kutuları (Üst Sıra)
st.markdown(f"""
    <div class="metric-container">
        <div class="metric-box"><span class="metric-label">Toplam Başvuru</span><span class="metric-value">190</span></div>
        <div class="metric-box"><span class="metric-label">Bireysel Araştırma</span><span class="metric-value">128</span></div>
        <div class="metric-box"><span class="metric-label">Uzmanlık Tezi</span><span class="metric-value">48</span></div>
        <div class="metric-box"><span class="metric-label">Y. Lisans Tezi</span><span class="metric-value">10</span></div>
        <div class="metric-box"><span class="metric-label">Doktora Tezi</span><span class="metric-value">4</span></div>
    </div>
""", unsafe_allow_html=True)

# Gündem Sayıları Tablosu (Tam İstediğin Yer)
st.write("### 📅 2026 Gündem Sayıları")
st.table(df_gundem_full)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.write("#### 📋 Kurul Üye_1 Genel Karar Çizelgesi")
    try:
        st.image("genel_tablo_ekran_goruntusu.png", use_column_width=True)
    except:
        st.info("Genel Karar Çizelgesi görseli bekleniyor...")

with tab2:
    st.write("#### 🔍 Raportör Detaylı Karar Takibi")
    r_secim = st.selectbox("Raportör Seçiniz:", df_raportor["Adı Soyadı"].tolist())
    r = df_raportor[df_raportor["Adı Soyadı"] == r_secim].iloc[0]
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Toplam Atanan", r["Dosya Sayısı"])
    m2.metric("Karar Verilen", int(r["Onay"] + r["Düzeltme"]))
    m3.metric("Bekleyen", int(r["Dosya Sayısı"] - (r["Onay"] + r["Düzeltme"])))
    
    st.write("---")
    st.write(f"✅ **ONAY:** {r['Onay']} | ⚠️ **DÜZELTME:** {r['Düzeltme']} | 📂 **KAEK:** {r['KAEK']}")
    st.write(f"📝 **GÖRÜŞ:** {r['Görüş']} | ❌ **RET:** {r['Ret']} | 🚫 **KAPSAM DIŞI:** {r['Kapsam Dışı']} | 🔄 **GERİ ÇEKİLDİ:** {r['Geri Çekildi']}")

with tab3:
    st.write("#### 🏢 Birim Analizi (İlk 5)")
    birimler = [{"Ad": "İç Hastalıkları Anabilim Dalı", "T": 27}, {"Ad": "Çocuk Sağlığı ve Hastalıkları A.D.", "T": 23}, {"Ad": "Kadın Hastalıkları ve Doğum A.D.", "T": 9}]
    for b in birimler:
        with st.expander(f"{b['Ad']} ({b['T']} Dosya)"):
            st.write("Birim detayları.")

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü (İlk 5)")
    for s in sorumlular:
        with st.expander(f"{s['Hoca']} ({s['T']} Dosya)"):
            st.write(f"🏢 **Birim:** {s['Birim']}")
            st.write(f"📊 **Bireysel:** {s['B']} | 🎓 **Uzmanlık:** {s['U']}")

# --- ALT BİLGİ ---
st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
