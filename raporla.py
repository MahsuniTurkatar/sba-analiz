import streamlit as st

# Sayfa Yapılandırması - Yayılmayı önleyen 'centered' yapı
st.set_page_config(page_title="Hacettepe SBA 2026", layout="centered")

# Dark Navy Blue (Gece Mavisi) & Hacettepe Gold Teması
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    .block-container { max-width: 800px; padding-top: 2rem; }
    
    /* Metrik Kartları */
    div[data-testid="stMetric"] {
        background-color: #001d3d !important;
        border: 1px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    
    /* Detaylı Bilgi Kartları */
    .data-card {
        background-color: #001d3d;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffc300;
        margin-bottom: 12px;
    }
    
    /* Yazı Renkleri */
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    .rank-num { color: #ffc300; font-weight: bold; font-size: 20px; margin-right: 12px; }
    </style>
    """, unsafe_allow_html=True)

# Kurumsal Başlık
st.markdown("<h1 style='text-align: center; margin-bottom:0;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-top:0;'>SBA Analiz Sistemi</h3>", unsafe_allow_html=True)

# --- VERİ MERKEZİ (Excel'den Birebir) ---
#
toplam_basvuru = 190
kurul_sayisi = 4

# Raportör Verileri
raportorler = {
    "Dr. Öğr. Üyesi Müge DEMİR": {"Atanan": 31, "ONAY": 18, "DÜZELTME": 11, "KAEK": 2},
    "Doç. Dr. Kübra AYKAÇ": {"Atanan": 30, "ONAY": 14, "DÜZELTME": 9, "KAEK": 0},
    "Doç. Dr. Burcu ERSÖZ ALAN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 6, "KAEK": 0},
    "Prof. Dr. Gözde GİRGİN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 5, "KAEK": 0},
    "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY": {"Atanan": 28, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1},
    "Prof. Dr. Melih Önder BABAOĞLU": {"Atanan": 28, "ONAY": 12, "DÜZELTME": 8, "KAEK": 0},
    "Prof. Dr. M. Özgür UYANIK": {"Atanan": 27, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1},
    "Prof. Dr. Ayşe Nurten AKARSU": {"Atanan": 22, "ONAY": 11, "DÜZELTME": 4, "KAEK": 0},
    "Doç. Dr. Ekim GÜMELER": {"Atanan": 17, "ONAY": 11, "DÜZELTME": 4, "KAEK": 1},
    "Prof. Dr. Yavuz AYHAN": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 8, "KAEK": 0},
    "Doç. Dr. Tolga ÇAKMAK": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 5, "KAEK": 1},
    "Prof. Dr. Ayşe KİN İŞLER": {"Atanan": 17, "ONAY": 12, "DÜZELTME": 3, "KAEK": 2}
}

# Birim İlk 5
ilk_5_birim = [
    {"Birim": "İç Hastalıkları Anabilim Dalı", "Sayi": 27},
    {"Birim": "Çocuk Sağlığı ve Hastalıkları A.D.", "Sayi": 23},
    {"Birim": "Kadın Hastalıkları ve Doğum A.D.", "Sayi": 9},
    {"Birim": "Klinik Eczacılık Anabilim Dalı", "Sayi": 9},
    {"Birim": "Göğüs Hastalıkları Anabilim Dalı", "Sayi": 9}
]

# Sorumlu İlk 5
ilk_5_sorumlu = [
    {"Sorumlu": "Prof. Dr. Meltem Gülhan HALİL", "Birim": "İç Hastalıkları A.D.", "Sayi": 6},
    {"Sorumlu": "Prof. Dr. Yasemin ÖZSÜREKCİ", "Birim": "Çocuk Sağlığı ve Hastalıkları A.D.", "Sayi": 5},
    {"Sorumlu": "Dr. Öğr. Üyesi Gonca ÖZTEN", "Birim": "Klinik Eczacılık A.D.", "Sayi": 4},
    {"Sorumlu": "Doç. Dr. Süleyman Nahit ŞENDUR", "Birim": "İç Hastalıkları A.D.", "Sayi": 4},
    {"Sorumlu": "Prof. Dr. Ali Fuat KALYONCU", "Birim": "Göğüs Hastalıkları A.D.", "Sayi": 4}
]

# Ana Özet Paneli
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", f"{toplam_basvuru}")
c2.metric("🗓️ Kurul Sayısı", f"{kurul_sayisi}")

st.write("---")

# --- 3 AYRI ANALİZ SEKMESİ ---
tab1, tab2, tab3 = st.tabs(["👤 Raportörler", "🏛️ Top 5 Birim", "🎓 Top 5 Sorumlu"])

with tab1:
    secilen_r = st.selectbox("Bir raportör seçiniz:", list(raportorler.keys()))
    u = raportorler[secilen_r]
    
    m1, m2, m3 = st.columns(3)
    karar_sayisi = u['ONAY'] + u['DÜZELTME'] + u['KAEK']
    m1.metric("Atanan", f"{u['Atanan']}")
    m2.metric("Karar", f"{karar_sayisi}")
    m3.metric("Bekleyen", f"{u['Atanan'] - karar_sayisi}")
    
    st.write("#### 📊 Durum Dağılımı")
    for key, val in u.items():
        if key != "Atanan":
            st.write(f"{key}: {val}")
            st.progress(val / u['Atanan'] if u['Atanan'] > 0 else 0)

with tab2:
    st.write("#### 🏢 Başvuru Sayısı En Yüksek Birimler")
    for i, b in enumerate(ilk_5_birim, 1):
        st.markdown(f"""
            <div class="data-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div><span class="rank-num">#{i}</span><b>{b['Birim']}</b></div>
                    <div style="color:#ffc300; font-size:18px; font-weight:bold;">{b['Sayi']} Dosya</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

with tab3:
    st.write("#### 👨‍🏫 En Çok Başvuru Yapan Sorumlular")
    for i, s in enumerate(ilk_5_sorumlu, 1):
        st.markdown(f"""
            <div class="data-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span class="rank-num">#{i}</span><b>{s['Sorumlu']}</b><br>
                        <small style="margin-left:38px; color:#aaaaaa;">{s['Birim']}</small>
                    </div>
                    <div style="color:#ffc300; font-size:18px; font-weight:bold;">{s['Sayi']} Dosya</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.write("---")
st.markdown("<center style='color:#555;'>Hacettepe SBA Karar Destek Sistemi © 2026</center>", unsafe_allow_html=True)
