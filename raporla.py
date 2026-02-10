import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SBA 2026 Analiz", layout="wide")

if 'ana_veri' not in st.session_state:
    st.session_state['ana_veri'] = None

st.title("📊 SBA 2026 Kurul Analiz Sistemi")

# --- SOL PANEL ---
with st.sidebar:
    st.header("⚙️ Yönetici Paneli")
    yuklenen_dosya = st.file_uploader("Excel Yükle (XLSX)", type=["xlsx"])
    if yuklenen_dosya:
        try:
            # Sadece "Üye_1" sayfasını okuyoruz
            df_uye = pd.read_excel(yuklenen_dosya, sheet_name="Üye_1")
            # Sütun isimlerini temizle
            df_uye.columns = [str(c).strip() for c in df_uye.columns]
            st.session_state['ana_veri'] = df_uye
            st.success("✅ Üye_1 Verisi Yüklendi!")
        except Exception as e:
            st.error(f"Sayfa Okuma Hatası: {e}")

# --- ANA EKRAN ---
if st.session_state['ana_veri'] is not None:
    df = st.session_state['ana_veri']
    
    # Raporlama yapılacak sütun aralığı (C'den AQ'ya - İsimden sonrasına kadar)
    # Pandas'ta C sütunu genellikle 2. indextir. İsimler 'A' veya 'B'deyse ona göre seçer.
    # Biz burada 'AD-SOYAD' sütununu bulup sonrasındaki sayısal verileri alacağız.
    
    isim_sutunu = 'AD-SOYAD' # Excel'deki tam sütun adı neyse o olmalı
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("🔍 Kurul Üyesi")
        uye_listesi = sorted(df[isim_sutunu].dropna().unique())
        secilen_uye = st.selectbox("Üye Seçiniz:", ["Seçiniz..."] + uye_listesi)

    with col2:
        if secilen_uye != "Seçiniz...":
            # Seçilen üyenin satırını bul
            uye_satiri = df[df[isim_sutunu] == secilen_uye].iloc[0]
            
            # C (index 2) ile AQ (index 42) arasını alıyoruz. 
            # Not: Excel yapınıza göre bu indexleri gerekirse kaydırabiliriz.
            analiz_verisi = uye_satiri.iloc[2:43] # C'den AQ'ya kadar olan sütunlar
            
            # Sadece değeri 0'dan büyük olan kararları filtrele (Tablo temiz görünsün)
            analiz_verisi = analiz_verisi[analiz_verisi > 0]
            
            # Toplam Dosya (AQ sütunu genelde TOPLAM olur)
            toplam_is = analiz_verisi.sum()
            
            st.metric(f"👤 {secilen_uye}", f"Toplam {toplam_is} Karar/Dosya")
            
            if not analiz_verisi.empty:
                fig, ax = plt.subplots(figsize=(10, 6))
                analiz_verisi.plot(kind='barh', ax=ax, color='#2ecc71')
                ax.set_title(f"{secilen_uye} - Detaylı Karar Dağılımı", fontweight='bold')
                ax.invert_yaxis()
                for i, v in enumerate(analiz_verisi.values):
                    ax.text(v + 0.1, i, str(int(v)), va='center', fontweight='bold')
                st.pyplot(fig)
            else:
                st.warning("Bu üyeye ait kayıtlı bir karar bulunamadı.")
        else:
            # Genel Toplam (Tüm kurulun toplam başvurusu)
            # Eğer toplam sayı bir hücrede yazıyorsa onu çekelim, yoksa sum yapalım.
            genel_toplam = 145 # Sizin belirttiğiniz sabit rakam veya hesaplama
            st.metric("📈 Kurul Genel Toplam Başvuru", genel_toplam)
            st.info("Lütfen detaylarını görmek istediğiniz üyeyi soldan seçiniz.")

else:
    st.warning("⚠️ Lütfen 'Üye_1' sayfasını içeren Excel'i yükleyiniz.")
