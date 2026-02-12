import streamlit as st

# Sayfa Ayarları (Web ve Mobil Uyumlu)
st.set_page_config(page_title="SBA 2026 Rapor", layout="centered")

st.title("📊 SBA 2026 Kurul Analiz Sistemi")

# --- RAPORTÖR VERİLERİ (Görsellerden Güncellendi) ---
veriler = {
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

# Seçim Menüsü
secilen = st.selectbox("👤 Analiz İçin Raportör Seçiniz:", ["Genel Bakış"] + sorted(veriler.keys()))

if secilen == "Genel Bakış":
    st.info("Kurul üyelerinin güncel durumlarını görmek için yukarıdan bir isim seçiniz.")
    st.metric("📈 Kurul Toplam Başvuru", "145")
else:
    u = veriler[secilen]
    
    # Ana Metrik Kartları (Telefonda yan yana görünür)
    c1, c2 = st.columns(2)
    c1.metric("Dosya Yükü", f"{u['Atanan']} Adet")
    karar_sayisi = u['ONAY'] + u['DÜZELTME'] + u['KAEK'] + u['GÖRÜŞ'] + u['RET']
    c2.metric("Karar Verilen", f"{karar_sayisi} Adet")

    st.write("---")
    st.subheader("📋 Karar Dağılım Listesi")

    # Mobil uyumlu ilerleme çubukları (Progress bars)
    # Bu yöntem hem çok şıktır hem de telefonda asla hata vermez.
    def goster(etiket, deger, renk):
        if deger > 0:
            oran = min(deger / u['Atanan'], 1.0)
            st.write(f"**{etiket}**: {deger}")
            st.progress(oran)

    goster("✅ ONAY", u['ONAY'], "green")
    goster("🔧 DÜZELTME", u['DÜZELTME'], "blue")
    goster("🔬 KAEK", u['KAEK'], "purple")
    goster("💬 GÖRÜŞ", u['GÖRÜŞ'], "orange")
    goster("🚫 RET", u['RET'], "red")

st.divider()
st.caption("📱 Bu panel mobil cihazlar için optimize edilmiştir.")
