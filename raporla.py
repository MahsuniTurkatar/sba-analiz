import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sayfa Genişliği ve Başlık
st.set_page_config(page_title="SBA 2026 Analiz", layout="wide")

st.title("📊 SBA 2026 Kurul Analiz Sistemi")

# --- SABİT VERİ SÖZLÜĞÜ (Excel'den Manuel Giriş) ---
# Buraya Excel'deki verileri bu formatta ekleyebilirsin
veriler = {
    "Dr. Öğr. Üyesi Müge DEMİR": {
        "Dosya Sayısı": 31,
        "ONAY": 18,
        "DÜZELTME": 11,
        "KAEK": 2,
        "GÖRÜŞ": 0,
        "RET": 0,
        "KAPSAM DIŞI": 0,
        "GERİ ÇEKİLDİ": 0
    },
    "Doç. Dr. Kübra AYKAÇ": {
        "Dosya Sayısı": 30,
        "ONAY": 14,
        "DÜZELTME": 9,
        "KAEK": 0,
        "GÖRÜŞ": 1,
        "RET": 1,
        "KAPSAM DIŞI": 0,
        "GERİ ÇEKİLDİ": 0
    },
    "Doç. Dr. Burcu ERSÖZ ALAN": {
        "Dosya Sayısı": 28,
        "ONAY": 18,
        "DÜZELTME": 6,
        "KAEK": 0,
        "GÖRÜŞ": 0,
        "RET": 0,
        "KAPSAM DIŞI": 0,
        "GERİ ÇEKİLDİ": 0
    }
    # Diğer hocalarımızı da buraya aynı formatta ekleyebiliriz
}

# --- ARAYÜZ ---
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("🔍 Kurul Üyesi")
    uye_listesi = sorted(veriler.keys())
    secilen_uye = st.selectbox("Bir Üye Seçiniz:", ["Seçiniz..."] + uye_listesi)

with col2:
    if secilen_uye != "Seçiniz...":
        data = veriler[secilen_uye]
        
        # Üst Metrik
        st.metric(f"👤 {secilen_uye}", f"Atanan Dosya Sayısı: {data['Dosya Sayısı']}")
        
        # Grafik Hazırlığı (Sadece 0'dan büyük kararları göster)
        grafik_datasi = {k: v for k, v in data.items() if k != "Dosya Sayısı" and v > 0}
        analiz = pd.Series(grafik_datasi)
        
        if not analiz.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            analiz.plot(kind='barh', ax=ax, color='#3498db')
            ax.set_title(f"{secilen_uye} - Karar Dağılımı", fontweight='bold', fontsize=14)
            ax.set_xlabel("Dosya Sayısı")
            ax.invert_yaxis()
            
            # Barların üzerine sayıları yaz
            for i, v in enumerate(analiz.values):
                ax.text(v + 0.1, i, str(int(v)), va='center', fontweight='bold')
            
            st.pyplot(fig)
        else:
            st.warning("Bu üyeye ait henüz karar girişi bulunmuyor.")
    else:
        # Ana Ekran Metriği (İstediğin o 145 rakamı)
        st.metric("📈 Kurul Genel Başvuru Toplamı", "145")
        st.info("Kurul üyelerinin güncel durumlarını görmek için soldan bir isim seçiniz.")

st.divider()
st.caption("Veriler manuel olarak sisteme işlenmiştir. Güncelleme için raporla.py dosyasını düzenleyiniz.")
