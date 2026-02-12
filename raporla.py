import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="SBA 2026 Kurul Analiz", layout="wide")

# Görsel Stil Geliştirmeleri
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stProgress > div > div > div > div { background-color: #3498db; }
    .unit-card {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 8px;
        border-left: 5px solid #2ecc71;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_label_with_html=True)

# Başlık Bölümü
st.title("📊 SBA 2026 Karar Destek Sistemi")
st.subheader("Sağlık Bilimleri Araştırma Etik Kurulu - 2026")

# --- VERİ SETİ (Raportörler) ---
raportorler = {
    "Dr. Öğr. Üyesi Müge DEMİR": {"Atanan": 31, "ONAY": 18, "DÜZELTME": 11, "KAEK": 2, "GÖRÜŞ": 0, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Doç. Dr. Kübra AYKAÇ": {"Atanan": 30, "ONAY": 14, "DÜZELTME": 9, "KAEK": 0, "GÖRÜŞ": 1, "RET": 1, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Doç. Dr. Burcu ERSÖZ ALAN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 6, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. Gözde GİRGİN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 5, "KAEK": 0, "GÖRÜŞ": 1, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY": {"Atanan": 28, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. Melih Önder BABAOĞLU": {"Atanan": 28, "ONAY": 12, "DÜZELTME": 8, "KAEK": 0, "GÖRÜŞ": 1, "RET": 1, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0}
}

# --- VERİ SETİ (Birimler ve Sorumlular - İlk 10) ---
# Görselden alınan verilere göre simüle edilmiştir
birimler = [
    {"Birim": "Kulak Burun Boğaz Anabilim Dalı", "Sorumlu": "Prof. Dr. X", "Dosya": 5},
    {"Birim": "Ortopedi ve Travmatoloji Anabilim Dalı", "Sorumlu": "Doç. Dr. Y", "Dosya": 5},
    {"Birim": "Nöroloji Anabilim Dalı", "Sorumlu": "Dr. Öğr. Üyesi Z", "Dosya": 5},
    {"Birim": "Anatomi Anabilim Dalı", "Sorumlu": "Prof. Dr. A", "Dosya": 4},
    {"Birim": "Radyoloji Anabilim Dalı", "Sorumlu": "Prof. Dr. B", "Dosya": 4},
    {"Birim": "Çocuk ve Ergen Ruh Sağlığı Anabilim Dalı", "Sorumlu": "Doç. Dr. C", "Dosya": 4},
    {"Birim": "Üroloji Anabilim Dalı", "Sorumlu": "Dr. Öğr. Üyesi D", "Dosya": 4},
    {"Birim": "Deri ve Zührevi Hastalıklar Anabilim Dalı", "Sorumlu": "Prof. Dr. E", "Dosya": 4},
    {"Birim": "Fiziksel Tıp ve Rehabilitasyon Anabilim Dalı", "Sorumlu": "Doç. Dr. F", "Dosya": 3},
    {"Birim": "Göz Hastalıkları Anabilim Dalı", "Sorumlu": "Dr. G", "Dosya": 3}
]

# --- SEKME YAPISI ---
tab1, tab2 = st.tabs(["👤 Raportör Analizi", "🏢 Birim & Sorumlu Analizi"])

with tab1:
    secilen = st.selectbox("Raportör Seçiniz:", ["Genel Bakış"] + list(raportorler.keys()))
    
    if secilen == "Genel Bakış":
        st.metric("📈 Kurul Toplam Başvuru", "145")
        st.info("Bireysel performans ve dosya detayları için isim seçiniz.")
    else:
        u = raportorler[secilen]
        c1, c2, c3 = st.columns(3)
        c1.metric("Toplam Yük", f"{u['Atanan']} Dosya")
        karar_toplam = u['ONAY'] + u['DÜZELTME'] + u['KAEK'] + u['GÖRÜŞ'] + u['RET']
        c2.metric("Karar Verilen", f"{karar_toplam}")
        c3.metric("Bekleyen", f"{u['Atanan'] - karar_toplam}")

        st.write("### 📋 Karar Kırılımları")
        
        # Ayrıntılı Görsellik (Progress barlar ile)
        for kat, deger in u.items():
            if kat not in ["Atanan"] and deger > 0:
                oran = deger / u['Atanan']
                st.write(f"**{kat}**: {deger}")
                st.progress(oran)

with tab2:
    st.subheader("🏢 En Çok Başvuru Yapan İlk 10 Birim")
    for item in birimler:
        st.markdown(f"""
            <div class="unit-card">
                <strong>{item['Birim']}</strong><br>
                <small>Sorumlu: {item['Sorumlu']} | 📂 Dosya Sayısı: {item['Dosya']}</small>
            </div>
        """, unsafe_allow_label_with_html=True)

st.divider()
st.write("© 2026 Sağlık Bilimleri Araştırma Etik Kurulu")
