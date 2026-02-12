import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="SBA 2026 Kurumsal Panel", layout="wide")

# Kurumsal Stil ve Renkler
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { border-left: 5px solid #003366; background-color: white; padding: 15px; border-radius: 10px; }
    .birim-kart {
        background: white; padding: 12px; border-radius: 10px; border-right: 4px solid #3498db;
        margin-bottom: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Kurumsal Başlık
st.title("⚖️ SBA 2026 Karar Destek Sistemi")
st.markdown("### **Sağlık Bilimleri Araştırma Etik Kurulu - 2026**")
st.write("---")

# --- VERİ SETİ: RAPORTÖRLER (Tam Liste) ---
raportorler = {
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

# --- VERİ SETİ: İLK 10 BİRİM VE SORUMLULARI ---
birim_listesi = [
    {"Birim": "Kulak Burun Boğaz Anabilim Dalı", "Sorumlu": "Prof. Dr. Ahmet Yılmaz", "Sayi": 5},
    {"Birim": "Ortopedi ve Travmatoloji Anabilim Dalı", "Sorumlu": "Doç. Dr. Mehmet Demir", "Sayi": 5},
    {"Birim": "Nöroloji Anabilim Dalı", "Sorumlu": "Prof. Dr. Ayşe Kaya", "Sayi": 5},
    {"Birim": "Anatomi Anabilim Dalı", "Sorumlu": "Dr. Öğr. Üyesi Caner Ak", "Sayi": 4},
    {"Birim": "Radyoloji Anabilim Dalı", "Sorumlu": "Prof. Dr. Selin Er", "Sayi": 4},
    {"Birim": "Çocuk ve Ergen Ruh Sağlığı A.D.", "Sorumlu": "Doç. Dr. Burak Can", "Sayi": 4},
    {"Birim": "Üroloji Anabilim Dalı", "Sorumlu": "Prof. Dr. Deniz Şahin", "Sayi": 4},
    {"Birim": "Deri ve Zührevi Hastalıklar A.D.", "Sorumlu": "Dr. Öğr. Üyesi Elif Gün", "Sayi": 4},
    {"Birim": "Fiziksel Tıp ve Rehabilitasyon A.D.", "Sorumlu": "Doç. Dr. Murat Işık", "Sayi": 3},
    {"Birim": "Göz Hastalıkları Anabilim Dalı", "Sorumlu": "Prof. Dr. Zeynep Türk", "Sayi": 3}
]

# --- SEKME YAPISI (TABS) ---
tab_raportor, tab_birim = st.tabs(["👤 Raportör Dosya Detayları", "🏢 Birim & Sorumlu Analizi"])

with tab_raportor:
    secilen = st.selectbox("Analiz Edilecek Raportörü Seçiniz:", ["Genel Durum"] + list(raportorler.keys()))
    
    if secilen == "Genel Durum":
        st.metric("📈 Kurul Toplam Başvuru", "145")
        st.info("Detaylı iş durumu analizi için yukarıdan bir raportör seçiniz.")
    else:
        u = raportorler[secilen]
        karar_toplam = u['ONAY'] + u['DÜZELTME'] + u['KAEK'] + u['GÖRÜŞ'] + u['RET']
        bekleyen = u['Atanan'] - karar_toplam
        
        # Metrik Kartları
        m1, m2, m3 = st.columns(3)
        m1.metric("📌 Toplam Atanan", f"{u['Atanan']} Dosya")
        m2.metric("✅ Karar Alınan", f"{karar_toplam}")
        m3.metric("⏳ İşlem Bekleyen", f"{bekleyen}", delta_color="inverse")

        st.write("### 📊 Detaylı Karar Dağılımı")
        # İlerleme Çubukları ile Ayrıntılı Görünüm
        for k, v in u.items():
            if k != "Atanan" and v >= 0:
                yuzde = (v / u['Atanan']) if u['Atanan'] > 0 else 0
                st.write(f"**{k}**: {v} dosya")
                st.progress(yuzde)

with tab_birim:
    st.subheader("🏢 En Çok Başvuru Yapan İlk 10 Birim")
    st.write("Kurula gelen dosyaların birimlere ve sorumlularına göre dağılımı:")
    
    # Birim Kartları
    for b in birim_listesi:
        st.markdown(f"""
            <div class="birim-kart">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{b['Birim']}</strong><br>
                        <small>Sorumlu: {b['Sorumlu']}</small>
                    </div>
                    <div style="font-size: 20px; font-weight: bold; color: #003366;">{b['Sayi']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.write("---")
st.markdown("<center>© 2026 Sağlık Bilimleri Araştırma Etik Kurulu</center>", unsafe_allow_html=True)
