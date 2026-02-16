import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: SABİT VE SAĞLAM DÜZEN ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Metrik ve Nitelik Kutuları */
    div[data-testid="stMetric"], .nitelik-box {
        background-color: #001d3d !important;
        border: 2px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        text-align: center !important;
    }

    /* Kutuları Yan Yana Tutan Konteyner */
    .ozet-konteyner {
        display: flex;
        flex-wrap: nowrap;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 10px;
    }
    .kutu-item {
        flex: 1;
        background-color: #001d3d;
        border: 2px solid #ffc300;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
    }
    .kutu-label { color: #ffffff; font-size: 0.9rem; display: block; margin-bottom: 3px; }
    .kutu-value { color: #ffc300; font-weight: bold; font-size: 1.5rem; }

    /* Başlıklar ve Sekmeler */
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    
    /* Alt Bilgi */
    .footer {
        width: 100%;
        background-color: #000814;
        color: #ffc300;
        text-align: center;
        padding: 20px 0;
        font-weight: bold;
        border-top: 1px solid #ffc300;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETLERİ (TAM KADRO - HİÇBİRİ KIRPILMADI) ---

# 1. Raportörler (12 Kişi ve Tüm Kararlar)
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

# 2. Sorumlu Araştırmacılar (Tüm Sayılar Dahil)
sorumlular = [
    {"Hoca": "Prof. Dr. Meltem Gülhan HALİL", "D": 6, "B": 4, "U": 2, "Birim": "İç Hastalıkları A.D."},
    {"Hoca": "Prof. Dr. Yasemin ÖZSÜREKCİ", "D": 5, "B": 2, "U": 3, "Birim": "Çocuk Sağlığı A.D."},
    {"Hoca": "Dr. Öğr. Üyesi Gonca ÖZTEN", "D": 4, "B": 4, "U": 0, "Birim": "Kadın Hastalıkları ve Doğum A.D."},
    {"Hoca": "Doç. Dr. Süleyman Nahit ŞENDUR", "D": 4, "B": 3, "U": 1, "Birim": "İç Hastalıkları A.D."},
    {"Hoca": "Prof. Dr. Ali Fuat KALYONCU", "D": 4, "B": 4, "U": 0, "Birim": "Göğüs Hastalıkları A.D."}
]

# --- ÜST PANEL ---
st.markdown("<h1 style='text-align: center; margin-bottom:0;'>Sağlık Bilimleri Araştırma Etik Kurulu</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-top:0;'>2026 Analiz Raporu</h3>", unsafe_allow_html=True)

# Üst Metrikler
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# Nitelikler (1. Sıra)
st.markdown("""
    <div class="ozet-konteyner">
        <div class="kutu-item"><span class="kutu-label">Bireysel Araştırma</span><span class="kutu-value">128</span></div>
        <div class="kutu-item"><span class="kutu-label">Uzmanlık Tezi</span><span class="kutu-value">48</span></div>
        <div class="kutu-item"><span class="kutu-label">Y. Lisans Tezi</span><span class="kutu-value">10</span></div>
        <div class="kutu-item"><span class="kutu-label">Doktora Tezi</span><span class="kutu-value">4</span></div>
    </div>
""", unsafe_allow_html=True)

# Gündem Sayıları (2. Sıra - İstediğin Sayılar)
st.markdown("""
    <div class="ozet-konteyner">
        <div class="kutu-item"><span class="kutu-label">Yeni Başvuru</span><span class="kutu-value">190</span></div>
        <div class="kutu-item"><span class="kutu-label">Gelen Düzeltme</span><span class="kutu-value">58</span></div>
        <div class="kutu-item"><span class="kutu-label">Gelen Dilekçe</span><span class="kutu-value">42</span></div>
    </div>
""", unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Genel Durum", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

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
    birimler = [{"Ad": "İç Hastalıkları Anabilim Dalı", "T": 27}, {"Ad": "Çocuk Sağlığı ve Hastalıkları A.D.", "T": 23}, {"Ad": "Kadın Hastalıkları ve Doğum A.D.", "T": 9}, {"Ad": "Klinik Eczacılık Anabilim Dalı", "T": 9}, {"Ad": "Göğüs Hastalıkları Anabilim Dalı", "T": 9}]
    for b in birimler:
        with st.expander(f"{b['Ad']} ({b['T']} Dosya)"):
            st.write("Birim bazlı detaylı raporlama aktif.")

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü (İlk 5)")
    for s in sorumlular:
        with st.expander(f"{s['Hoca']} ({s['D']} Dosya) | Birim: {s['Birim']}"):
            st.write(f"📊 **Bireysel Araştırma:** {s['B']}")
            st.write(f"🎓 **Uzmanlık Tezi:** {s['U']}")

# --- ALT BİLGİ ---
st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
