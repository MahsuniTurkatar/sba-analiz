import streamlit as st
import pandas as pd

# Mobil ve Web Uyumu
st.set_page_config(page_title="SBA 2026 Rapor", layout="wide")

# Modern Stil Ayarları
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #3498db;
    }
    .status-card {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        color: white;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
    }
    </style>
    """, unsafe_allow_label_with_html=True)

st.title("📊 SBA 2026 Kurul Analiz Sistemi")

# --- HOCA VERİLERİ (Gömülü Sistem) ---
veriler = {
    "Dr. Öğr. Üyesi Müge DEMİR": {"Atanan": 31, "ONAY": 18, "DÜZELTME": 11, "KAEK": 2, "GÖRÜŞ": 0, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Doç. Dr. Kübra AYKAÇ": {"Atanan": 30, "ONAY": 14, "DÜZELTME": 9, "KAEK": 0, "GÖRÜŞ": 1, "RET": 1, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Doç. Dr. Burcu ERSÖZ ALAN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 6, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. Gözde GİRGİN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 5, "KAEK": 0, "GÖRÜŞ": 1, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY": {"Atanan": 28, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. Melih Önder BABAOĞLU": {"Atanan": 28, "ONAY": 12, "DÜZELTME": 8, "KAEK": 0, "GÖRÜŞ": 1, "RET": 1, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. M. Özgür UYANIK": {"Atanan": 27, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. Ayşe Nurten AKARSU": {"Atanan": 22, "ONAY": 11, "DÜZELTME": 4, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Doç. Dr. Ekim GÜMELER": {"Atanan": 17, "ONAY": 11, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 0, "RET": 1, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. Yavuz AYHAN": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 8, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Doç. Dr. Tolga ÇAKMAK": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 5, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. Ayşe KİN İŞLER": {"Atanan": 17, "ONAY": 12, "DÜZELTME": 3, "KAEK": 2, "GÖRÜŞ": 0, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0}
}

# Seçim
secilen_uye = st.selectbox("👤 Raportör Listesi:", ["Genel Bakış"] + sorted(veriler.keys()))

if secilen_uye == "Genel Bakış":
    st.metric("📈 Kurul Toplam Başvuru", "145")
    st.info("Raportör bazlı detayları görmek için yukarıdan bir isim seçebilirsiniz.")
else:
    u = veriler[secilen_uye]
    
    # Şık Özet Kartları
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Dosya Yükü", f"{u['Atanan']} Dosya")
    with c2:
        tamam = sum([u[k] for k in ["ONAY", "DÜZELTME", "KAEK", "GÖRÜŞ", "RET"]])
        st.metric("Karar Alınan", f"{tamam} Dosya")

    st.subheader("📋 Karar Detayları")
    
    # Mobil Uyumlu Özel Renkli Kartlar (Grafik yerine daha şık durur)
    def status_box(label, value, color):
        if value > 0:
            st.markdown(f"""<div class="status-card" style="background-color: {color};">
                <span>{label}</span><span>{value}</span>
                </div>""", unsafe_allow_label_with_html=True)

    status_box("✅ ONAY", u['ONAY'], "#27ae60")
    status_box("🔧 DÜZELTME", u['DÜZELTME'], "#2980b9")
    status_box("🔬 KAEK", u['KAEK'], "#8e44ad")
    status_box("💬 GÖRÜŞ", u['GÖRÜŞ'], "#f39c12")
    status_box("🚫 RET", u['RET'], "#c0392b")
    status_box("📁 KAPSAM DIŞI", u['KAPSAM DIŞI'], "#7f8c8d")
    status_box("↩️ GERİ ÇEKİLDİ", u['GERİ ÇEKİLDİ'], "#34495e")

st.divider()
st.caption("📱 Bu panel mobil görünüm için optimize edilmiştir.")
