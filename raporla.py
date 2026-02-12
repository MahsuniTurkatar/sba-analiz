import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# Kurumsal Stil
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stMetric { border-top: 4px solid #ff0000; background-color: #f8f9fa; padding: 15px; border-radius: 5px; }
    .unit-card {
        background-color: #f1f3f5; padding: 12px; border-radius: 8px;
        margin-bottom: 8px; border-left: 6px solid #ff0000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TAM İSTEDİĞİN BAŞLIK ---
st.title("🏛️ Hacettepe Üniversitesi")
st.subheader("Sağlık Bilimleri Araştırma Etik Kurulu")
st.markdown("#### 2026 Yılı Başvuru Analiz Paneli")
st.write("---")

# --- VERİ SETİ (Raportörler - Eksiksiz) ---
raportorler = {
    "Dr. Öğr. Üyesi Müge DEMİR": {"Atanan": 31, "ONAY": 18, "DÜZELTME": 11, "KAEK": 2, "GÖRÜŞ": 0, "RET": 0},
    "Doç. Dr. Kübra AYKAÇ": {"Atanan": 30, "ONAY": 14, "DÜZELTME": 9, "KAEK": 0, "GÖRÜŞ": 1, "RET": 1},
    "Doç. Dr. Burcu ERSÖZ ALAN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 6, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0},
    "Prof. Dr. Gözde GİRGİN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 5, "KAEK": 0, "GÖRÜŞ": 1, "RET": 0},
    "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY": {"Atanan": 28, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0},
    "Prof. Dr. Melih Önder BABAOĞLU": {"Atanan": 28, "ONAY": 12, "DÜZELTME": 8, "KAEK": 0, "GÖRÜŞ": 1, "RET": 1},
    "Prof. Dr. M. Özgür UYANIK": {"Atanan": 27, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0},
    "Prof. Dr. Ayşe Nurten AKARSU": {"Atanan": 22, "ONAY": 11, "DÜZELTME": 4, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0},
    "Doç. Dr. Ekim GÜMELER": {"Atanan": 17, "ONAY": 11, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 0, "RET": 1},
    "Prof. Dr. Yavuz AYHAN": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 8, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0},
    "Doç. Dr. Tolga ÇAKMAK": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 5, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0},
    "Prof. Dr. Ayşe KİN İŞLER": {"Atanan": 17, "ONAY": 12, "DÜZELTME": 3, "KAEK": 2, "GÖRÜŞ": 0, "RET": 0}
}

# --- BİRİMLER (Rakamlar Eklendi) ---
birim_verisi = [
    ("Kulak Burun Boğaz Anabilim Dalı", 5),
    ("Ortopedi ve Travmatoloji Anabilim Dalı", 5),
    ("Nöroloji Anabilim Dalı", 5),
    ("Anatomi Anabilim Dalı", 4),
    ("Radyoloji Anabilim Dalı", 4),
    ("Çocuk ve Ergen Ruh Sağlığı A.D.", 4),
    ("Üroloji Anabilim Dalı", 4),
    ("Deri ve Zührevi Hastalıklar A.D.", 4),
    ("Fiziksel Tıp ve Rehabilitasyon A.D.", 3),
    ("Göz Hastalıkları Anabilim Dalı", 3)
]

tab_r, tab_b = st.tabs(["👥 Raportör Dosya Detayı", "🏢 Birim Başvuru Sayıları"])

with tab_r:
    secilen = st.selectbox("Raportör Seçiniz:", list(raportorler.keys()))
    u = raportorler[secilen]
    
    # Rakamlar Netleşti
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Atanan Dosya", f"{u['Atanan']}")
    karar = sum([u[k] for k in ["ONAY", "DÜZELTME", "KAEK", "GÖRÜŞ", "RET"]])
    c2.metric("Karar Verilen", f"{karar}")
    c3.metric("Bekleyen", f"{u['Atanan'] - karar}")

    st.write("#### 📉 İşlem Dağılımı")
    for k, v in u.items():
        if k != "Atanan" and v >= 0:
            st.write(f"**{k}**: {v}")
            st.progress(v / u['Atanan'] if u['Atanan'] > 0 else 0)

with tab_b:
    st.subheader("🏢 İlk 10 Birim ve Dosya Sayıları")
    for isim, sayi in birim_verisi:
        st.markdown(f"""
            <div class="unit-card">
                <div style="display: flex; justify-content: space-between;">
                    <span>{isim}</span>
                    <b style="color: #ff0000; font-size: 1.2em;">{sayi} Dosya</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.write("---")
st.write("Hacettepe Üniversitesi SBA - 2026")
